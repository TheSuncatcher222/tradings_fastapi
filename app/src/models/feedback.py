# """
# Модуль с ORM моделями базы данных приложения "feedback".
# """

from datetime import datetime

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
