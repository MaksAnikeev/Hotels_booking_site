from sqlalchemy import select

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilitiesMapper, RoomFacilitiesDataMapper
from src.schemas.facilities_schemas import RoomFacilitiesCreateSchemas


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesMapper


class RoomFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomFacilitiesDataMapper

    async def set_room_facilities(self, room_id, facilities_ids):
        existing_room_facilities_ids_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        query = await self.session.execute(existing_room_facilities_ids_query)
        existing_room_facilities_ids = set(query.scalars().all())

        facilities_delete_ids = existing_room_facilities_ids - set(facilities_ids)
        facilities_add_ids = set(facilities_ids) - existing_room_facilities_ids

        if facilities_add_ids:
            room_facilities = [
                RoomFacilitiesCreateSchemas(room_id=room_id, facility_id=f_id)
                for f_id in facilities_add_ids
            ]
            await self.add_bulk(room_facilities)

        if facilities_delete_ids:
            await self.delete_bulk(
                attribute="facility_id",
                ids_for_delete=facilities_delete_ids,
                room_id=room_id,
            )
