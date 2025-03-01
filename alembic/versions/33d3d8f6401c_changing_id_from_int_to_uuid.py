"""changing id from int to uuid

Revision ID: 33d3d8f6401c
Revises: 0ed813484302
Create Date: 2025-02-28 15:44:37.945680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision: str = '33d3d8f6401c'
down_revision: Union[str, None] = '0ed813484302'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("user", "id")
    op.add_column(
        "user",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
    )


def downgrade() -> None:
    op.drop_column("user", "id")
    
    op.add_column(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    )
