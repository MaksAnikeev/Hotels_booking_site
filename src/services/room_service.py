from datetime import date

from src.api.routers.utils import check_date_to_after_date_from
from src.exceptions import ObjectNotFoundException, FacilitiesNotFoundException
from src.schemas.facilities_schemas import RoomFacilitiesCreateSchemas
from src.schemas.rooms_schemas import (
    RoomGetSchemas,
    RoomRequestSchemas,
    RoomCreateSchemas,
    RoomChangeRequestSchemas,
    RoomChangeSchemas,
)
from src.services.base_service import BaseService


class RoomService(BaseService):
    async def get_all_with_parameters(self, hotel_id: int) -> list[RoomGetSchemas]:
        await self.check_hotel_or_room_exists(hotel_id=hotel_id)
        rooms = await self.db.rooms.get_all_with_parameters(hotel_id=hotel_id)
        return rooms

    async def get_rooms_to_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ) -> list[RoomGetSchemas]:

        check_date_to_after_date_from(date_from, date_to)
        await self.check_hotel_or_room_exists(hotel_id=hotel_id)
        rooms = await self.db.rooms.get_rooms_to_date(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
        return rooms

    async def get_one_or_none_with_relship(
        self,
        hotel_id: int,
        room_id: int,
    ) -> RoomGetSchemas:

        await self.check_hotel_or_room_exists(hotel_id=hotel_id, room_id=room_id)
        room = await self.db.rooms.get_one_or_none_with_relship(
            id=room_id, hotel_id=hotel_id
        )
        return room

    async def add(
        self,
        hotel_id: int,
        room_info: RoomRequestSchemas,
    ) -> RoomGetSchemas:

        await self.check_hotel_or_room_exists(hotel_id=hotel_id)
        _room_info = RoomCreateSchemas(hotel_id=hotel_id, **room_info.model_dump())
        room: RoomGetSchemas = await self.db.rooms.add(_room_info)
        room_facilities = [
            RoomFacilitiesCreateSchemas(room_id=room.id, facility_id=f_id)
            for f_id in room_info.facilities_ids
        ]
        try:
            await self.db.room_facilities.add_bulk(room_facilities)
        except ObjectNotFoundException:
            raise FacilitiesNotFoundException
        return room

    async def edit(
        self, hotel_id: int, room_id: int, room_info: RoomRequestSchemas
    ) -> RoomGetSchemas:

        await self.check_hotel_or_room_exists(hotel_id=hotel_id, room_id=room_id)
        _room_info = RoomCreateSchemas(hotel_id=hotel_id, **room_info.model_dump())
        room = await self.db.rooms.edit(
            data=_room_info,
            id=room_id,
        )
        try:
            await self.db.room_facilities.set_room_facilities(
                room_id=room.id,
                facilities_ids=room_info.facilities_ids,
            )
        except ObjectNotFoundException:
            raise FacilitiesNotFoundException
        return room

    async def part_edit(
        self, hotel_id: int, room_id: int, room_info: RoomChangeRequestSchemas
    ) -> RoomGetSchemas:

        await self.check_hotel_or_room_exists(hotel_id=hotel_id, room_id=room_id)
        room_info_dict = room_info.model_dump(exclude_unset=True)
        _room_info = RoomChangeSchemas(hotel_id=hotel_id, **room_info_dict)
        room = await self.db.rooms.edit(data=_room_info, id=room_id, hotel_id=hotel_id)

        if "facilities_ids" in room_info_dict:
            try:
                await self.db.room_facilities.set_room_facilities(
                    room_id=room.id,
                    facilities_ids=room_info_dict["facilities_ids"],
                )

            except ObjectNotFoundException:
                raise FacilitiesNotFoundException
        return room

    async def delete(
        self,
        hotel_id: int,
        room_id: int,
    ) -> RoomGetSchemas:

        await self.check_hotel_or_room_exists(hotel_id=hotel_id, room_id=room_id)
        room = await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        return room
