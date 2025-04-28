"""adding followers count to business

Revision ID: d1697403af7e
Revises: f3cd7940684b
Create Date: 2025-04-27 13:10:10.368772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1697403af7e'
down_revision: Union[str, None] = 'f3cd7940684b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # followers_count = Column(Integer, default=0)
    op.add_column('business', sa.Column('followers_count', sa.Integer(), nullable=True))
    # Set default value to 0 for existing records
    op.execute("UPDATE business SET followers_count = 0")

def downgrade() -> None:
    # Remove the followers_count column
    op.drop_column('business', 'followers_count')