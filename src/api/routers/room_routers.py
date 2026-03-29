from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    TooLongParameterException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    FacilitiesNotFoundException,
    FacilitiesNotFoundHTTPException,
    TooLongParameterHTTPException,
)
from src.schemas.rooms_schemas import (
    example_add_room,
    example_change_room,
    RoomRequestSchemas,
    RoomChangeRequestSchemas,
    RoomGetSchemas,
)
from src.services.room_service import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить номера в отеле")
async def get_rooms(hotel_id: int, db: DBDep):
    try:
        rooms = await RoomService(db).get_all_with_parameters(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "success", "rooms": rooms, "details": None}


@router.get(
    "/{hotel_id}/free_rooms",
    summary="Получить свободные номера в отеле в указанный период",
)
async def get_free_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(date(2026, 1, 25), description="Дата заезда"),
    date_to: date = Query(date(2026, 1, 30), description="Дата выезда"),
):
    try:
        rooms = await RoomService(db).get_rooms_to_date(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "success", "rooms": rooms, "details": None}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить данные по номеру")
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        room = await RoomService(db).get_one_or_none_with_relship(
            hotel_id=hotel_id,
            room_id=room_id,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "success", "room": room, "detail": None}


@router.post("/{hotel_id}/room", summary="Добавить номер в БД")
async def add_room(
    hotel_id: int,
    db: DBDep,
    room_info: RoomRequestSchemas = Body(openapi_examples=example_add_room),
):
    try:
        room: RoomGetSchemas = await RoomService(db).add(
            hotel_id=hotel_id, room_info=room_info
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilitiesNotFoundException:
        raise FacilitiesNotFoundHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с названием {room.title} успешно добавлен в отель с ид {room.hotel_id}.",
        "room_info": room,
    }


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить данные по номеру")
async def change_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_info: RoomRequestSchemas = Body(openapi_examples=example_add_room),
) -> dict:
    try:
        room = await RoomService(db).edit(
            hotel_id=hotel_id, room_id=room_id, room_info=room_info
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilitiesNotFoundException:
        raise FacilitiesNotFoundHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с ид {room.id} успешно изменен.",
        "new_room_info": room,
    }


@router.patch(
    "/{hotel_id}/rooms/room/{room_id}", summary="Частично изменить данные по номеру"
)
async def part_change_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_info: RoomChangeRequestSchemas = Body(openapi_examples=example_change_room),
) -> dict:

    try:
        room = await RoomService(db).part_edit(
            hotel_id=hotel_id, room_id=room_id, room_info=room_info
        )

    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilitiesNotFoundException:
        raise FacilitiesNotFoundHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с ид {room.id} успешно изменен.",
        "new_room_info": room,
    }


@router.delete("/{hotel_id}/room/{room_id}", summary="Удалить номер по ИД")
async def del_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        room = await RoomService(db).delete(hotel_id=hotel_id, room_id=room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilitiesNotFoundException:
        raise FacilitiesNotFoundHTTPException
    except TooLongParameterException:
        raise TooLongParameterHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с ид {room.id} удален.",
        "delete_room_info": room,
    }
