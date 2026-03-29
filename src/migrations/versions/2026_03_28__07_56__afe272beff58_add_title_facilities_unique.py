"""Add title facilities unique

Revision ID: afe272beff58
Revises: b1d29ea9cf0a
Create Date: 2026-03-28 07:56:14.280842

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "afe272beff58"
down_revision: Union[str, Sequence[str], None] = "b1d29ea9cf0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(op.f("ix_facilities_title"), "facilities", ["title"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_facilities_title"), table_name="facilities")
