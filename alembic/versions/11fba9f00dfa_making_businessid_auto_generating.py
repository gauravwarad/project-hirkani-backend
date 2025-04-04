"""making businessid auto generating

Revision ID: 11fba9f00dfa
Revises: 9fba5cf78c8f
Create Date: 2025-04-03 19:55:35.277944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '11fba9f00dfa'
down_revision: Union[str, None] = '9fba5cf78c8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # Add default generation to the 'id' column
    op.alter_column(
        'business',
        'id',
        server_default=sa.text('uuid_generate_v4()'),
        existing_type=postgresql.UUID(),
        existing_nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'business',
        'id',
        server_default=None,
        existing_type=postgresql.UUID(),
        existing_nullable=False
    )
