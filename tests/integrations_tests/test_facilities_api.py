from httpx import AsyncClient


async def test_post_facilities(ac: AsyncClient):
    facilities_info = {"title": "Унитаз"}
    response = await ac.post("/facilities/", json=facilities_info)
    assert response.status_code == 200


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get("/facilities/")
    assert response.status_code == 200
    facilities = response.json()
    assert facilities["data"][0]["title"] == "Унитаз"
