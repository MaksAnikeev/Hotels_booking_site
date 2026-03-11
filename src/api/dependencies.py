from typing import Annotated

from fastapi import Depends, HTTPException
from starlette.requests import Request

from src.database import async_session_factory
from src.schemas.hotels_schemas import PaginationParamsSchemas
from src.services.auth import AuthService
from src.utils.db_manager import DBManager

PaginationDep = Annotated[PaginationParamsSchemas, Depends(PaginationParamsSchemas)]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(
            status_code=404, detail="Нет токена. Необходимо залогиниться"
        )
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().get_data_from_hash(token)
    return data["user_id"]


UserIDDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
