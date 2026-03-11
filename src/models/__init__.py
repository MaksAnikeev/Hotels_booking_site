from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.models.booking import BookingORM
from src.models.facilities import FacilitiesORM


all = [
    UsersORM,
    HotelsORM,
    RoomsORM,
    BookingORM,
    FacilitiesORM,
]