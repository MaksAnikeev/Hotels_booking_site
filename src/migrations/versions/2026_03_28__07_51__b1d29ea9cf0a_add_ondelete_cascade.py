"""Add ondelete cascade

Revision ID: b1d29ea9cf0a
Revises: 87080ad390e5
Create Date: 2026-03-28 07:51:24.569934

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b1d29ea9cf0a"
down_revision: Union[str, Sequence[str], None] = "87080ad390e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f("booking_user_id_fkey"), "booking", type_="foreignkey")
    op.drop_constraint(op.f("booking_room_id_fkey"), "booking", type_="foreignkey")
    op.create_foreign_key(
        None, "booking", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "booking", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint(op.f("rooms_hotel_id_fkey"), "rooms", type_="foreignkey")
    op.create_foreign_key(
        None, "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "rooms", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_hotel_id_fkey"), "rooms", "hotels", ["hotel_id"], ["id"]
    )
    op.drop_constraint(None, "booking", type_="foreignkey")
    op.drop_constraint(None, "booking", type_="foreignkey")
    op.create_foreign_key(
        op.f("booking_room_id_fkey"), "booking", "rooms", ["room_id"], ["id"]
    )
    op.create_foreign_key(
        op.f("booking_user_id_fkey"), "booking", "users", ["user_id"], ["id"]
    )
