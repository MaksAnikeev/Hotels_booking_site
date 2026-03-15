from sqlalchemy import select, func

from src.exceptions import NotAllowedParameterException
from src.models.booking import BookingORM
from src.models.rooms import RoomsORM


def get_query_all_rooms_to_date(date_from, date_to):
    """
    Получаем все забронированные номера в указанный период
    with rooms_booked as (
    select room_id, Count(*) as booked_rooms
    from booking
    where
    (date_from <= date '2026-01-30' and date_to >= date '2026-01-25')
    group by room_id)
    """

    rooms_booked = (
        select(BookingORM.room_id, func.count("*").label("booked_rooms"))
        .select_from(BookingORM)
        .filter(BookingORM.date_from <= date_to, BookingORM.date_to >= date_from)
        .group_by(BookingORM.room_id)
        .cte()
    )
    return rooms_booked


def get_query_rooms_to_date(date_from, date_to, hotel_id: int | None = None):

    rooms_booked = get_query_all_rooms_to_date(date_from, date_to)

    """
    Вычитаем из общего количества номеров уже забронированные и берем все поля модели rooms
    available_rooms as (
    select
    r.*, quantity - coalesce(booked_rooms, 0) as free_rooms
    from rooms r left join rooms_booked rb on r.id = rb.room_id 
    )
    """
    available_rooms = (
        select(
            RoomsORM.id,
            (RoomsORM.quantity - func.coalesce(rooms_booked.c.booked_rooms, 0)).label(
                "free_rooms"
            ),
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_booked, RoomsORM.id == rooms_booked.c.room_id)
        .cte("available_rooms")
    )
    """
    Получаем ид номеров, принадлежащих к указанному отелю и переводим это в подзапрос
    select id as room_id
    from rooms
    where hotel_id = 1
    """
    room_ids_from_hotel = select(RoomsORM.id).select_from(RoomsORM)
    if hotel_id:
        room_ids_from_hotel = room_ids_from_hotel.filter(RoomsORM.hotel_id == hotel_id)

    room_ids_from_hotel = room_ids_from_hotel.subquery(name="room_ids_from_hotel")
    """
    Убираем из финального запроса типы номеров, у которых нет свободных слотов
    select * from available_rooms
    where free_rooms > 0 and id in (
    select id as room_id
    from rooms
    where hotel_id = 1
    )
    """
    rooms_to_get = (
        select(available_rooms.c.id)
        .select_from(available_rooms)
        .filter(
            available_rooms.c.free_rooms > 0,
            available_rooms.c.id.in_(select(room_ids_from_hotel)),
        )
    )
    return rooms_to_get


def check_safe_filters(safe_filters):
    if not safe_filters:
        raise NotAllowedParameterException
