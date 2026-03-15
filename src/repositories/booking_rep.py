from datetime import date
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select, and_, insert

from src.exceptions import ObjectNotFoundException, AllRoomIsBookedException, NotAllNecessaryParamsException
from src.models.booking import BookingORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import get_query_rooms_to_date


class BookingRepository(BaseRepository):
    model = BookingORM
    mapper = BookingDataMapper

    async def get_booking_to_date(self, room_id, date_from, date_to):
        query = select(self.model).filter_by(room_id=room_id)
        if not date_from or not date_to:
            raise NotAllNecessaryParamsException
        query = query.where(
            and_(BookingORM.date_from <= date_to, BookingORM.date_to >= date_from)
        )
        # print(query.compile(async_engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        rooms = result.scalars().all()
        return self._to_schemas(rooms)

    async def get_booking_chek_in_now(self):
        query = select(self.model).where(BookingORM.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(r) for r in result.scalars().all()]

    async def add_booking(self, data: BaseModel, hotel_id: int = None):
        free_rooms_ids_query = get_query_rooms_to_date(
            data.date_from, data.date_to, hotel_id
        )
        result = await self.session.execute(free_rooms_ids_query)
        free_rooms_ids: Sequence[int] = result.scalars().all()
        if data.room_id not in free_rooms_ids:
            raise AllRoomIsBookedException
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        # print(stmt.compile(async_engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(stmt)
        return self.mapper.map_to_domain_entity(result.scalars().one())
