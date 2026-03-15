"""RoomFacilitiesORM add ondelete cascade

Revision ID: 87080ad390e5
Revises: 1660b327200b
Create Date: 2026-03-15 11:25:25.044139

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "87080ad390e5"
down_revision: Union[str, Sequence[str], None] = "1660b327200b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("rooms_facilities_room_id_fkey"), "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "rooms_facilities", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_facilities_room_id_fkey"),
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
    )
