from src.models.booking import BookingORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base_mapp import DataMapper
from src.schemas.booking_shemas import BookingGetSchemas
from src.schemas.facilities_schemas import (
    FacilitiesGetSchemas,
    RoomFacilitiesGetSchemas,
)
from src.schemas.hotels_schemas import HotelGetSchemas
from src.schemas.rooms_schemas import RoomGetSchemas
from src.schemas.users_schemas import UserGetSchemas


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schemas = HotelGetSchemas


class BookingDataMapper(DataMapper):
    db_model = BookingORM
    schemas = BookingGetSchemas


class FacilitiesMapper(DataMapper):
    db_model = FacilitiesORM
    schemas = FacilitiesGetSchemas


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schemas = RoomGetSchemas


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schemas = UserGetSchemas


class RoomFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schemas = RoomFacilitiesGetSchemas
