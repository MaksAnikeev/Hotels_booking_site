from pydantic import EmailStr
from sqlalchemy import select, func

from src.exceptions import ObjectNotFoundException
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users_schemas import UserGetHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_all(self, first_name=None, last_name=None, limit=None, offset=None):
        query = select(self.model)
        if first_name:
            query = query.filter(UsersORM.first_name.ilike(f"%{first_name.strip()}%"))
        if last_name:
            query = query.filter(
                func.lower(UsersORM.last_name).contains(last_name.lower().strip())
            )
        if limit and offset:
            query = query.limit(limit).offset(offset)
        # print(query.compile(async_engine, compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        users = result.scalars().all()
        return self._to_schemas(users)

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        query_result = await self.session.execute(query)
        result = query_result.scalars().one_or_none()
        if not result:
            raise ObjectNotFoundException
        return UserGetHashedPassword.model_validate(result, from_attributes=True)
