# ruff: noqa: E402

import json
from typing import AsyncGenerator
from unittest import mock

import pytest
from httpx import ASGITransport, AsyncClient

mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda func: func
).start()

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, async_engine_null_pull, async_session_factory_null_pull
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels_schemas import HotelCreateSchemas
from src.schemas.rooms_schemas import RoomCreateSchemas
from src.utils.db_manager import DBManager


def read_json_files():
    with open("tests/data_to_tests/mock_hotels.json", "r", encoding="utf-8") as f:
        hotels = json.load(f)
        hotels_params = [HotelCreateSchemas.model_validate(hotel) for hotel in hotels]
    with open("tests/data_to_tests/mock_rooms.json", "r", encoding="utf-8") as f:
        rooms = json.load(f)
        rooms_params = [RoomCreateSchemas.model_validate(room) for room in rooms]
        return hotels_params, rooms_params


@pytest.fixture(scope="session", autouse=True)
async def check_test():
    assert settings.MODE == "TEST"


@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_factory_null_pull) as db:
        yield db


async def db_null_pull() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_factory_null_pull) as db:
        yield db


app.dependency_overrides[get_db] = db_null_pull


@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test):
    async with async_engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    hotels_params, rooms_params = read_json_files()
    async with DBManager(session_factory=async_session_factory_null_pull) as db_:
        await db_.hotels.add_bulk(hotels_params)
        await db_.rooms.add_bulk(rooms_params)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(check_test, ac: AsyncClient):
    user_info = {
        "email": "cat@pes.ru",
        "first_name": "Pavel",
        "last_name": "Prokhorov",
        "password": "1234",
    }
    await ac.post("/user/add", json=user_info)


@pytest.fixture(scope="session")
async def auth_ac(register_user, ac: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    user_info = {"email": "cat@pes.ru", "password": "1234"}
    await ac.post("/user/login", json=user_info)
    assert ac.cookies["access_token"]
    yield ac


@pytest.fixture(scope="session")
async def delete_all_bookings(check_test):
    async with DBManager(session_factory=async_session_factory_null_pull) as db_:
        await db_.booking.delete_all()
        await db_.commit()
