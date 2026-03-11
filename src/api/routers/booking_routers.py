from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.api.dependencies import DBDep, UserIDDep
from src.models.booking import BookingORM
from src.schemas.booking_shemas import (
    BookingRequestSchemas,
    example_add_booking,
    BookingCreateSchemas,
    BookingGetSchemas,
)
from src.schemas.rooms_schemas import RoomGetSchemas

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me", summary="Получить данные по моим бронированиям")
async def get_my_booking(
    user_id: UserIDDep,
    db: DBDep,
    date_from: date | None = Query(
        date(2026, 1, 31), description="Дата заезда, с которой показать бронирования"
    ),
):
    if date_from:
        bookings = await db.booking.get_all_with_any_parameters(
            BookingORM.date_from >= date_from, user_id=user_id
        )
    else:
        bookings = await db.booking.get_all_with_parameters(user_id=user_id)
    return {"status": "success", "data": bookings, "detail": None}


@router.get("/{room_id}", summary="Получить данные бронирования по номеру")
async def get_room_booking(
    db: DBDep,
    room_id: int,
    date_from: date = Query(date(2026, 1, 31), description="Дата заезда"),
    date_to: date = Query(date(2026, 2, 2), description="Дата выезда"),
):
    booking = await db.booking.get_booking_to_date(
        room_id=room_id, date_from=date_from, date_to=date_to
    )
    quantity_booked_rooms = len(booking)
    room: RoomGetSchemas | None = await db.rooms.get_one_or_none(id=room_id)
    quantity_rooms = room.quantity
    quantity_free_rooms = quantity_rooms - quantity_booked_rooms
    return {
        "status": "success",
        "data": booking,
        "detail": {
            "quantity_booked_rooms": quantity_booked_rooms,
            "quantity_free_rooms": quantity_free_rooms,
        },
    }


@router.post("/", summary="Создать бронирование")
async def add_booking(
    user_id: UserIDDep,
    db: DBDep,
    booking_info: BookingRequestSchemas = Body(openapi_examples=example_add_booking),
):
    if booking_info.date_from > booking_info.date_to:
        raise HTTPException(status_code=400, detail="Дата выезда раньше даты заезда")
    room: RoomGetSchemas | None = await db.rooms.get_one_or_none(id=booking_info.room_id)
    _booking_info = BookingCreateSchemas(
        user_id=user_id, price=room.price, **booking_info.model_dump()
    )
    booking: BookingGetSchemas | None = await db.booking.add_booking(_booking_info, hotel_id=room.hotel_id)
    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с названием {room.title} в отеле {room.hotel_id} успешно забронирован.",
        "room_info": booking,
    }
