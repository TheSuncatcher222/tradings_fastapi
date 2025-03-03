"""Модуль с классом CRUD запросов в базу данных для модели UsedPassResetToken."""

from datetime import datetime

from sqlalchemy.sql import select
from sqlalchemy.sql.selectable import Select

from src.database.base_async_crud import BaseAsyncCrud
from src.database.database import AsyncSession
from src.models.auth import UsedPassResetToken


class UsedPassResetTokenV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице UsedPassResetToken."""

    async def retrieve_by_token(
        self,
        *,
        obj_token: str,
        session: AsyncSession,
    ) -> UsedPassResetToken:
        """Получает один объект из базы данных по указанному значение токена."""
        query: Select = select(self.model).where(self.model.token == obj_token)
        return (await session.execute(query)).scalars().first()

    async def delete_by_exp_date(
        self,
        *,
        session: AsyncSession,
    ) -> None:
        """Удаляет все объекты из базы данных с истекшим сроком жизни."""
        stmt: Select = select(self.model).where(
            self.model.exp_date < datetime.now(),
        )
        await session.execute(stmt)
        await session.commit()
        return


used_pass_reset_token_v1_crud = UsedPassResetTokenV1Crud(model=UsedPassResetToken)
