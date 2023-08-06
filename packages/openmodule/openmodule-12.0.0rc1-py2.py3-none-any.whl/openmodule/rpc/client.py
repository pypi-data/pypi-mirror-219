import logging
import threading
import time
import warnings
from typing import Dict, Optional, List, Type
from uuid import uuid4

import pydantic
from pydantic import BaseModel, parse_obj_as

from openmodule.config import settings
from openmodule.core import core
from openmodule.dispatcher import SubscribingMessageDispatcher
from openmodule.messaging import wait_for_connection
from openmodule.models.base import OpenModuleModel
from openmodule.models.rpc import RPCResponse, RPCRequest, RPCErrorResult, RPCServerError
from openmodule.rpc.common import channel_to_response_topic, channel_to_request_topic


class RPCClient:
    class Exception(Exception):
        pass

    class CancelError(Exception):
        pass

    class ValidationError(pydantic.ValidationError, Exception):
        pass

    class TimeoutError(Exception, TimeoutError):
        pass

    class ServerHandlerError(Exception):
        pass

    class ServerFilterError(Exception):
        pass

    class ServerValidationError(Exception):
        pass

    class RPCServerError(Exception):  # error we got from RPCServer running in the Internet
        pass

    class ServerUnknownError(Exception):
        pass

    class RPCEntry:
        def __init__(self, timeout):
            self.timestamp = time.time()
            self.timeout = timeout
            self.response = None
            self.ready = threading.Event()
            self.cancelled = False

        def done(self):
            return bool(self.response)

        def result(self, response_type: Type[OpenModuleModel], timeout=None):
            if timeout and (timeout > self.timeout):
                warnings.warn("You cannot extend the timeout of an RPC after sending the request. "
                              "The timeout will be limited to at most the initial timeout.", stacklevel=2)
                timeout = max(timeout, self.timeout)

            if self.response is None:
                timeout = timeout or self.timeout
                maximum_wait_time = (self.timestamp + timeout) - time.time()

                if maximum_wait_time < 0:  # timeout has already passed
                    raise RPCClient.TimeoutError()

                if not self.ready.wait(timeout=maximum_wait_time):
                    raise RPCClient.TimeoutError()

                if self.cancelled:
                    raise RPCClient.CancelError()

            try:
                if self.response.get("status", "ok") == "ok":
                    return parse_obj_as(response_type, self.response)
                else:
                    error_result = RPCErrorResult.parse_obj(self.response)
                    if error_result.status == RPCServerError.handler_error:
                        raise RPCClient.ServerHandlerError(error_result.exception or "")
                    elif error_result.status == RPCServerError.validation_error:
                        raise RPCClient.ServerValidationError(error_result.exception or "")
                    elif error_result.status == RPCServerError.filter_error:
                        raise RPCClient.ServerFilterError(error_result.exception or "")
                    elif error_result.status == RPCServerError.error:
                        raise RPCClient.RPCServerError(error_result.error)
                    else:
                        assert RPCClient.ServerUnknownError("RPCErrorResult successfully parsed but status not handled."
                                                            " Implement this!")
            except pydantic.ValidationError as e:
                raise RPCClient.ValidationError(e.raw_errors, e.model)

        def cancel(self):
            self.cancelled = True
            self.ready.set()

    def __init__(self, dispatcher: SubscribingMessageDispatcher, channels: Optional[List[str]] = None,
                 default_timeout=3.,  _warn=True):
        # the new design with one dedicated thread for the rpc client in the core discourages instantiating the
        # rpc client on its own. so we warn every user about this
        if _warn:
            warnings.warn(
                "\n\nInstantiating the RPC Client on your own is discouraged. PLease use the open module core's rpc "
                "client. For testcases or if you absolutely MUST for whatever reason instantiate the client pass "
                "`_warn=False` to the constructor.", DeprecationWarning, stacklevel=2
            )

        if channels is None:
            channels = []
        assert all(isinstance(channel, str) for channel in channels), "channels must be a list of strings"

        self.dispatcher = dispatcher
        self.log = logging.getLogger("rcp-client")
        self.lock = threading.Lock()
        self.results = dict()
        self.default_timeout = default_timeout
        self.running = True

        self.channels = []
        for channel in channels:
            self.register_channel(channel)
        if self.channels:
            wait_for_connection(self.dispatcher)

    def register_channel(self, channel: str):
        assert self.running, "Cannot register channels when rpc client is shutdown"
        assert isinstance(channel, str), "channel must be a string"

        if channel not in self.channels:
            self.channels.append(channel)
            topic = channel_to_response_topic(channel)
            self.log.debug("Registering channel: {}".format(topic))
            self.dispatcher.register_handler(topic, RPCResponse, self.receive, match_type=False)

    def unregister_channel(self, channel: str):
        assert isinstance(channel, str), "channel must be a string"

        self.channels.remove(channel)
        topic = channel_to_response_topic(channel)
        self.log.debug("Unregistering channel: {}".format(topic))
        self.dispatcher.unsubscribe(topic)

    def cleanup_old_results(self):
        now = time.time()
        with self.lock:
            to_delete = []
            for rpc_id, entry in self.results.items():
                if now > entry.timestamp + entry.timeout:
                    to_delete.append(rpc_id)
            for rpc_id in to_delete:
                self.results.pop(rpc_id, None)

    def _call(self, channel: str, typ: str, request: Dict, timeout: float):
        rpc_id = str(uuid4())

        request = RPCRequest(rpc_id=rpc_id, name=settings.NAME, request=request, type=typ)
        topic = channel_to_request_topic(channel)
        entry = self.RPCEntry(timeout=timeout)
        with self.lock:
            self.results[rpc_id] = entry
        core().publish(topic=topic, message=request)
        return entry

    def rpc_non_blocking(self, channel: str, type: str, request: [Dict, BaseModel], timeout: float = None) -> RPCEntry:
        assert isinstance(channel, str), "channel must be a string"

        self.cleanup_old_results()
        if isinstance(request, dict):
            warnings.warn(
                '\n\nPassing dicts as RPC Requests is deprecated and will be removed. Please '
                'define your RPC in a model and pass a model instance.\n',
                DeprecationWarning, stacklevel=2
            )

        if timeout is None:
            timeout = self.default_timeout

        if channel not in self.channels:
            self.register_channel(channel)
            wait_for_connection(self.dispatcher)

        return self._call(channel, type, request, timeout)

    def rpc(self, channel: str, type: str, request: [Dict, BaseModel], response_type: Type[OpenModuleModel],
            timeout: float = None) -> OpenModuleModel:
        entry = self.rpc_non_blocking(channel, type, request, timeout)
        return entry.result(response_type, timeout=timeout)

    def shutdown(self):
        self.running = False
        for channel in self.channels:
            self.unregister_channel(channel)

    def receive(self, response: RPCResponse):
        """handler that receives and saves the rpc responses"""
        self.cleanup_old_results()
        with self.lock:
            entry = self.results.get(str(response.rpc_id))
        if entry:
            entry.response = response.response
            entry.ready.set()
