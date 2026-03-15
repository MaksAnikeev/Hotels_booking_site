from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundException
from src.models import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import (
    get_query_rooms_to_date,
    get_query_all_rooms_to_date,
    check_safe_filters,
)
from src.schemas.rooms_schemas import FreeRoomGetSchemas, RoomFacilitiesGetSchemas


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_rooms_to_date(self, date_from, date_to, hotel_id):
        query = select(HotelsORM).filter_by(id=hotel_id)
        query_result = await self.session.execute(query)
        result = query_result.scalars().one_or_none()
        if not result:
            raise ObjectNotFoundException

        available_rooms_ids = get_query_rooms_to_date(date_from, date_to, hotel_id)
        # print(rooms_to_get.compile(async_engine, compile_kwargs={'literal_binds': True}))
        rooms_booked_again = get_query_all_rooms_to_date(date_from, date_to)

        query = (
            select(
                self.model,  # type: ignore
                (
                    self.model.quantity
                    - func.coalesce(rooms_booked_again.c.booked_rooms, 0)
                ).label("free_rooms"),
            )
            .outerjoin(
                rooms_booked_again, self.model.id == rooms_booked_again.c.room_id
            )
            .filter(
                self.model.id.in_(
                    select(available_rooms_ids.c.id)
                )  # ← или просто available_rooms_subq.c.id
            )
            .options(selectinload(self.model.facilities))
        )
        query_result = await self.session.execute(query)
        result = query_result.all()
        return [
            FreeRoomGetSchemas.model_validate(
                {
                    **row[0].__dict__,  # все атрибуты RoomsORM c facilities
                    "free_rooms": row[1],
                }
            )
            for row in result
        ]

    async def get_one_or_none_with_relship(self, **filters) -> BaseModel:
        safe_filters = self._get_safe_filters(filters)
        check_safe_filters(safe_filters)
        query = select(self.model).filter_by(**safe_filters)
        query_result = await self.session.execute(query)
        result = query_result.scalars().one_or_none()
        if not result:
            raise ObjectNotFoundException
        query = (
            select(self.model)
            .filter_by(**safe_filters)
            .options(selectinload(self.model.facilities))  # type: ignore
        )
        query_result = await self.session.execute(query)
        result = query_result.scalars().one_or_none()
        return RoomFacilitiesGetSchemas.model_validate(result, from_attributes=True)
