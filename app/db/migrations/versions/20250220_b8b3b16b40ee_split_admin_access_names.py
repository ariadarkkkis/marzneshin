"""Split admin access names

Revision ID: b8b3b16b40ee
Revises: 57eba0a293f2
Create Date: 2025-02-20 01:34:53.871901

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b8b3b16b40ee"
down_revision = "57eba0a293f2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "admins",
        sa.Column(
            "add_users_access",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column(
            "edit_users_access",
            sa.Boolean(),
            server_default=sa.text("0"),
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column(
            "delete_users_access",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column(
            "delete_expired_users_access",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column(
            "reset_users_usage_access",
            sa.Boolean(),
            server_default=sa.text("0"),
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column(
            "toggle_users_status_access",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )
    op.add_column(
        "admins",
        sa.Column(
            "revoke_users_sub_access",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )
    op.drop_column("admins", "modify_users_access")
    # op.alter_column('hosts', 'alpn',
    #            existing_type=sa.VARCHAR(length=11),
    #            type_=sa.String(length=32),
    #            nullable=True,
    #            existing_server_default=sa.text("'none'"))
    # op.create_foreign_key(None, 'hosts', 'inbounds', ['inbound_id'], ['id'])
    # op.alter_column('inbounds', 'protocol',
    #            existing_type=sa.VARCHAR(length=11),
    #            type_=sa.Enum('VMess', 'VLESS', 'Trojan', 'Shadowsocks', 'Shadowsocks2022', 'Hysteria2', 'WireGuard', 'TUIC', 'ShadowTLS', name='proxytypes'),
    #            existing_nullable=True)
    # op.alter_column('users', 'usage_duration',
    #            existing_type=sa.INTEGER(),
    #            type_=sa.BigInteger(),
    #            existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('users', 'usage_duration',
    #            existing_type=sa.BigInteger(),
    #            type_=sa.INTEGER(),
    #            existing_nullable=True)
    # op.alter_column('inbounds', 'protocol',
    #            existing_type=sa.Enum('VMess', 'VLESS', 'Trojan', 'Shadowsocks', 'Shadowsocks2022', 'Hysteria2', 'WireGuard', 'TUIC', 'ShadowTLS', name='proxytypes'),
    #            type_=sa.VARCHAR(length=11),
    #            existing_nullable=True)
    # op.drop_constraint(None, 'hosts', type_='foreignkey')
    # op.alter_column('hosts', 'alpn',
    #            existing_type=sa.String(length=32),
    #            type_=sa.VARCHAR(length=11),
    #            nullable=False,
    #            existing_server_default=sa.text("'none'"))
    op.add_column(
        "admins",
        sa.Column(
            "modify_users_access",
            sa.BOOLEAN(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )
    op.drop_column("admins", "revoke_users_sub_access")
    op.drop_column("admins", "toggle_users_status_access")
    op.drop_column("admins", "reset_users_usage_access")
    op.drop_column("admins", "delete_expired_users_access")
    op.drop_column("admins", "delete_users_access")
    op.drop_column("admins", "edit_users_access")
    op.drop_column("admins", "add_users_access")
    # ### end Alembic commands ###
