"""Initiate Marzneshin database

Revision ID: 20faa9f18c0a
Revises:
Create Date: 2024-01-15 09:48:24.808505

"""
import os
from alembic import op
import sqlalchemy as sa
from app.utils.crypto import generate_certificate

# revision identifiers, used by Alembic.
revision = '20faa9f18c0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('hashed_password', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_sudo', sa.Boolean(), nullable=True),
    sa.Column('password_reset_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.create_index(op.f('ix_admins_username'), 'admins', ['username'], unique=True)
    
    jwttable = op.create_table('jwt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secret_key', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(jwttable, [{"id": 1, "secret_key": os.urandom(32).hex()}])

    op.create_table('nodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256, collation='NOCASE'), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('api_port', sa.Integer(), nullable=False),
    sa.Column('xray_version', sa.String(length=32), nullable=True),
    sa.Column('status', sa.Enum('connected', 'connecting', 'error', 'disabled', name='nodestatus'), nullable=False),
    sa.Column('last_status_change', sa.DateTime(), nullable=True),
    sa.Column('message', sa.String(length=1024), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('uplink', sa.BigInteger(), nullable=True),
    sa.Column('downlink', sa.BigInteger(), nullable=True),
    sa.Column('usage_coefficient', sa.Float(), server_default=sa.text('(1.0)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_nodes_id'), 'nodes', ['id'], unique=False)
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)
    op.create_index(op.f('ix_services_name'), 'services', ['name'], unique=False)
    
    systable = op.create_table('system',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uplink', sa.BigInteger(), nullable=True),
    sa.Column('downlink', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(systable, [{"id": 1, "uplink": 0, "downlink": 0}])
    op.create_index(op.f('ix_system_id'), 'system', ['id'], unique=False)
    
    tlstable = op.create_table('tls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=4096), nullable=False),
    sa.Column('certificate', sa.String(length=2048), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    tls = generate_certificate()
    op.bulk_insert(tlstable, [{"id": 1, "key": tls['key'], "certificate": tls['cert']}])

    op.create_table('inbounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('protocol', sa.String(), nullable=True),
    sa.Column('tag', sa.String(length=256), nullable=False),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inbounds_node_id'), 'inbounds', ['node_id'], unique=False)
    op.create_index(op.f('ix_inbounds_tag'), 'inbounds', ['tag'], unique=False)
    op.create_table('node_usages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.Column('uplink', sa.BigInteger(), nullable=True),
    sa.Column('downlink', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('created_at', 'node_id')
    )
    op.create_index(op.f('ix_node_usages_id'), 'node_usages', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32, collation='NOCASE'), nullable=True),
    sa.Column('key', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Enum('active', 'disabled', 'limited', 'expired', 'on_hold', name='userstatus'), nullable=False),
    sa.Column('used_traffic', sa.BigInteger(), nullable=True),
    sa.Column('data_limit', sa.BigInteger(), nullable=True),
    sa.Column('data_limit_reset_strategy', sa.Enum('no_reset', 'day', 'week', 'month', 'year', name='userdatalimitresetstrategy'), nullable=False),
    sa.Column('ip_limit', sa.Integer(), nullable=False),
    sa.Column('settings', sa.String(), nullable=True),
    sa.Column('expire', sa.Integer(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('sub_revoked_at', sa.DateTime(), nullable=True),
    sa.Column('sub_updated_at', sa.DateTime(), nullable=True),
    sa.Column('sub_last_user_agent', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('note', sa.String(length=500), nullable=True),
    sa.Column('online_at', sa.DateTime(), nullable=True),
    sa.Column('on_hold_expire_duration', sa.BigInteger(), nullable=True),
    sa.Column('on_hold_timeout', sa.DateTime(), nullable=True),
    sa.Column('edit_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_key'), 'users', ['key'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('hosts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('remark', sa.String(length=256), nullable=False),
    sa.Column('address', sa.String(length=256), nullable=False),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=256), nullable=True),
    sa.Column('sni', sa.String(length=256), nullable=True),
    sa.Column('host', sa.String(length=256), nullable=True),
    sa.Column('security', sa.Enum('inbound_default', 'none', 'tls', name='inboundhostsecurity'), nullable=False),
    sa.Column('alpn', sa.Enum('none', 'h2', 'http/1.1', 'h2,http/1.1', name='proxyhostalpn'), server_default='none', nullable=False),
    sa.Column('fingerprint', sa.Enum('none', 'chrome', 'firefox', 'safari', 'ios', 'android', 'edge', '360', 'qq', 'random', 'randomized', name='proxyhostfingerprint'), server_default='none', nullable=False),
    sa.Column('inbound_id', sa.Integer(), nullable=False),
    sa.Column('allowinsecure', sa.Boolean(), nullable=True),
    sa.Column('is_disabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['inbound_id'], ['inbounds.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inbounds_services',
    sa.Column('inbound_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inbound_id'], ['inbounds.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
    sa.PrimaryKeyConstraint('inbound_id', 'service_id')
    )
    op.create_table('node_user_usages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.Column('used_traffic', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['nodes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('created_at', 'user_id', 'node_id')
    )
    op.create_index(op.f('ix_node_user_usages_id'), 'node_user_usages', ['id'], unique=False)
    op.create_table('notification_reminders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Enum('expiration_date', 'data_usage', name='remindertype'), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_reminders_id'), 'notification_reminders', ['id'], unique=False)
    op.create_table('user_usage_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('used_traffic_at_reset', sa.BigInteger(), nullable=False),
    sa.Column('reset_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_usage_logs_id'), 'user_usage_logs', ['id'], unique=False)
    op.create_table('users_services',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'service_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_services')
    op.drop_index(op.f('ix_user_usage_logs_id'), table_name='user_usage_logs')
    op.drop_table('user_usage_logs')
    op.drop_index(op.f('ix_notification_reminders_id'), table_name='notification_reminders')
    op.drop_table('notification_reminders')
    op.drop_index(op.f('ix_node_user_usages_id'), table_name='node_user_usages')
    op.drop_table('node_user_usages')
    op.drop_table('inbounds_services')
    op.drop_table('hosts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_key'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_node_usages_id'), table_name='node_usages')
    op.drop_table('node_usages')
    op.drop_index(op.f('ix_inbounds_tag'), table_name='inbounds')
    op.drop_index(op.f('ix_inbounds_node_id'), table_name='inbounds')
    op.drop_table('inbounds')
    op.drop_table('tls')
    op.drop_index(op.f('ix_system_id'), table_name='system')
    op.drop_table('system')
    op.drop_index(op.f('ix_services_name'), table_name='services')
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')
    op.drop_index(op.f('ix_nodes_id'), table_name='nodes')
    op.drop_table('nodes')
    op.drop_table('jwt')
    op.drop_index(op.f('ix_admins_username'), table_name='admins')
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_table('admins')
    # ### end Alembic commands ###