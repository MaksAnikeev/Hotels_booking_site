from src.schemas.hotels_schemas import HotelCreateSchemas


async def test_create_hotel(db):
    hotel_data = HotelCreateSchemas(
        title="hotel 5*",
        location="Краснодар",
        description="новый отель около Краснодара с бассейном",
    )
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
    # print(new_hotel_data)
