from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

# это часть кода, когда мы прокидываем в обычное подключение к БД null_pull во время тестов, иначе тесты валятся,
# ищут пулл соединений, а его нет и тут мы указываем что нет пула, соединение одно
# сейчас это реализовано другим методом - подмена зависимости в conftest.py
# # db_params = {}
#
# if settings.MODE == 'TEST':
#     db_params = {'poolclass': NullPool}
#
# async_engine = create_async_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo = False,
#     **db_params,
# )

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=False)

async_engine_null_pull = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    poolclass=NullPool,
)

async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
async_session_factory_null_pull = async_sessionmaker(
    bind=async_engine_null_pull, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
