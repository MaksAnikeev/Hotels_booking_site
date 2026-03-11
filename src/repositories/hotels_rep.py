from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import get_query_rooms_to_date


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_all(
        self,
        title,
        location,
        limit,
        offset,
    ):
        query = select(self.model).options(
            selectinload(self.model.rooms).selectinload(RoomsORM.facilities)
        )
        if location:
            query = query.filter(HotelsORM.location.ilike(f"%{location.strip()}%"))
        if title:
            query = query.filter(
                func.lower(HotelsORM.title).contains(title.lower().strip())
            )
        query = query.limit(limit).offset(offset)
        # print(query.compile(async_engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        hotels = result.scalars().unique().all()
        return hotels

    async def get_all_to_date(self, title, location, limit, offset, date_from, date_to):
        free_rooms_ids = get_query_rooms_to_date(date_from, date_to)

        hotels_id_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(free_rooms_ids))
        )

        available_hotels = select(self.model).filter(HotelsORM.id.in_(hotels_id_to_get))
        if location:
            available_hotels = available_hotels.filter(
                HotelsORM.location.ilike(f"%{location.strip()}%")
            )
        if title:
            available_hotels = available_hotels.filter(
                func.lower(HotelsORM.title).contains(title.lower().strip())
            )
        available_hotels = available_hotels.limit(limit).offset(offset)
        # print(available_hotels.compile(async_engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(available_hotels)
        hotels = result.scalars().all()
        return self._to_schemas(hotels)
