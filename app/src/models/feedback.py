"""
Модуль с ORM моделями базы данных приложения "feedback".
"""

from datetime import datetime

from sqladmin import ModelView
from sqlalchemy import (
    ARRAY,
    DateTime,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import func

from src.database.database import (
    Base,
    TableNames,
)
from src.validators.feedback import FeedbackParams
from src.validators.user import UserParams


class Feedback(Base):
    """Декларативная модель представления формы обратной связи пользователей."""

    __tablename__ = TableNames.feedback
    __tableargs__ = {
        'comment': 'Форма обратной связи пользователей',
    }

    # Primary Keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Columns
    attachments: Mapped[str] = mapped_column(
        ARRAY(String(length=FeedbackParams.FILE_LEN_MAX)),
        comment='данные прикрепленных файлов',
    )
    contacts: Mapped[str] = mapped_column(
        String(length=FeedbackParams.CONTACTS_LEN_MAX),
        comment='телефон или телеграм',
    )
    datetime_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время отправки',
        server_default=func.now(),
    )
    email: Mapped[str] = mapped_column(
        String(length=UserParams.EMAIL_LEN_MAX),
        comment='email',
    )
    message: Mapped[str] = mapped_column(
        String(length=FeedbackParams.MESSAGE_LEN_MAX),
        comment='сообщение',
    )
    username: Mapped[str] = mapped_column(
        String(length=UserParams.EMAIL_LEN_MAX),
        comment='имя',
    )


class FeedbackAdmin(ModelView, model=Feedback):

    # Metadata.
    name = 'Отзыв'
    name_plural = 'Отзывы'
    icon = 'fa-solid fa-comment'
    category = 'Обращения'

    # Permissions.
    can_create = True
    can_view_details = True
    can_export = True
    can_edit = True
    can_delete = True

    # Pagination options.
    page_size = 25
    page_size_options = (
        25,
        50,
        100,
        200,
    )

    # List page.
    column_default_sort = [
        (Feedback.id, True),
    ]
    column_list = (
        'id',
        'datetime_created',
        'email',
        'contacts',
        'username',
    )
    column_searchable_list = (
        Feedback.id,
        Feedback.datetime_created,
        Feedback.email,
        Feedback.contacts,
        Feedback.username,
    )
    column_sortable_list = (
        Feedback.id,
        Feedback.datetime_created,
        Feedback.email,
        Feedback.contacts,
        Feedback.username,
    )

    # Details page.
    column_details_list = (
        'id',
        'datetime_created',
        'email',
        'contacts',
        'username',
        'attachments',
        'message',
    )

    # Other.
    pk_columns = (Feedback.id,)
    is_async = True
