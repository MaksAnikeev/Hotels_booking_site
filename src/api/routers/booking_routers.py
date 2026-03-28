from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep, UserIDDep
from src.exceptions import (
    AllRoomIsBookedException,
    NotAllNecessaryParamsException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    NotBookingDateHTTPException,
    AllRoomIsBookedExceptionHTTPException,
)

from src.schemas.booking_shemas import (
    BookingRequestSchemas,
    example_add_booking,
)
from src.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me", summary="Получить данные по моим бронированиям")
async def get_my_booking(
    user_id: UserIDDep,
    db: DBDep,
    date_from: date | None = Query(
        date(2026, 1, 31), description="Дата заезда, с которой показать бронирования"
    ),
):
    bookings = await BookingService(db).get_all_with_any_parameters(
        user_id=user_id, date_from=date_from
    )
    return {"status": "success", "data": bookings, "detail": None}


@router.get("/{room_id}", summary="Получить данные бронирования по номеру")
async def get_room_booking(
    db: DBDep,
    room_id: int,
    date_from: date = Query(date(2026, 1, 31), description="Дата заезда"),
    date_to: date = Query(date(2026, 2, 2), description="Дата выезда"),
):
    try:
        booking, quantity_booked_rooms, quantity_free_rooms = await BookingService(
            db
        ).get_booking_to_date(room_id=room_id, date_from=date_from, date_to=date_to)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NotAllNecessaryParamsException:
        raise NotBookingDateHTTPException
    return {
        "status": "success",
        "data": booking,
        "detail": {
            "quantity_booked_rooms": quantity_booked_rooms,
            "quantity_free_rooms": quantity_free_rooms,
        },
    }


@router.post("", summary="Создать бронирование")
async def add_booking(
    user_id: UserIDDep,
    db: DBDep,
    booking_info: BookingRequestSchemas = Body(openapi_examples=example_add_booking),
):
    try:
        booking, room = await BookingService(db).add_booking(
            user_id=user_id, booking_info=booking_info
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomIsBookedException:
        raise AllRoomIsBookedExceptionHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с названием {room.title} в отеле {room.hotel_id} успешно забронирован.",
        "room_info": booking,
    }
