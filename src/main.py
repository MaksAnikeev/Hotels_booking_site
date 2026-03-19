import uvicorn
from async_generator import asynccontextmanager
from fastapi import FastAPI
import sys
import logging
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import text

from src.api.routers.routers import init_routers
from src.database import async_session_factory_null_pull
from src.setup import redis_connector
from src.utils.db_manager import DBManager

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector._redis), prefix="fastapi-cache")
    logging.info("FastAPI Cache initialized")
    try:
        async with async_session_factory_null_pull() as session:
            await session.execute(text("SELECT 1"))
            logging.info("Подключение к базе данных успешно проверено")
    except Exception as e:
        logging.critical(
            "Не удалось подключиться к базе данных при старте", exc_info=True
        )
        raise RuntimeError(f"Ошибка подключения к БД: {e}") from e
    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

init_routers(app_=app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
