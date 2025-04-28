"""adding business_follow and business_posts tables

Revision ID: f3cd7940684b
Revises: 649ecbe28149
Create Date: 2025-04-27 12:45:08.278264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3cd7940684b'
down_revision: Union[str, None] = '649ecbe28149'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

# class BusinessFollow(Base):
#     __tablename__ = "business_follow"
#     id = Column(Integer, primary_key=True, index=True)
#     business_id = Column(UUID, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
#     follower_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
#     created_at = Column(DateTime, default=func.now())

# class BusinessPost(Base):
#     __tablename__ = "business_post"
#     id = Column(Integer, primary_key=True, index=True)
#     business_id = Column(UUID, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
#     title = Column(String)
#     content = Column(String)
#     created_at = Column(DateTime, default=func.now())
    op.create_table(
        'business_follow',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('business_id', sa.UUID(), sa.ForeignKey("business.id", ondelete="CASCADE"), nullable=False),
        sa.Column("follower_id", sa.UUID, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )
    op.create_table(
        'business_post',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('business_id', sa.UUID(), sa.ForeignKey("business.id", ondelete="CASCADE"), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('business_post')
    op.drop_table('business_follow')
