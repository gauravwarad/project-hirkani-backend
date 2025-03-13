"""creating posts table

Revision ID: d367f360ce2a
Revises: f633795476f4
Create Date: 2025-03-13 09:16:43.731603

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd367f360ce2a'
down_revision: Union[str, None] = 'f633795476f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('poster_id', UUID, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
        sa.Column('title', sa.String),
        sa.Column('text', sa.String),
        sa.Column('likes', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('posts')