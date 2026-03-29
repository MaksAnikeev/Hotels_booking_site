from datetime import date

from src.api.dependencies import PaginationDep
from src.api.routers.utils import check_date_to_after_date_from
from src.schemas.hotels_schemas import (
    HotelGetSchemas,
    HotelCreateSchemas,
    HotelChangeSchemas,
)
from src.services.base_service import BaseService


class HotelService(BaseService):
    async def get_all(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
    ) -> list[HotelGetSchemas]:

        hotels = await self.db.hotels.get_all(
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
        )
        return hotels

    async def get_all_to_date(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ) -> list[HotelGetSchemas]:

        check_date_to_after_date_from(date_from, date_to)
        hotels = await self.db.hotels.get_all_to_date(
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
            date_from=date_from,
            date_to=date_to,
        )
        return hotels

    async def get_one(self, hotel_id: int) -> HotelGetSchemas:
        hotel = await self.db.hotels.get_one(id=hotel_id)
        return hotel

    async def add(self, hotel_info: HotelCreateSchemas) -> HotelGetSchemas:
        hotel = await self.db.hotels.add(hotel_info)
        return hotel

    async def edit(
        self, hotel_id: int, hotel_info: HotelCreateSchemas
    ) -> HotelGetSchemas:
        hotel = await self.db.hotels.edit(
            data=hotel_info,
            id=hotel_id,
        )
        return hotel

    async def part_edit(
        self, hotel_id: int, hotel_info: HotelChangeSchemas
    ) -> HotelGetSchemas:
        hotel = await self.db.hotels.edit(
            data=hotel_info,
            is_patch=True,
            id=hotel_id,
        )
        return hotel

    async def delete(self, hotel_id: int) -> HotelGetSchemas:
        hotel = await self.db.hotels.delete(
            id=hotel_id,
        )
        return hotel
