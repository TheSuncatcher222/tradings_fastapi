"""Модуль с классом CRUD запросов в базу данных для модели User."""

from fastapi import HTTPException, status
from sqlalchemy.sql import select, update
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.selectable import Select

from src.database.base_async_crud import BaseAsyncCrud
from src.database.database import AsyncSession
from src.models.user import User
from src.utils.email_confirm import send_email_confirm_code
from src.utils.password import hash_password


# TODO. Запретить прочие методы.
class UserV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице User."""

    async def retrieve_by_email(
        self,
        *,
        obj_email: str,
        session: AsyncSession,
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
        session: AsyncSession,
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

    async def update_by_id(
        self,
        *,
        obj_id: int,
        obj_data: dict[str, any],
        session: AsyncSession,
        obj_unique_check: bool = False,
    ) -> User:
        """
        Обновляет один объект из базы данных по указанному id.

        Если пользователь решил обновить адрес электронной почты,
        не изменяет это поле сразу, а отправляет ссылку для подтверждения
        на новый указанный почтовый адрес.
        """

        user: User = await self.retrieve_by_id(obj_id=obj_id, session=session)
        new_email: str | None = obj_data.get('email', None)
        if new_email and user.email != new_email:
            await self._check_unique(obj_values=obj_data, session=session)
            new_email: str = obj_data.pop('email')
            await send_email_confirm_code(
                user_id=user.id,
                user_email=new_email,
                user_full_name=user.get_full_name,
            )
        elif obj_unique_check:
            await self._check_unique(obj_values=obj_data, session=session)

        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**obj_data)
            .returning(self.model)
        )
        obj: User = (await session.execute(stmt)).scalars().first()

        await session.commit()

        return obj

    async def delete_by_id(self):
        """
        Удаляет один объект из базы данных по указанному id.
        Метод запрещен.
        """
        raise NotImplementedError('Метод "delete_by_id" в классе "UserV1Crud" запрещен.')

    async def update_email_by_id(
        self,
        *,
        obj_id: int,
        new_email: str,
        session: AsyncSession,
    ) -> None:
        """
        Изменяет адрес электронной почты пользователя
        и устанавливает статус "подтверждена".
        """
        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(
                {
                    'email': new_email,
                    'email_is_confirmed': True,
                },
            )
        )
        await session.execute(stmt)
        await session.commit()

        return


user_v1_crud = UserV1Crud(
    model=User,
    unique_columns=('email',),
    unique_columns_err='Пользователь с таким адресом электронной почты уже зарегистрирован',
)
