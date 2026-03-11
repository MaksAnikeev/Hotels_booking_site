from src.schemas.hotels_schemas import HotelCreateSchemas
from src.utils.db_manager import DBManager


async def test_create_hotel(db: DBManager):
    hotel_data = HotelCreateSchemas(
        title="hotel 5*",
        location="Краснодар",
        description="новый отель около Краснодара с бассейном",
    )
    await db.hotels.add(hotel_data)
    await db.commit()
    # print(new_hotel_data)
