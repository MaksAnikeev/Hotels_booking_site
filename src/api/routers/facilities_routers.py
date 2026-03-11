from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities_schemas import (
    FacilitiesCreateSchemas,
    example_add_facilities,
)

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получить все доступные удобства")
@cache(20)
async def get_facilities(
    db: DBDep,
):
    facilities = await db.facilities.get_all()
    return {"status": "success", "data": facilities, "detail": None}


@router.post("/", summary="Создать удобство")
async def add_facilities(
    db: DBDep,
    facilities_info: FacilitiesCreateSchemas = Body(
        openapi_examples=example_add_facilities
    ),
):
    facilities = await db.facilities.add(facilities_info)
    await db.commit()
    return {
        "status": "OK",
        "description": f"Удобство с названием {facilities.title} успешно добавлено.",
        "room_info": facilities,
    }
