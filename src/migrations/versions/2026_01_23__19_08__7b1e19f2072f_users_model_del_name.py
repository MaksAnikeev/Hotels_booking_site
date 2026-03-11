"""Users model del name

Revision ID: 7b1e19f2072f
Revises: fe35850e8602
Create Date: 2026-01-23 19:08:57.430728

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b1e19f2072f"
down_revision: Union[str, Sequence[str], None] = "fe35850e8602"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("users", "name")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
