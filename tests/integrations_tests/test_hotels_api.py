from pprint import pprint


async def test_get_hotels(ac):
    response = await ac.get(url="/hotels/")
    assert response.status_code == 200
    hotels = response.json()["data"]
    assert len(hotels) == 5


async def test_get_hotels_with_params(ac):
    params = {"title": 5}
    response = await ac.get(url="/hotels/", params=params)
    assert response.status_code == 200
    hotels = response.json()
    assert "data" in hotels
    assert hotels["data"][0]["location"] == "Краснодар"


async def test_get_free_hotels(ac):
    params = {
        "date_from": "2026-01-25",
        "date_to": "2026-01-30",
    }
    response = await ac.get(url="/hotels/free", params=params)
    assert response.status_code == 200
    free_hotels = response.json()
    assert len(free_hotels["data"]) == 3
