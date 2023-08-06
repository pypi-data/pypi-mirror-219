import logging
from collections import namedtuple
from datetime import datetime
from enum import Enum
from typing import Optional, Callable, Union, List, Dict, Tuple, Set, Any
from typing import TYPE_CHECKING

from openmodule.config import settings
from pydantic import Field

from openmodule.models.base import ZMQMessage, OpenModuleModel, datetime_to_timestamp, timezone_validator

if TYPE_CHECKING:  # pragma: no cover
    from openmodule.core import OpenModuleCore


class HealthPongPayload(OpenModuleModel):
    status: str = "ok"
    version: str
    name: str
    startup: datetime
    message: Optional[str]

    _tz_last_update = timezone_validator("startup")

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["startup"] = datetime_to_timestamp(data["startup"])
        return data


class HealthMetricType(str, Enum):
    count: str = "count"
    gauge: str = "gauge"
    str: str = "str"


class HealthMetric(OpenModuleModel):
    id: str = Field(..., description="A identifier for this metric. Must be unique per `package` this check is "
                                     "assigned to, independently of the source service which is returning the metric.")
    name: str = Field(..., description="Human readable name of the Metric.")
    description: str = Field(..., description="Human-readable description of the metric. The same description will be"
                                              "displayed when the metric is displayed.")
    type: HealthMetricType = Field(..., description="The type of this metric. This is used to determine how the metric"
                                                    "is used.")
    labels: List[str] = Field(..., description="List of label names for this metric. In debug and testing mode exactly"
                                               "those labels are required for the metric to be valid. In production"
                                               "wrong labels are still accepted.")
    values: Dict[str, Any] = Field(
        {}, description="Contains the values for this metric, grouped by labels. The labels are "
                        "represented as a the string of the sorted list of label items. str(list(<label_dict>.items()))"
                        "'[(<label_name>, <label_value>), (<label_name>, <label_value>), ...]: <metric_value>'")
    package: str = Field(..., description="The package this metric is assigned to. It may be your own service"
                                          "but can also be any other hardware or software service.")
    source: Optional[str] = Field(None,
                                  description="The service which reported the health check. This value is "
                                              "automatically set by health service and must not be set manually.")


class HealthCheckState(str, Enum):
    ok = "ok"
    fail = "fail"
    no_data = "no-data"


class HealthCheck(OpenModuleModel):
    id: str = Field(..., description="A identifier for this check. Must be unique per `package` this check is "
                                     "assigned to, independently of the source service which is returning the check.")
    package: str = Field(..., description="The package this check is assigned to. It may be your own service"
                                          "but can also be any other hardware or software service.")
    state: HealthCheckState = Field("no-data", description="The state of this check")
    name: str = Field(..., description="Human readable name of the check. ")
    description: Optional[str] = Field(...,
                                       description="Human-readable description of the check. The same description"
                                                   "will be displayed when the check fails or succeeds. Consider this"
                                                   "when choosing the wording.")
    message: Optional[str] = Field(None,
                                   description="A human readable text which is displayed next to the check in the "
                                               "user interface. Can be used to convey more information. Please "
                                               "note that no efforts are taken to notify the user about changes "
                                               "in this value (i.e. no new e-mails are sent if the message "
                                               "changes).")
    source: Optional[str] = Field(None,
                                  description="The service which reported the health check. This value is "
                                              "automatically set by health service and must not be set manually.")


class HealthPongMessage(ZMQMessage):
    type: str = "healthz"
    pong: HealthPongPayload
    metrics: Optional[List[HealthMetric]]
    checks: Optional[List[HealthCheck]]


class HealthPingMessage(ZMQMessage):
    type: str = "ping"


startup = datetime.utcnow()

HealthResult = namedtuple("HealthResult", "status,message,meta")

HealthHandlerType = Callable[[], HealthResult]


class Healthz:
    health_handler: HealthHandlerType

    templates: Dict[str, Tuple[str, str]] = {}
    metrics: Dict[Tuple[str, str], HealthMetric] = {}
    checks: Dict[Tuple[str, str], HealthCheck] = {}

    def __init__(self, core: 'OpenModuleCore'):
        self.core = core
        self.log = logging.getLogger(self.__class__.__name__)
        self.metrics = {}
        self.checks = {}

    def _check_id(self, check_id: str, parent: Optional[bool] = False, package: Optional[str] = None):
        assert not (parent and package), "you can only set either parent or package"
        if parent:
            package = self.core.config.PARENT
            assert package, "no parent is set"
        else:
            package = package or self.core.config.NAME
        return check_id, package

    def add_check_template(self, check_id: str, name: str, description: str = None):
        self.templates[check_id] = (name, description)

    def update_template_packages(self, check_id: str, packages: Union[List[str], Set[str]]):
        existing_packages = set(x[1] for x in self.checks if x[0] == check_id)
        packages_set = set(packages)
        for package in existing_packages - packages_set:
            self.checks.pop((check_id, package))
        for package in packages_set - existing_packages:
            name, description = self.templates[check_id]
            self.add_check(check_id, name, description, package=package)

    def add_check(self, check_id: str, name: str, description: str, *, parent: Optional[bool] = False,
                  package: Optional[str] = None):
        key = self._check_id(check_id, parent, package)
        self.checks[key] = HealthCheck(
            id=check_id,
            package=key[1],
            name=name,
            description=description,
            state=HealthCheckState.no_data
        )

    def remove_check(self, check_id, *, parent: Optional[bool] = False, package: Optional[str] = None):
        key = self._check_id(check_id, parent, package)
        self.checks.pop(key, None)

    def set_check_state(self, check_id: str, state: HealthCheckState, *, parent: Optional[bool] = False,
                        package: Optional[str] = None, message: Optional[str] = None):
        key = self._check_id(check_id, parent, package)
        check = self.checks.get(key)
        if check:
            check.state = state
            if state == HealthCheckState.fail:
                check.message = message
            else:
                check.message = None
        else:
            if self.core.config.DEBUG or self.core.config.TESTING:
                assert False, "please ensure you register your checks properly beforehand"
            self.log.warning(f"Check {key} not found, the check state will not be set")

    def check_fail(self, check_id: str, *, parent: Optional[bool] = False, package: Optional[str] = None,
                   message: Optional[str] = None):
        self.set_check_state(check_id, HealthCheckState.fail, parent=parent, package=package, message=message)

    def check_success(self, check_id: str, *, parent: Optional[bool] = False, package: Optional[str] = None,
                      message: Optional[str] = None):
        self.set_check_state(check_id, HealthCheckState.ok, parent=parent, package=package, message=message)

    def add_metric(self, metric_id: str, metric_type: HealthMetricType, name: str, description: str, *,
                   labels: List[str] = None, parent: Optional[bool] = False, package: Optional[str] = None):
        key = self._check_id(metric_id, parent, package)
        labels = set(labels or ())
        self.metrics[key] = HealthMetric(
            id=metric_id,
            name=name,
            type=metric_type,
            package=key[1],
            description=description,
            labels=list(labels),
        )

    def remove_metric(self, metric_id: str, *, parent: Optional[bool] = False, package: Optional[str] = None):
        key = self._check_id(metric_id, parent, package)
        self.metrics.pop(key, None)

    def _metric_log_or_raise(self, msg, *args, **kwargs):
        if settings.DEBUG or settings.TESTING:
            raise ValueError(msg, *args)
        else:
            self.log.error(msg, *args, **kwargs)

    def _metric_check_labels(self, metric, labels: Dict[str, str]):
        if set(labels.keys()) != set(metric.labels):
            self._metric_log_or_raise("Metric %s labels do not match the metric definition: expected %s, got %s",
                                      metric.id, metric.labels, list(labels.keys()))

    def metric_clear(self, metric_id: str, *, parent: Optional[bool] = False, package: Optional[str] = None,
                     values_to_keep: List[dict] = None):
        key = self._check_id(metric_id, parent, package)
        keep = [self._labels_string(x) for x in values_to_keep or ()]
        metric = self.metrics.get(key)
        if not metric:
            self._metric_log_or_raise("Metric %s not found, cannot be cleared", key)
        if keep:
            metric.values = {k: v for k, v in metric.values.items() if k in keep}
        else:
            metric.values = {}

    @staticmethod
    def _labels_string(labels: dict):
        labels["compute_id"] = settings.COMPUTE_ID
        return str(sorted(((k, str(v)) for k, v in labels.items())))

    def metric_inc(self, metric_id: str, amount: Union[int, float] = 1, *,
                   parent: Optional[bool] = False, package: Optional[str] = None, **labels):
        key = self._check_id(metric_id, parent, package)
        metric = self.metrics.get(key)
        if not metric:
            self._metric_log_or_raise("Metric %s not found, the metric will not be increased", key)
        elif metric.type == HealthMetricType.str:
            self._metric_log_or_raise("Metric %s of type str cannot be increased, only set", key)
        elif not isinstance(amount, (int, float)):
            self._metric_log_or_raise(f"Metric %s of type {metric.type.value} cannot be set to a non-numeric value",
                                      key)
        elif metric.type == HealthMetricType.count and amount < 0:
            self._metric_log_or_raise("Metric %s of type count cannot be decreased", key)
        else:
            self._metric_check_labels(metric, labels)
            labels_string = self._labels_string(labels)
            metric.values[labels_string] = metric.values.get(labels_string, 0) + amount

    def metric_dec(self, metric_id: str, amount: Union[int, float] = 1, *,
                   parent: Optional[bool] = False, package: Optional[str] = None, **labels):
        self.metric_inc(metric_id, -amount, parent=parent, package=package, **labels)

    def metric_set(self, metric_id: str, value: Union[int, float, str, None], *,
                   parent: Optional[bool] = False, package: Optional[str] = None, **labels):
        key = self._check_id(metric_id, parent, package)
        metric = self.metrics.get(key)
        if not metric:
            self._metric_log_or_raise("Metric %s not found, the metric will not be set", key)
        if value is None:
            metric.values.pop(self._labels_string(labels), None)
        elif metric.type == HealthMetricType.count:
            self._metric_log_or_raise("Metric %s of type count cannot be set, only increased", key)
        elif metric.type == HealthMetricType.str and not isinstance(value, str):
            self._metric_log_or_raise("Metric %s of type str cannot be set to a non-string value", key)
        elif metric.type == HealthMetricType.gauge and not isinstance(value, (int, float)):
            self._metric_log_or_raise("Metric %s of type gauge cannot be set to a non-numeric value", key)
        else:
            if metric.type == HealthMetricType.str:
                value.replace('"', '\"')
            self._metric_check_labels(metric, labels)
            metric.values[self._labels_string(labels)] = value

    def process_message(self, _: HealthPingMessage):
        checks = list(self.checks.values())
        status = "ok"
        message = None
        for check in checks:
            if check.state == HealthCheckState.fail:
                status = "error"
                message = check.message
        response = HealthPongMessage(
            name=self.core.config.NAME,
            pong=HealthPongPayload(status=status, version=self.core.config.VERSION, name=self.core.config.NAME,
                                   startup=startup, message=message),
            checks=checks,
            metrics=list(self.metrics.values()),
        )
        self.core.publish(response, "healthpong")
