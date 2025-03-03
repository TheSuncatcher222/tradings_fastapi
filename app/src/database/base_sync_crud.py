"""
Модуль базового класса синхронных CRUD запросов в базу данных.
"""

from uuid import UUID

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql import (
    delete,
    select,
    update,
)
from sqlalchemy.sql.dml import (
    Delete,
    Update,
)
from sqlalchemy.sql.selectable import Select

from app.src.config.config import Pagination
from app.src.database.database import Base
from app.src.utils.datetime_calc import datetime_now_utc


class BaseSyncCrud():
    """
    Базовый класс синхронных CRUD запросов в базу данных.
    """

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

    def create(
        self,
        *,
        obj_data: dict[str, any],
        # TODO. Узнать аннотацию.
        session: Session,
        perform_cleanup: bool = True,
        perform_commit: bool = True,
    ) -> Base:
        """
        Создает один объект в базе данных.
        """
        self._check_unique(obj_data=obj_data, session=session)

        if perform_cleanup:
            obj_data: dict[str, any] = self._clean_obj_data_non_model_fields(obj_data=obj_data)

        model: Base = self.model(**obj_data)
        session.add(model)

        if perform_commit:
            session.commit()

        return model

    def retrieve_all(
        self,
        *,
        limit: int = Pagination.LIMIT_DEFAULT,
        offset: int = Pagination.OFFSET_DEFAULT,
        session: Session,
    ) -> list[Base]:
        """
        Получает все объекты из базы данных.
        """
        query: Select = (
            select(self.model)
            .limit(limit)
            .offset(offset)
        )
        return (session.execute(query)).scalars().all()

    def retrieve_by_id(
        self,
        *,
        obj_id: int,
        session: Session,
    ) -> Base:
        """
        Получает один объект из базы данных по указанному id.
        """
        query: Select = select(self.model).where(self.model.id == obj_id)
        return (session.execute(query)).scalars().first()

    def update_by_id(
        self,
        *,
        obj_id: int,
        obj_data: dict[str, any],
        session: Session,
        perform_cleanup: bool = True,
        perform_commit: bool = True,
        perform_obj_unique_check: bool = False,
    ) -> Base:
        """
        Обновляет один объект из базы данных по указанному id.
        """
        if perform_cleanup:
            obj_data: dict[str, any] = self._clean_obj_data_non_model_fields(obj_data=obj_data)

        if perform_obj_unique_check:
            self._check_unique(obj_data=obj_data, session=session)

        query: Select = select(self.model).where(self.model.id == obj_id)
        if (session.execute(query)).scalars().first() is None:
            self._raise_httpexception_404_not_found(id=obj_id)

        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**obj_data)
            .returning(self.model)
        )
        obj: Base = (session.execute(stmt)).scalars().first()

        if perform_commit:
            session.commit()

        return obj

    def delete_by_id(
        self,
        *,
        obj_id: int,
        session: Session,
        perform_commit: bool = True,
    ) -> None:
        """
        Удаляет один объект из базы данных по указанному id.
        """
        stmt: Delete = (
            delete(self.model)
            .where(self.model.id == obj_id)
        )
        session.execute(stmt)
        if perform_commit:
            session.commit()
        return

    def delete_soft_by_id(
        self,
        *,
        obj_id: int,
        session: Session,
        perform_commit: bool = True,
    ) -> None:
        """
        Удаляет фиктивно один объект из базы данных по указанному id:
            - обновляет поле is_deleted = True
            - обновляет поле datetime_deleted = "сейчас"
        """
        query: Select = select(self.model).where(self.model.id == obj_id)
        if (session.execute(query)).scalars().first() is None:
            return

        stmt: Update = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(
                is_deleted=True,
                datetime_deleted=datetime_now_utc(),
            )
        )
        session.execute(stmt)

        if perform_commit:
            session.commit()

        return

    def _check_unique(
        self,
        *,
        obj_data: dict[str, any],
        session: Session,
    ) -> None:
        """
        Проверяет уникальность объекта в базе данных.
        """
        ...

    def _clean_obj_data_non_model_fields(
        self,
        *,
        obj_data: dict[str, any],
    ) -> dict[str, any]:
        """
        Удаляет из переданных данных поля, которые не являются колонками модели.
        Возвращает новый словарь obj_data без удаленных полей.
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
