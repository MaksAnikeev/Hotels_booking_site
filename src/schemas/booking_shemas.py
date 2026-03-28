from datetime import datetime, date

from pydantic import BaseModel, Field

from src.schemas.base_schema import ChangeBaseSchema


class BookingRequestSchemas(ChangeBaseSchema):
    room_id: int = Field(..., description="ИД номера")
    date_from: date = Field(..., description="Дата заезда")
    date_to: date = Field(..., description="Дата выезда")


example_add_booking = {
    "1": {
        "summary": "Правильный",
        "value": {
            "room_id": 13,
            "date_from": "2026-01-30",
            "date_to": "2026-02-02",
        },
    },
    "2": {
        "summary": "Даты ошибочны",
        "value": {
            "room_id": 13,
            "date_from": "2026-02-28",
            "date_to": "2026-02-02",
        },
    },
    "3": {
        "summary": "Неполная ин-фа",
        "value": {
            "room_id": 130,
            "date_to": "2026-02-02",
        },
    },
}


class BookingCreateSchemas(BaseModel):
    room_id: int = Field(..., description="ИД номера")
    user_id: int = Field(..., description="ИД клиента")
    date_from: date = Field(..., description="Дата заезда")
    date_to: date = Field(..., description="Дата выезда")
    price: int = Field(..., ge=1, description="Стоимость номера за сутки")


class BookingGetSchemas(BookingCreateSchemas):
    id: int = Field(..., description="ИД номера")
    total_cost: int = Field(
        ..., ge=1, description="Полная стоимость номера за время бронирования"
    )
    created_at: datetime = Field(..., description="Дата регистрации бронирования")


class BookingChangeSchemas(ChangeBaseSchema):
    date_from: date | None = Field(None, description="Дата заезда")
    date_to: date | None = Field(None, description="Дата выезда")
    price: int | None = Field(None, ge=1, description="Стоимость номера за сутки")
