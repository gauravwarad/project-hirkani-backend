"""adding name and address to business

Revision ID: 4e840e11bc8b
Revises: 11fba9f00dfa
Create Date: 2025-04-07 11:43:20.905183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e840e11bc8b'
down_revision: Union[str, None] = '11fba9f00dfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("business", sa.Column("name", sa.String(), nullable=True))
    op.add_column("business", sa.Column("address", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("business", "address")
    op.drop_column("business", "name")