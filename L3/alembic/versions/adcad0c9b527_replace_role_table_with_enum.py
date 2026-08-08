"""replace_role_table_with_enum

Revision ID: adcad0c9b527
Revises: dec1f247088f
Create Date: 2026-07-25 23:40:52.813247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'adcad0c9b527'
down_revision: Union[str, Sequence[str], None] = 'dec1f247088f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('users_role_name_fkey', 'users', type_='foreignkey')
    sa.Enum('superadmin', 'hr', 'manager', 'new_hire', name='userrole').create(op.get_bind())
    op.alter_column('users', 'role_name',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('superadmin', 'hr', 'manager', 'new_hire', name='userrole', create_type=False),
               postgresql_using='role_name::userrole',
               existing_nullable=False,
               server_default=sa.text("'new_hire'::userrole"))
    op.drop_table('roles')


def downgrade() -> None:
    op.create_table('roles',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='roles_name_key')
    )
    op.execute("INSERT INTO roles (id, name) VALUES (gen_random_uuid(), 'superadmin'), (gen_random_uuid(), 'hr'), (gen_random_uuid(), 'manager'), (gen_random_uuid(), 'new_hire')")
    op.alter_column('users', 'role_name',
               existing_type=sa.Enum('superadmin', 'hr', 'manager', 'new_hire', name='userrole', create_type=False),
               type_=sa.VARCHAR(),
               postgresql_using='role_name::varchar',
               existing_nullable=False,
               server_default=None)
    op.create_foreign_key('users_role_name_fkey', 'users', 'roles', ['role_name'], ['name'])
    op.execute("DROP TYPE IF EXISTS userrole")
