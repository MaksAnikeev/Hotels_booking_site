from datetime import date

from fastapi import HTTPException, APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.api.routers.utils import check_date_to_after_date_from
from src.exceptions import ObjectNotFoundException, TooLongParameterException, HotelNotFoundHTTPException, \
    HotelOrRoomNotFoundHTTPException
from src.schemas.facilities_schemas import RoomFacilitiesCreateSchemas
from src.schemas.rooms_schemas import (
    RoomCreateSchemas,
    example_add_room,
    RoomChangeSchemas,
    example_change_room,
    RoomRequestSchemas,
    RoomChangeRequestSchemas,
    RoomGetSchemas,
)

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить номера в отеле")
async def get_rooms(hotel_id: int, db: DBDep):
    rooms = await db.rooms.get_all_with_parameters(hotel_id=hotel_id)
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
    check_date_to_after_date_from(date_from, date_to)

    try:
        rooms = await db.rooms.get_rooms_to_date(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "success", "rooms": rooms, "details": None}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить данные по номеру")
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        room = await db.rooms.get_one_or_none_with_relship(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelOrRoomNotFoundHTTPException
    return {"status": "success", "room": room, "detail": None}


@router.post("/{hotel_id}/room", summary="Добавить номер в БД")
async def add_room(
    hotel_id: int,
    db: DBDep,
    room_info: RoomRequestSchemas = Body(openapi_examples=example_add_room),
):
    _room_info = RoomCreateSchemas(hotel_id=hotel_id, **room_info.model_dump())
    try:
        room: RoomGetSchemas = await db.rooms.add(_room_info)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Отель с таким ид не найден"
        )
    room_facilities = [
        RoomFacilitiesCreateSchemas(room_id=room.id, facility_id=f_id)
        for f_id in room_info.facilities_ids
    ]
    try:
        await db.room_facilities.add_bulk(room_facilities)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Указаны не существующие удобства"
        )

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
    _room_info = RoomCreateSchemas(hotel_id=hotel_id, **room_info.model_dump())
    try:
        room = await db.rooms.edit(
            data=_room_info,
            id=room_id,
        )
    except ObjectNotFoundException:
        raise HotelOrRoomNotFoundHTTPException
    except TooLongParameterException as ex:
        raise HTTPException(400, detail=ex.detail)
    try:
        await db.room_facilities.set_room_facilities(
            room_id=room.id,
            facilities_ids=room_info.facilities_ids,
        )
    except ObjectNotFoundException:
        raise HTTPException(404, 'Указаны не существующие удобства')

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
    room_info_dict = room_info.model_dump(exclude_unset=True)
    _room_info = RoomChangeSchemas(hotel_id=hotel_id, **room_info_dict)
    try:
        room = await db.rooms.edit(data=_room_info, id=room_id, hotel_id=hotel_id)

    except ObjectNotFoundException:
        raise HotelOrRoomNotFoundHTTPException
    except TooLongParameterException as ex:
        raise HTTPException(400, detail=ex.detail)


    if "facilities_ids" in room_info_dict:
        try:
            await db.room_facilities.set_room_facilities(
                room_id=room.id,
                facilities_ids=room_info_dict["facilities_ids"],
            )
        except ObjectNotFoundException:
            raise HTTPException(404, 'Указаны не существующие удобства')

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
        room = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelOrRoomNotFoundHTTPException
    except TooLongParameterException as ex:
        raise HTTPException(400, detail=ex.detail)
    await db.commit()
    return {
        "status": "OK",
        "description": f"Номер с ид {room.id} удален.",
        "delete_room_info": room,
    }
