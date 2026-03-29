import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-02-15", "2026-02-20", 200),
        (1, "2026-02-15", "2026-02-20", 200),
        (1, "2026-02-16", "2026-02-21", 200),
        (1, "2026-02-17", "2026-02-22", 200),
        (1, "2026-02-15", "2026-02-20", 200),
        (1, "2026-02-18", "2026-02-21", 409),
        (1, "2026-02-25", "2026-02-27", 200),
        (1, "2026-02-16", "2026-02-22", 409),
    ],
)
async def test_create_booking(
    room_id, date_from, date_to, status_code, auth_ac: AsyncClient
):
    booking_data = {
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    }
    response = await auth_ac.post("/bookings", json=booking_data)
    assert response.status_code == status_code
    res = response.json()
    if response.status_code == 200:
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "room_info" in res
    else:
        assert res["detail"] == "Нет свободных номеров данного класса на выбранную дату"


@pytest.mark.parametrize(
    "room_id, date_from, date_to, quantity_booked",
    [
        (1, "2026-03-15", "2026-03-20", 1),
        (1, "2026-02-15", "2026-02-20", 2),
        (1, "2026-04-16", "2026-04-21", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    quantity_booked,
    auth_ac: AsyncClient,
    delete_all_bookings,
):
    booking_data = {
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    }
    response_booked = await auth_ac.post("/bookings", json=booking_data)
    assert response_booked.status_code == 200

    response = await auth_ac.get("/bookings/me", params={"date_from": "2026-02-10"})
    assert response.status_code == 200
    if response.status_code == 200:
        assert len(response.json()["data"]) == quantity_booked
