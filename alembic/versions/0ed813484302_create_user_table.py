"""Create user table

Revision ID: 0ed813484302
Revises: 
Create Date: 2025-02-20 14:08:14.023166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ed813484302'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(length=64), nullable=False, unique=True),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column("is_superuser", sa.Boolean, nullable=False, default=False),
        sa.Column("is_verified", sa.Boolean, nullable=False, default=False),
    )



def downgrade() -> None:
    op.drop_table("user")
