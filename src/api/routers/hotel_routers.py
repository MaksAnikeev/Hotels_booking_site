from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels_schemas import (
    HotelCreateSchemas,
    HotelChangeSchemas,
    example_add_hotel,
    example_change_hotel,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получить данные по всем существующим отелям")
@cache(20)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="название отеля"),
    location: str | None = Query(None, description="адрес отеля"),
):
    hotels = await db.hotels.get_all(
        title=title,
        location=location,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )

    return {"status": "success", "data": hotels, "details": None}


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

    hotels = await db.hotels.get_all_to_date(
        title=title,
        location=location,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
        date_from=date_from,
        date_to=date_to,
    )

    return {"status": "success", "data": hotels, "details": None}


@router.get("/{hotel_id}", summary="Получить данные по одному отелю")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return {"status": "success", "data": hotel, "detail": None}


@router.post("/hotel", summary="Добавить отель в БД")
async def add_hotel(
    db: DBDep,
    hotel_info: HotelCreateSchemas = Body(openapi_examples=example_add_hotel),
):
    hotel = await db.hotels.add(hotel_info)
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
    hotel = await db.hotels.edit(
        data=hotel_info,
        id=hotel_id,
    )
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
    hotel = await db.hotels.edit(
        data=hotel_info,
        is_patch=True,
        id=hotel_id,
    )
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
    hotel = await db.hotels.delete(
        id=hotel_id,
    )
    await db.commit()
    return {
        "status": "OK",
        "description": f"Отель с ид {hotel.id} удален.",
        "delete_hotel_info": hotel,
    }
