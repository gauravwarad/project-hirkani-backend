"""add rating & business id to posts table

Revision ID: 9fba5cf78c8f
Revises: 78fdb575ab88
Create Date: 2025-03-19 12:33:24.632891

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.types import UUID
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fba5cf78c8f'
down_revision: Union[str, None] = '78fdb575ab88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('rating', sa.Float))
    op.add_column('posts', sa.Column('business_id', UUID, ForeignKey("business.id", ondelete="CASCADE"), nullable=True))
def downgrade() -> None:
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'business_id')
