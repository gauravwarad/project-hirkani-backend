"""add likes table

Revision ID: 649ecbe28149
Revises: 63ab1f8cff36
Create Date: 2025-04-27 06:15:54.794607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '649ecbe28149'
down_revision: Union[str, None] = '63ab1f8cff36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the likes table
    op.create_table(
        "likes",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

def downgrade() -> None:
    # Drop the likes table
    op.drop_table("likes")
