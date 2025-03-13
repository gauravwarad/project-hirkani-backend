"""creating follow table

Revision ID: f633795476f4
Revises: 33d3d8f6401c
Create Date: 2025-03-08 15:26:41.676075

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f633795476f4'
down_revision: Union[str, None] = '33d3d8f6401c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'id', 
                    type_=UUID(as_uuid=True), 
                    existing_type=UUID(as_uuid=True),  # Change if the previous type was different
                    nullable=False, 
                    server_default=sa.text("gen_random_uuid()"))  # Ensure default UUID generation
    op.create_primary_key("user_pkey", "user", ["id"])
    op.create_table(
        'follows',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('follower_id', UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete="CASCADE"), nullable=False),
        sa.Column('following_id', UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete="CASCADE"), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('follows')
