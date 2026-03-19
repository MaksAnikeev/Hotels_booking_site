from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.utils.db_manager import DBManager


class BaseService:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db

    async def check_hotel_exists(self, hotel_id: int) -> bool:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def check_room_exists(self, room_id: int) -> bool:
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

    async def check_hotel_or_room_exists(
        self, hotel_id: int = None, room_id: int = None
    ) -> bool:
        if hotel_id and room_id:
            await self.check_hotel_exists(hotel_id)
            await self.check_room_exists(room_id)
            return True
        elif hotel_id:
            await self.check_hotel_exists(hotel_id)
            return True
        elif room_id:
            await self.check_room_exists(room_id)
            return True
        else:
            return False
