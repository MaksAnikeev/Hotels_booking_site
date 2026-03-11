from pydantic import BaseModel, Field


class FacilitiesCreateSchemas(BaseModel):
    title: str = Field(..., description="Удобства в номере")


example_add_facilities = {
    "1": {
        "summary": "Кондей",
        "value": {
            "title": "кондиционер",
        },
    },
    "2": {
        "summary": "Холодильник",
        "value": {
            "title": "холодильник",
        },
    },
}


class FacilitiesGetSchemas(FacilitiesCreateSchemas):
    id: int = Field(..., description="ИД удобства")

    model_config = {"from_attributes": True}


class RoomFacilitiesCreateSchemas(BaseModel):
    room_id: int = Field(..., description="ИД номера")
    facility_id: int = Field(..., description="ИД удобства")


class RoomFacilitiesGetSchemas(RoomFacilitiesCreateSchemas):
    id: int
