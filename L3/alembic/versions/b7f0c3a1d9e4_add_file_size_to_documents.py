"""add_file_size_to_documents

Revision ID: b7f0c3a1d9e4
Revises: adcad0c9b527
Create Date: 2026-08-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b7f0c3a1d9e4'
down_revision: Union[str, Sequence[str], None] = 'adcad0c9b527'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('documents', sa.Column('file_size', sa.BigInteger(), nullable=True))


def downgrade() -> None:
    op.drop_column('documents', 'file_size')
