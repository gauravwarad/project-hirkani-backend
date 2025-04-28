"""add follow requests

Revision ID: 63ab1f8cff36
Revises: 4e840e11bc8b
Create Date: 2025-04-26 18:03:16.469719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63ab1f8cff36'
down_revision: Union[str, None] = '4e840e11bc8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # class FollowRequests(Base):
    # __tablename__ = "follow_requests"

    # id = Column(Integer, primary_key=True, index=True)
    # sender_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    # receiver_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    # created_at = Column(DateTime, default=func.now())

    op.create_table(
        "follow_requests",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("sender_id", sa.UUID, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        sa.Column("receiver_id", sa.UUID, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("follow_requests")
