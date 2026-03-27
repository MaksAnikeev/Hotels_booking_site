from fastapi import APIRouter, Body, Query, HTTPException, status, Response

from src.api.dependencies import PaginationDep, UserIDDep, DBDep
from src.exceptions import (
    AlreadyExistedException,
    ObjectNotFoundException,
    UserAlreadyExistedHTTPException,
    UserNotExistedHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from src.schemas.users_schemas import (
    UserRequestSchemas,
    UserCreateSchemas,
    example_add_user,
    UserRoleEnum,
)
from src.services.auth import AuthService

router = APIRouter(prefix="/user", tags=["Аутентификация и Авторизация"])


@router.get("/", summary="Получить данные по пользователям")
async def get_users(
    pagination: PaginationDep,
    db: DBDep,
    first_name: str | None = Query(None, description="Имя"),
    last_name: str | None = Query(None, description="Фамилия"),
):
    users = await db.users.get_all(
        first_name=first_name,
        last_name=last_name,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )

    return {"status": "success", "data": users, "details": None}


@router.get(
    "/me", summary="🧑‍💻 Мой профиль"
)
async def who_are_me(
    user_id: UserIDDep,
    db: DBDep,
):
    user = await db.users.get_one(id=user_id)
    return {"status": "success", "data": user, "details": None}


@router.post("/add", summary="регистрация пользователя")
async def add_user(
    db: DBDep,
    user_info: UserRequestSchemas = Body(openapi_examples=example_add_user),
):
    try:
        new_user = await AuthService(db).add_user(user_info=user_info)

    except AlreadyExistedException:
        raise UserAlreadyExistedHTTPException

    await db.commit()
    return {
        "status": "OK",
        "description": f"Новый пользователь {new_user.first_name} успешно добавлен",
        "user_info": new_user,
    }


@router.post("/login", summary="аутентификация пользователя")
async def user_login(
    response: Response,
    db: DBDep,
    user_info: UserRequestSchemas = Body(openapi_examples=example_add_user),
):
    try:
        access_token = await AuthService(db).get_user_with_hashed_password(
            user_info=user_info
        )
    except ObjectNotFoundException:
        raise UserNotExistedHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)

    return {
        "status": "OK",
        "description": "JWT token успешно создан",
        "access_token": access_token,
    }


@router.post("/logout", summary="Удаление токена доступа. Разлогиневание")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {
        "status": "success",
    }
