"""
Модуль базового класса асинхронных CRUD запросов в базу данных.
"""

from uuid import UUID

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.sql import (
    insert,
    select,
    update,
)
from sqlalchemy.sql.dml import (
    Insert,
    Update,
)
from sqlalchemy.sql.selectable import Select

from src.config.config import Pagination
from src.database.database import (
    AsyncSession,
    Base,
)
from src.utils.custom_exception import (
    CustomValidationTypes,
    form_pydantic_like_validation_error,
)
from src.utils.datetime_calc import datetime_now_utc


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
        obj_data: dict[str, any],
        session: AsyncSession,
        perform_cleanup: bool = True,
        perform_commit: bool = True,
    ) -> Base:
        """Создает один объект в базе данных."""
        await self._check_unique(obj_data=obj_data, session=session)

        if perform_cleanup:
            obj_data: dict[str, any] = self._clean_obj_data_non_model_fields(obj_data=obj_data)

        stmt: Insert = insert(self.model).values(**obj_data).returning(self.model)
        obj: Base = (await session.execute(stmt)).scalars().first()

        if perform_commit:
            await session.commit()

        return obj

    async def retrieve_all(
        self,
        *,
        limit: int = Pagination.LIMIT_DEFAULT,
        offset: int = Pagination.OFFSET_DEFAULT,
        session: AsyncSession,
    ) -> list[Base]:
        """Получает все объекты из базы данных."""
        query: Select = select(self.model).limit(limit).offset(offset)
        return (await session.execute(query)).scalars().all()

    async def retrieve_by_id(
        self,
        *,
        obj_id: int,
        session: AsyncSession,
        raise_404: bool = True,
    ) -> Base:
        """Получает один объект из базы данных по указанному id."""
        query: Select = select(self.model).where(self.model.id == obj_id)
        result: Base | None = (await session.execute(query)).scalars().first()
        if result is None and raise_404:
            self._raise_httpexception_404_not_found(id=obj_id)
        return result

    async def retrieve_by_uuid(
        self,
        *,
        obj_uuid: UUID,
        session: AsyncSession,
    ) -> Base:
        """Получает один объект из базы данных по указанному uuid."""
        query: Select = select(self.model).where(self.model.uuid == obj_uuid)
        result: Base | None = (await session.execute(query)).scalars().first()
        if result is None:
            self._raise_httpexception_404_not_found(uuid=obj_uuid)
        return result

    async def retrieve_by_uuid_and_user_id(
        self,
        *,
        obj_uuid: UUID,
        user_id: int,
        session: AsyncSession,
    ) -> Base:
        """Получает один объект из базы данных по указанному uuid."""
        query: Select = (
            select(self.model)
            .where(
                self.model.uuid == obj_uuid,
                self.model.user_id == user_id,
            )
        )
        result: Base | None = (await session.execute(query)).scalars().first()
        if result is None:
            self._raise_httpexception_404_not_found(uuid=obj_uuid)
        return result

    async def update_by_id(
        self,
        *,
        obj_id: int,
        obj_data: dict[str, any],
        session: AsyncSession,
        perform_obj_unique_check: bool = False,
        perform_cleanup: bool = True,
        perform_commit: bool = True,
    ) -> Base:
        """Обновляет один объект из базы данных по указанному id."""
        if perform_cleanup:
            obj_data: dict[str, any] = self._clean_obj_data_non_model_fields(obj_data=obj_data)

        if perform_obj_unique_check:
            await self._check_unique(obj_data=obj_data, session=session)

        query: Select = select(self.model).where(self.model.id == obj_id)
        if (await session.execute(query)).scalars().first() is None:
            self._raise_httpexception_404_not_found(id=obj_id)

        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**obj_data)
            .returning(self.model)
        )
        obj: Base = (await session.execute(stmt)).scalars().first()

        if perform_commit:
            await session.commit()

        return obj

    async def delete_soft_by_id(
        self,
        *,
        obj_id: int,
        session: AsyncSession,
        perform_commit: bool = True,
    ) -> None:
        """
        Удаляет фиктивно один объект из базы данных по указанному id:
            - обновляет поле is_deleted = True
            - обновляет поле datetime_deleted = "сейчас"
        """
        query: Select = select(self.model).where(self.model.id == obj_id)
        if (await session.execute(query)).scalars().first() is None:
            return

        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(
                is_deleted=True,
                datetime_deleted=datetime_now_utc(),
            )
        )
        await session.execute(stmt)

        if perform_commit:
            await session.commit()

        return

    async def _check_unique(
        self,
        *,
        obj_data: dict[str, any],
        session: AsyncSession,
    ) -> None:
        """Проверяет уникальность переданных значений."""
        if self.unique_columns is None:
            return

        conditions: list = []
        for column_name in self.unique_columns:
            conditions.append(getattr(self.model, column_name) == obj_data[column_name])
        query: Select = select(self.model).filter(*conditions)

        if (await session.execute(query)).scalar() is not None:
            detail: dict[str, any] = form_pydantic_like_validation_error(
                type_=CustomValidationTypes.VALUE_ERROR,
                loc=[
                    'body',
                    0,
                    *self.unique_columns,
                ],
                msg=self.unique_columns_err,
                input_={
                    column: obj_data[column] for column in self.unique_columns
                },
            )
            raise HTTPException(
                detail=detail,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return

    def _clean_obj_data_non_model_fields(
        self,
        *,
        obj_data: dict[str, any],
    ) -> dict[str, any]:
        """
        Удаляет из переданных данных поля, которые не являются колонками модели.
        Возвращает новый словарь obj_data без удаленных полей.

        Атрибуты:
            obj_data: dict[str, any] - данные для обновления объекта
        """
        model_valid_columns: set[str] = {
            col.name
            for col
            in self.model.__table__.columns
        }
        return {
            k: v
            for k, v
            in obj_data.items()
            if k in model_valid_columns
        }

    def _raise_httpexception_404_not_found(
        self,
        id: int | None = None,
        ids: list[int] | None = None,
        uuid: UUID | None = None,
    ) -> None:
        """Выбрасывает HTTPException со статусом 404."""
        if id is not None:
            detail: str = 'Объект с id {id} не найден'.format(id=id)
        elif ids is not None:
            detail = 'Объекты с id {ids} не найдены'.format(ids=', '.join([str(id) for id in ids]))
        elif uuid is not None:
            detail = 'Объект с uuid {uuid} не найден'.format(uuid=uuid)
        else:
            detail = 'Объект не найден'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
