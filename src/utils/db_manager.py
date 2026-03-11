from src.repositories.booking_rep import BookingRepository
from src.repositories.fasilities_rep import (
    FacilitiesRepository,
    RoomFacilitiesRepository,
)
from src.repositories.hotels_rep import HotelsRepository
from src.repositories.room_rep import RoomsRepository
from src.repositories.user_rep import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.booking = BookingRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.room_facilities = RoomFacilitiesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
