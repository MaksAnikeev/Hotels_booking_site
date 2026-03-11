from fastapi import FastAPI
from src.api.routers.hotel_routers import router as hotel_router
from src.api.routers.room_routers import router as room_router
from src.api.routers.user_routers import router as router_auth
from src.api.routers.booking_routers import router as booking_router
from src.api.routers.facilities_routers import router as facilities_router
from src.api.routers.image_routers import router as image_router
from src.api.routers.email_routers import router as email_router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router_auth)
    app_.include_router(hotel_router)
    app_.include_router(room_router)
    app_.include_router(booking_router)
    app_.include_router(facilities_router)
    app_.include_router(image_router)
    app_.include_router(email_router)
