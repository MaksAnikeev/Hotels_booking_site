from pydantic import BaseModel, Field

from src.schemas.facilities_schemas import FacilitiesGetSchemas


class RoomRequestSchemas(BaseModel):
    title: str = Field(..., description="Короткое название номера")
    description: str | None = Field(None, description="Описание номера")
    price: int = Field(..., ge=1, description="Стоимость номера за сутки")
    quantity: int = Field(
        ..., ge=1, le=1000, description="Количество номеров данного типа"
    )
    facilities_ids: list[int] = Field([], description="Список ид удобств")


example_add_room = {
    "1": {
        "summary": "Стандарт",
        "value": {
            "title": "Standard",
            "description": "Обычный двухместный номер",
            "price": 3500,
            "quantity": 50,
            "facilities_ids": [1, 2],
        },
    },
    "2": {
        "summary": "Полулюкс",
        "value": {
            "title": "1/2 Lux",
            "description": "Двухместный номер с большой кроватью",
            "price": 4500,
            "quantity": 20,
        },
    },
    "3": {
        "summary": "Не все параметры",
        "value": {
            "description": "Двухместный номер с большой кроватью",
            "price": 4500,
        },
    },
}


class RoomCreateSchemas(BaseModel):
    hotel_id: int = Field(..., description="ИД отеля")
    title: str = Field(..., description="Короткое название номера")
    description: str | None = Field(None, description="Описание номера")
    price: int = Field(..., ge=1, description="Стоимость номера за сутки")
    quantity: int = Field(
        ..., ge=1, le=1000, description="Количество номеров данного типа"
    )


class RoomGetSchemas(RoomCreateSchemas):
    id: int = Field(..., description="ИД номера")


class RoomFacilitiesGetSchemas(RoomGetSchemas):
    facilities: list[FacilitiesGetSchemas] = Field(..., description="список удобств")

    model_config = {"from_attributes": True}


class FreeRoomGetSchemas(RoomCreateSchemas):
    free_rooms: int | None = Field(
        None, description="Количество свободных номеров этого типа на период"
    )
    id: int = Field(..., description="ИД номера")
    facilities: list[FacilitiesGetSchemas] = Field(..., description="список удобств")

    model_config = {"from_attributes": True}


class RoomChangeSchemas(BaseModel):
    hotel_id: int | None = Field(None, description="Новое ИД отеля")
    title: str | None = Field(None, description="Новое короткое название номера")
    description: str | None = Field(None, description="Описание номера")
    price: int | None = Field(None, ge=1, description="Стоимость номера за сутки")
    quantity: int | None = Field(
        None, ge=1, le=1000, description="Количество номеров данного типа"
    )


class RoomChangeRequestSchemas(BaseModel):
    title: str | None = Field(None, description="Новое короткое название номера")
    description: str | None = Field(None, description="Описание номера")
    price: int | None = Field(None, ge=1, description="Стоимость номера за сутки")
    quantity: int | None = Field(
        None, ge=1, le=1000, description="Количество номеров данного типа"
    )
    facilities_ids: list[int] | None = Field(None, description="Список ид удобств")


example_change_room = {
    "1": {
        "summary": "Стандарт+",
        "value": {
            "title": "Standard+",
            "price": 3900,
        },
    },
    "2": {
        "summary": "Люкс",
        "value": {
            "title": "Lux",
            "description": "Трехместный номер с большой кроватью и видом на море",
            "price": 9500,
            "quantity": 5,
        },
    },
    "3": {
        "summary": "Удобства",
        "value": {
            "facilities_ids": [1, 3],
        },
    },
    "4": {"summary": "Неверные параметры", "value": {"quantity": -5, "price": "много"}},
}
