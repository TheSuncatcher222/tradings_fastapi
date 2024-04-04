"""Модуль базового класса CRUD запросов в базу данных."""

from fastapi import HTTPException, status
from sqlalchemy.sql import delete, insert, select, update
from sqlalchemy.sql.dml import Delete, Insert, Update
from sqlalchemy.sql.selectable import Select

from src.database.database import AsyncSession, Base

PAGINATION_LIMIT_DEFAULT: int = 15
PAGINATION_OFFSET_DEFAULT: int = 0


class BaseAsyncCrud():
    """Базовый класс CRUD запросов к базе данных."""

    def __init__(
        self,
        *,
        model: Base,
        unique_columns: tuple[str] = None,
        unique_columns_err: str = 'Объект уже существует',
    ):
        self.model = model
        self.unique_columns_err = unique_columns_err
        self.unique_columns = unique_columns

    async def create(
        self,
        *,
        obj_values: dict[str, any],
        session: AsyncSession,
    ) -> Base:
        """Создает один объект в базе данных."""
        await self._check_unique(obj_values=obj_values, session=session)
        stmt: Insert = insert(self.model).values(**obj_values).returning(self.model)
        obj: self.model = (await session.execute(stmt)).scalars().first()
        await session.commit()
        return obj

    async def retrieve_all(
        self,
        *,
        session: AsyncSession,
        offset: int = PAGINATION_OFFSET_DEFAULT,
        limit: int = PAGINATION_LIMIT_DEFAULT,
    ) -> list[Base]:
        """Получает все объекты из базы данных с указанными значениями пагинации."""
        query: Select = select(self.model).order_by(self.model.id.desc()).offset(offset).limit(limit)
        return (await session.execute(query)).scalars().all()

    async def retrieve_by_id(
        self,
        *,
        obj_id: int,
        session: AsyncSession,
    ) -> Base:
        """Получает один объект из базы данных по указанному id."""
        query: Select = select(self.model).where(self.model.id == obj_id)
        result: Base | None = (await session.execute(query)).scalars().first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Объект не найден',
            )
        return result

    async def retrieve_by_ids(
        self,
        *,
        obj_ids: list[int],
        session: AsyncSession,
    ) -> list[Base]:
        """Получает объекты из базы данных по указанному перечню id."""
        query: Select = select(self.model).filter(self.model.id.in_(obj_ids))
        return (await session.execute(query)).scalars().all()

    async def update_by_id(
        self,
        *,
        obj_id: int,
        obj_data: dict[str, any],
        session: AsyncSession,
        obj_unique_check: bool = False,
    ) -> Base:
        """Обновляет один объект из базы данных по указанному id."""
        query: Select = select(self.model).where(self.model.id == obj_id)
        if (await session.execute(query)).scalars().first() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Объект не найден',
            )

        if obj_unique_check:
            await self._check_unique(obj_values=obj_data, session=session)

        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**obj_data)
            .returning(self.model)
        )
        obj: Base = (await session.execute(stmt)).scalars().first()
        await session.commit()
        return obj

    async def delete_by_id(
        self,
        *,
        obj_id: int,
        session: AsyncSession,
    ) -> None:
        """Удаляет один объект из базы данных по указанному id."""
        stmt: Delete = delete(self.model).where(self.model.id == obj_id)
        await session.execute(stmt)
        await session.commit()
        return

    async def _check_unique(
        self,
        *,
        obj_values: dict[str, any],
        session: AsyncSession
    ) -> None:
        """Проверяет уникальность переданных значений."""
        # TODO. Сделать проверку, что поля в obj_values есть в self.unique_columns
        if self.unique_columns is None:
            return

        conditions: list = []
        for column_name in self.unique_columns:
            conditions.append(getattr(self.model, column_name) == obj_values[column_name])
        query: Select = select(self.model).filter(*conditions)

        if (await session.execute(query)).scalar() is not None:
            raise HTTPException(
                detail=self.unique_columns_err,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return
