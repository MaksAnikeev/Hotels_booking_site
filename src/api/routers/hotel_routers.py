from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import (
    ObjectNotFoundException,
    TooLongParameterException,
    TooManyObjectsException,
    NotAllowedParameterException,
    AlreadyExistedException,
    HotelNotFoundHTTPException,
    HotelAlreadyExistedHTTPException,
    TooLongParameterHTTPException,
    TooManyObjectsHTTPException,
    NotAllowedParameterHTTPException,
)

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels_schemas import (
    HotelCreateSchemas,
    HotelChangeSchemas,
    example_add_hotel,
    example_change_hotel,
)
from src.services.hotel_service import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить данные по всем существующим отелям")
@cache(20)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="название отеля"),
    location: str | None = Query(None, description="адрес отеля"),
):
    hotels = await HotelService(db).get_all(
        pagination=pagination,
        title=title,
        location=location,
    )

    return hotels


@router.get(
    "/free", summary="Получить данные по отелям, в которых есть свободные номера"
)
async def get_free_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="название отеля"),
    location: str | None = Query(None, description="адрес отеля"),
    date_from: date = Query(date(2026, 1, 25), description="Дата заезда"),
    date_to: date = Query(date(2026, 1, 30), description="Дата выезда"),
):

    hotels = await HotelService(db).get_all_to_date(
        pagination=pagination,
        title=title,
        location=location,
        date_from=date_from,
        date_to=date_to,
    )

    return hotels


@router.get("/{hotel_id}", summary="Получить данные по одному отелю")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        hotel = await HotelService(db).get_one(hotel_id=hotel_id)

    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except TooLongParameterException:
        raise TooLongParameterHTTPException
    except TooManyObjectsException:
        raise TooManyObjectsHTTPException

    return hotel


@router.post("/hotel", summary="Добавить отель в БД")
async def add_hotel(
    db: DBDep,
    hotel_info: HotelCreateSchemas = Body(openapi_examples=example_add_hotel),
):
    try:
        hotel = await HotelService(db).add(hotel_info)
    except AlreadyExistedException:
        raise HotelAlreadyExistedHTTPException
    await db.commit()
    return {
        "status": "OK",
        "description": f"Отель с названием {hotel.title} успешно добавлен",
        "hotel_info": hotel,
    }


@router.put("/{hotel_id}", summary="Изменить данные по отелю")
async def change_hotel(
    hotel_id: int,
    db: DBDep,
    hotel_info: HotelCreateSchemas = Body(openapi_examples=example_add_hotel),
) -> dict:

    try:
        hotel = await HotelService(db).edit(
            hotel_id=hotel_id,
            hotel_info=hotel_info,
        )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except TooLongParameterException:
        raise TooLongParameterHTTPException
    except TooManyObjectsException:
        raise TooManyObjectsHTTPException
    except NotAllowedParameterException:
        raise NotAllowedParameterHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Отель с ид {hotel.id} успешно изменен.",
        "new_hotel_info": hotel,
    }


@router.patch("/hotel/{hotel_id}", summary="Частично изменить данные по отелю")
async def part_change_hotel(
    hotel_id: int,
    db: DBDep,
    hotel_info: HotelChangeSchemas = Body(openapi_examples=example_change_hotel),
) -> dict:
    try:
        hotel = await HotelService(db).part_edit(
            hotel_id=hotel_id,
            hotel_info=hotel_info,
        )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except TooLongParameterException:
        raise TooLongParameterHTTPException
    except TooManyObjectsException:
        raise TooManyObjectsHTTPException
    except NotAllowedParameterException:
        raise NotAllowedParameterHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Отель с ид {hotel.id} успешно изменен.",
        "new_hotel_info": hotel,
    }


@router.delete("/{hotel_id}", summary="Удалить отель по ИД")
async def del_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        hotel = await HotelService(db).delete(
            hotel_id=hotel_id,
        )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except TooLongParameterException:
        raise TooLongParameterHTTPException
    except TooManyObjectsException:
        raise TooManyObjectsHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Отель с ид {hotel.id} удален.",
        "delete_hotel_info": hotel,
    }
