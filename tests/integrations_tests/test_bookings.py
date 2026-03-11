# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false

from datetime import date

import pytest
from fastapi import HTTPException

from src.schemas.booking_shemas import BookingCreateSchemas, BookingChangeSchemas
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingCreateSchemas(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2026, month=1, day=25),
        date_to=date(year=2026, month=2, day=10),
        price=1000,
    )
    new_booking = await db.booking.add(booking_data)
    assert (
        new_booking.total_cost
        == booking_data.price * (booking_data.date_to - booking_data.date_from).days
    )

    existing_booking = await db.booking.get_one_or_none(id=new_booking.id)
    assert existing_booking

    data_for_edit = BookingChangeSchemas(
        price=2000, date_to=date(year=2026, month=2, day=14) # type: ignore[attr-defined,operator]
    )
    edit_booking = await db.booking.edit(data=data_for_edit, id=existing_booking.id)
    assert edit_booking.price == data_for_edit.price
    assert edit_booking.date_to == date(year=2026, month=2, day=14)
    assert (
        edit_booking.total_cost
        == data_for_edit.price * (data_for_edit.date_to - booking_data.date_from).days     # type: ignore[attr-defined,operator]
    )

    await db.booking.delete(id=existing_booking.id)
    with pytest.raises(HTTPException) as exc_info:
        await db.booking.get_one_or_none(id=existing_booking.id)
    assert exc_info.value.status_code == 404
    assert "Объект с такими параметрами не найден" in exc_info.value.detail
