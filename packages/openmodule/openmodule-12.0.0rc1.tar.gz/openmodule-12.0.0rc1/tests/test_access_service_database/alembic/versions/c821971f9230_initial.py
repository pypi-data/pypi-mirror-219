"""initial

Revision ID: c821971f9230
Revises: 
Create Date: 2022-09-19 09:34:43.363411

"""
from alembic import op
import sqlalchemy as sa
from openmodule.database.custom_types import JSONEncodedDict

# revision identifiers, used by Alembic.
revision = 'c821971f9230'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.pre_upgrade()
    op.create_table('test_access_model',
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('e_tag', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.String(), nullable=True),
    sa.Column('car_id', sa.String(), nullable=True),
    sa.Column('group_id', sa.String(), nullable=True),
    sa.Column('access_infos', JSONEncodedDict(), nullable=True),
    sa.Column('lpr_id', sa.String(), nullable=True),
    sa.Column('lpr_id_search', sa.String(), nullable=True),
    sa.Column('lpr_country', sa.String(), nullable=True),
    sa.Column('matching_scheme', sa.String(), nullable=True),
    sa.Column('matching_version', sa.Integer(), nullable=True),
    sa.Column('qr_id', sa.String(), nullable=True),
    sa.Column('nfc_id', sa.String(), nullable=True),
    sa.Column('pin_id', sa.String(), nullable=True),
    sa.Column('regex', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('e_tag')
    )
    with op.batch_alter_table('test_access_model', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_test_access_model_e_tag'), ['e_tag'], unique=False)
        batch_op.create_index(batch_op.f('ix_test_access_model_key'), ['key'], unique=True)
        batch_op.create_index(batch_op.f('ix_test_access_model_lpr_id_search'), ['lpr_id_search'], unique=False)
        batch_op.create_index(batch_op.f('ix_test_access_model_nfc_id'), ['nfc_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_test_access_model_pin_id'), ['pin_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_test_access_model_qr_id'), ['qr_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_test_access_model_regex'), ['regex'], unique=False)

    op.post_upgrade()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.pre_downgrade()
    with op.batch_alter_table('test_access_model', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_test_access_model_regex'))
        batch_op.drop_index(batch_op.f('ix_test_access_model_qr_id'))
        batch_op.drop_index(batch_op.f('ix_test_access_model_pin_id'))
        batch_op.drop_index(batch_op.f('ix_test_access_model_nfc_id'))
        batch_op.drop_index(batch_op.f('ix_test_access_model_lpr_id_search'))
        batch_op.drop_index(batch_op.f('ix_test_access_model_key'))
        batch_op.drop_index(batch_op.f('ix_test_access_model_e_tag'))

    op.drop_table('test_access_model')
    op.post_downgrade()
    # ### end Alembic commands ###
