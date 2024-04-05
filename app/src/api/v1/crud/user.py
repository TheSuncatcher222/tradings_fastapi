"""Модуль с классом CRUD запросов в базу данных для модели User."""

from fastapi import HTTPException, status
from sqlalchemy.sql import select
from sqlalchemy.sql.selectable import Select

from src.api.base_async_crud import BaseAsyncCrud
from src.database.database import AsyncSession
from src.models.user import User
from src.utils.password import hash_password


# TODO. Запретить прочие методы.
class UserV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице User."""

    async def retrieve_by_email(
        self,
        *,
        obj_email: str,
        session: AsyncSession
    ) -> User:
        """Получает один объект User из базы данных по указанному email."""
        query: Select = (
            select(self.model)
            .where(self.model.email == obj_email)
        )
        user: User | None = (await session.execute(query)).scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Объект не найден',
            )
        return user

    async def retrieve_by_email_and_password(
        self,
        *,
        obj_email: str,
        obj_raw_password: str,
        session: AsyncSession
    ) -> User:
        """Получает один объект User из базы данных по указанному email и password."""
        query: Select = (
            select(self.model)
            .where(
                self.model.email == obj_email,
                self.model.hashed_password == await hash_password(raw_password=obj_raw_password),
            )
        )
        user: User | None = (await session.execute(query)).scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Объект не найден',
            )
        return user

    async def delete_by_id(self):
        """
        Удаляет один объект из базы данных по указанному id.
        Метод запрещен.
        """
        raise NotImplementedError('Метод "delete_by_id" в классе "UserV1Crud" запрещен.')


user_v1_crud = UserV1Crud(
    model=User,
    unique_columns=('email',),
    unique_columns_err='Пользователь с таким адресом электронной почты уже зарегистрирован',
)
