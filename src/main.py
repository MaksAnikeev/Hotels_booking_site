import uvicorn
from async_generator import asynccontextmanager
from fastapi import FastAPI
import sys
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.routers.routers import init_routers
from src.setup import redis_connector

sys.path.append(str(Path(__file__).parent.parent))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

init_routers(app_=app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
