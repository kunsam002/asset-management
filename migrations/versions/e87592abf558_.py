"""empty message

Revision ID: e87592abf558
Revises: None
Create Date: 2016-04-30 15:06:59.136478

"""

# revision identifiers, used by Alembic.
revision = 'e87592abf558'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line1', sa.String(), nullable=False),
    sa.Column('line2', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_address_date_created'), 'address', ['date_created'], unique=False)
    op.create_index(op.f('ix_address_last_updated'), 'address', ['last_updated'], unique=False)
    op.create_table('utility_provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_utility_provider_date_created'), 'utility_provider', ['date_created'], unique=False)
    op.create_index(op.f('ix_utility_provider_last_updated'), 'utility_provider', ['last_updated'], unique=False)
    op.create_table('consumer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('utility_provider_id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['utility_provider_id'], ['utility_provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consumer_date_created'), 'consumer', ['date_created'], unique=False)
    op.create_index(op.f('ix_consumer_last_updated'), 'consumer', ['last_updated'], unique=False)
    op.create_table('transformer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transformer_date_created'), 'transformer', ['date_created'], unique=False)
    op.create_index(op.f('ix_transformer_last_updated'), 'transformer', ['last_updated'], unique=False)
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reference_id', sa.String(), nullable=False),
    sa.Column('consumer_id', sa.Integer(), nullable=True),
    sa.Column('utility_provider_id', sa.Integer(), nullable=True),
    sa.Column('is_master', sa.Boolean(), nullable=True),
    sa.Column('is_slave', sa.Boolean(), nullable=True),
    sa.Column('transformer_id', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['consumer_id'], ['consumer.id'], ),
    sa.ForeignKeyConstraint(['transformer_id'], ['transformer.id'], ),
    sa.ForeignKeyConstraint(['utility_provider_id'], ['utility_provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_date_created'), 'device', ['date_created'], unique=False)
    op.create_index(op.f('ix_device_last_updated'), 'device', ['last_updated'], unique=False)
    op.create_table('power_reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('voltage', sa.Float(), nullable=True),
    sa.Column('current', sa.Float(), nullable=True),
    sa.Column('power', sa.Float(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_power_reading_date_created'), 'power_reading', ['date_created'], unique=False)
    op.create_index(op.f('ix_power_reading_last_updated'), 'power_reading', ['last_updated'], unique=False)
    op.create_table('temparature_reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('degree', sa.Float(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('transformer_id', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['transformer_id'], ['transformer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_temparature_reading_date_created'), 'temparature_reading', ['date_created'], unique=False)
    op.create_index(op.f('ix_temparature_reading_last_updated'), 'temparature_reading', ['last_updated'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_temparature_reading_last_updated'), table_name='temparature_reading')
    op.drop_index(op.f('ix_temparature_reading_date_created'), table_name='temparature_reading')
    op.drop_table('temparature_reading')
    op.drop_index(op.f('ix_power_reading_last_updated'), table_name='power_reading')
    op.drop_index(op.f('ix_power_reading_date_created'), table_name='power_reading')
    op.drop_table('power_reading')
    op.drop_index(op.f('ix_device_last_updated'), table_name='device')
    op.drop_index(op.f('ix_device_date_created'), table_name='device')
    op.drop_table('device')
    op.drop_index(op.f('ix_transformer_last_updated'), table_name='transformer')
    op.drop_index(op.f('ix_transformer_date_created'), table_name='transformer')
    op.drop_table('transformer')
    op.drop_index(op.f('ix_consumer_last_updated'), table_name='consumer')
    op.drop_index(op.f('ix_consumer_date_created'), table_name='consumer')
    op.drop_table('consumer')
    op.drop_index(op.f('ix_utility_provider_last_updated'), table_name='utility_provider')
    op.drop_index(op.f('ix_utility_provider_date_created'), table_name='utility_provider')
    op.drop_table('utility_provider')
    op.drop_index(op.f('ix_address_last_updated'), table_name='address')
    op.drop_index(op.f('ix_address_date_created'), table_name='address')
    op.drop_table('address')
    ### end Alembic commands ###