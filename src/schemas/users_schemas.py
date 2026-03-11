from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Enum


class UserRequestSchemas(BaseModel):
    email: EmailStr = Field(..., description="Адрес эл.почты")
    first_name: str | None = Field(None, description="Имя пользователя")
    last_name: str | None = Field(None, description="Фамилия пользователя")
    password: str = Field(..., description="Пароль")


example_add_user = {
    "1": {
        "summary": "Макс",
        "value": {
            "email": "anikeev.mks@rambler.com",
            "first_name": "Maks",
            "last_name": "Ananimus",
            "password": "admin",
        },
    },
    "2": {
        "summary": "Лучиано",
        "value": {"email": "luchy@rambler.com", "password": "userik"},
    },
}


class UserCreateSchemas(BaseModel):
    email: EmailStr = Field(..., description="Адрес эл.почты")
    first_name: str | None = Field(None, description="Имя пользователя")
    last_name: str | None = Field(None, description="Фамилия пользователя")
    hashed_password: str = Field(..., description="Закодированный пароль")
    is_active: bool | None = Field(True, description="Статус пользователя")
    role: str = Field(..., description="Роль в проекте")


class UserGetSchemas(BaseModel):
    id: int
    email: EmailStr = Field(..., description="Адрес эл.почты")
    first_name: str | None = Field(None, description="Имя пользователя")
    last_name: str | None = Field(None, description="Фамилия пользователя")
    is_active: bool = Field(..., description="Статус пользователя")
    role: str = Field(..., description="Роль в проекте")
    created_at: datetime = Field(..., description="Дата регистрации пользователя")
    updated_at: datetime = Field(
        ..., description="Дата обновления информации о пользователе"
    )


class UserGetHashedPassword(BaseModel):
    id: int
    email: EmailStr = Field(..., description="Адрес эл.почты")
    hashed_password: str = Field(..., description="Закодированный пароль")

    model_config = {"from_attributes": True}


class UserRoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    anonymous = "anonymous"
