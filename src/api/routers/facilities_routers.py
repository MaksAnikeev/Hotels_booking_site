from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    AlreadyExistedException,
    FacilitiesAlreadyExistedHTTPException,
)
from src.schemas.facilities_schemas import (
    FacilitiesCreateSchemas,
    example_add_facilities,
)
from src.services.facilities_service import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все доступные удобства")
@cache(20)
async def get_facilities(
    db: DBDep,
):
    facilities = await FacilitiesService(db).get_all()
    return {"status": "success", "data": facilities, "detail": None}


@router.post("", summary="Создать удобство")
async def add_facilities(
    db: DBDep,
    facilities_info: FacilitiesCreateSchemas = Body(
        openapi_examples=example_add_facilities
    ),
):
    try:
        facility = await FacilitiesService(db).add(facilities_info)
    except AlreadyExistedException:
        raise FacilitiesAlreadyExistedHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Удобство с названием {facility.title} успешно добавлено.",
        "facility_info": facility,
    }
