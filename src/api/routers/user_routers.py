from fastapi import APIRouter, Body, Query, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import PaginationDep, UserIDDep, DBDep
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
    "/me", summary="демонстрация данных по текущему аутентифицированному пользователю"
)
async def who_are_me(
    user_id: UserIDDep,
    db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return {"status": "success", "data": user, "details": None}


@router.post("/add", summary="регистрация пользователя")
async def add_user(
    db: DBDep,
    user_info: UserRequestSchemas = Body(openapi_examples=example_add_user),
):
    hashed_password = AuthService().get_password_hash(user_info.password)
    role = UserRoleEnum.user
    try:
        new_user_info = UserCreateSchemas(
            email=user_info.email,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            hashed_password=hashed_password,
            role=role,
        )
        new_user = await db.users.add(new_user_info)
        await db.commit()
        return {
            "status": "OK",
            "description": f"Новый пользователь {new_user.first_name} успешно добавлен",
            "user_info": new_user,
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Пользователь с таким email {user_info.email} уже существует",
        )


@router.post("/login", summary="аутентификация пользователя")
async def user_login(
    response: Response,
    db: DBDep,
    user_info: UserRequestSchemas = Body(openapi_examples=example_add_user),
):
    user = await db.users.get_user_with_hashed_password(email=user_info.email)
    if not AuthService().verify_password(user_info.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверно указанный пароль.")

    access_token = AuthService().create_access_token({"user_id": user.id})
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
