from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from pwdlib import PasswordHash
import jwt

from src.config import settings


class AuthService:
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.password_hash.hash(password)

    def get_data_from_hash(self, token):
        try:
            data = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return data
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Время действия токена истекло. Необходимо залогиниться",
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(
                status_code=401, detail="Некорректный токен. Необходимо залогиниться"
            )
