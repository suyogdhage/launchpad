"""seeding

Revision ID: 7904e2e8787a
Revises: dc6f02d99321
Create Date: 2026-06-24 14:12:02.720771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
from config import settings
from dependencies.auth import Authentication

# revision identifiers, used by Alembic.
revision: str = '7904e2e8787a'
down_revision: Union[str, Sequence[str], None] = 'dc6f02d99321'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SUPERADMIN_ROLE_ID=str(uuid.uuid4())
NEW_HIRE_ID=str(uuid.uuid4())
HR_ID=str(uuid.uuid4())
MANAGER_ID=str(uuid.uuid4())
SUPERADMIN_ID=str(uuid.uuid4())
PASSWORD=Authentication.hash_password(settings.SUPERADMIN_PASSWORD)
def upgrade() -> None:

    op.execute(f"""
        INSERT INTO roles (id, name)
        VALUES
        ('{SUPERADMIN_ROLE_ID}', 'superadmin'),
        ('{NEW_HIRE_ID}', 'new_hire'),
        ('{HR_ID}', 'hr'),
        ('{MANAGER_ID}', 'manager'); 
    """)

    op.execute(f"""
        INSERT INTO users (id, name,email,password,role_name)
        VALUES
        ('{SUPERADMIN_ID}','suyog','suyogdhage@gmail.com','{PASSWORD}','superadmin')""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(f"""
        DELETE FROM roles 
        WHERE id IN ('{SUPERADMIN_ROLE_ID}','{NEW_HIRE_ID}', '{HR_ID}','{MANAGER_ID}');
    """)

    op.execute(f"""
        DELETE FROM users 
        WHERE id IN ('{SUPERADMIN_ID}');
    """)