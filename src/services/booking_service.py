from datetime import date

from src.api.routers.utils import check_date_to_after_date_from
from src.models import BookingORM
from src.schemas.booking_shemas import (
    BookingGetSchemas,
    BookingRequestSchemas,
    BookingCreateSchemas,
)
from src.schemas.rooms_schemas import RoomGetSchemas
from src.services.base_service import BaseService


class BookingService(BaseService):
    async def get_all_with_any_parameters(
        self,
        user_id: int,
        date_from: date = None,
    ) -> list[BookingGetSchemas]:
        if date_from:
            bookings = await self.db.booking.get_all_with_any_parameters(
                BookingORM.date_from >= date_from, user_id=user_id
            )
        else:
            bookings = await self.db.booking.get_all_with_parameters(user_id=user_id)

        return bookings

    async def get_booking_to_date(
        self,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> tuple[list[BookingGetSchemas], int, int]:
        check_date_to_after_date_from(date_from, date_to)
        await self.check_hotel_or_room_exists(room_id=room_id)
        booking = await self.db.booking.get_booking_to_date(
            room_id=room_id, date_from=date_from, date_to=date_to
        )
        quantity_booked_rooms = len(booking)
        room: RoomGetSchemas = await self.db.rooms.get_one(id=room_id)
        quantity_rooms = room.quantity
        quantity_free_rooms = quantity_rooms - quantity_booked_rooms
        return booking, quantity_booked_rooms, quantity_free_rooms

    async def add_booking(
        self,
        user_id: int,
        booking_info: BookingRequestSchemas,
    ) -> tuple[BookingGetSchemas, RoomGetSchemas]:
        check_date_to_after_date_from(booking_info.date_from, booking_info.date_to)
        await self.check_hotel_or_room_exists(room_id=booking_info.room_id)
        room: RoomGetSchemas = await self.db.rooms.get_one(id=booking_info.room_id)
        _booking_info = BookingCreateSchemas(
            user_id=user_id, price=room.price, **booking_info.model_dump()
        )
        booking: BookingGetSchemas = await self.db.booking.add_booking(
            _booking_info, hotel_id=room.hotel_id
        )
        return booking, room
