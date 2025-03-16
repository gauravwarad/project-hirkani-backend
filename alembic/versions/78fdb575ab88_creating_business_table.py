"""creating business table

Revision ID: 78fdb575ab88
Revises: d367f360ce2a
Create Date: 2025-03-16 15:22:16.898153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '78fdb575ab88'
down_revision: Union[str, None] = 'd367f360ce2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "business",
        sa.Column("id", UUID, primary_key=True, index=True),
        sa.Column("google_id", sa.String),
        sa.Column("handler_id", UUID, sa.ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now())
    )



def downgrade() -> None:
    op.drop_table("business")
