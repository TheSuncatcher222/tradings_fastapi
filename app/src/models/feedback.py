# """
# Модуль с ORM моделями базы данных приложения "feedback".
# """

from datetime import datetime

from sqladmin import ModelView
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.database.database import Base, table_names
from src.validators.feedback import FEEDBACK_CONTACTS_LEN, FEEDBACK_MESSAGE_LEN
from src.validators.user import USER_EMAIL_LEN, USER_USERNAME_LEN


class Feedback(Base):
    """Декларативная модель представления формы обратной связи пользователей."""

    __tablename__ = table_names.feedback
    __tableargs__ = {
        'comment': 'Форма обратной связи пользователей'
    }

    # Primary Keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Columns
    contacts: Mapped[str] = mapped_column(
        String(length=FEEDBACK_CONTACTS_LEN),
        comment='телефон или телеграм',
    )
    created_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время отправки',
        server_default=func.now(),
    )
    data_process_approve: Mapped[bool] = mapped_column(
        comment='согласие на обработку персональных данных',
    )
    email: Mapped[str] = mapped_column(
        String(length=USER_EMAIL_LEN),
        comment='email',
    )
    is_accepted: Mapped[bool] = mapped_column(
        comment='статус отправки в поддержку',
        default=False,
    )
    message: Mapped[str] = mapped_column(
        String(length=FEEDBACK_MESSAGE_LEN),
        comment='сообщение',
    )
    username: Mapped[str] = mapped_column(
        String(length=USER_USERNAME_LEN),
        comment='имя',
    )


"""SQLAdmin."""


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
        'username',
        'email',
        'contacts',
        'is_accepted',
        'created_datetime',
    )
    column_searchable_list = (
        Feedback.id,
        Feedback.username,
        Feedback.email,
        Feedback.contacts,
        Feedback.created_datetime,
    )
    column_sortable_list = (
        Feedback.id,
        Feedback.username,
        Feedback.email,
        Feedback.contacts,
        Feedback.is_accepted,
        Feedback.created_datetime,
    )

    # Details page.
    column_details_list = (
        'id',
        'username',
        'email',
        'contacts',
        'is_accepted',
        'created_datetime',
        'data_process_approve',
        'message',
    )

    # Other.
    pk_columns = (Feedback.id,)
    is_async = True
