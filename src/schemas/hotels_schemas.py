from pydantic import BaseModel, Field


class HotelCreateSchemas(BaseModel):
    title: str = Field(..., description="Короткое название отеля")
    location: str = Field(..., description="Адрес отеля")
    description: str | None = Field(None, description="Описание отеля")


example_add_hotel = {
    "1": {
        "summary": "Эмир",
        "value": {
            "title": "Resort spa Emir",
            "location": "Около ТаджМахала",
            "description": "Крутой отель в Египте",
        },
    },
    "2": {
        "summary": "Сочи",
        "value": {"title": "Sochy curort spa", "location": "в центре Сочи"},
    },
}


class HotelGetSchemas(HotelCreateSchemas):
    id: int = Field(..., description="ИД отеля")


class HotelChangeSchemas(BaseModel):
    title: str | None = Field(None, description="Новое короткое название")
    location: str | None = Field(None, description="Адрес отеля")
    description: str | None = Field(None, description="Новое описание")


example_change_hotel = {
    "1": {"summary": "Эмир", "value": {"description": "Крутой отель в Египте"}},
    "2": {
        "summary": "Сочи",
        "value": {"title": "Sochi curort spa", "location": "у чера на куличках"},
    },
    "3": {
        "summary": "Сочи2",
        "value": {
            "title": "New Sochi hotel",
        },
    },
}


class PaginationParamsSchemas(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы")
    per_page: int = Field(
        20, ge=1, le=100, description="количество объектов на странице"
    )
