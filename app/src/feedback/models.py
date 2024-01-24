"""
Модуль с ORM моделями базы данных приложения "feedback".
"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from src.config import TABLE_FEEDBACK
from src.users.models import USER_EMAIL_LEN, USER_TELEGRAM_LEN, USER_USERNAME_LEN

FEEDBACK_CONTACTS_LEN: int = 30
FEEDBACK_MESSAGE_LEN: int = 512


class Base(DeclarativeBase):
    """Инициализирует фабрику создания декларативных классов моделей."""
    pass


class Feedback(Base):
    """Декларативная модель представления формы обратной связи пользователей."""

    __tablename__ = TABLE_FEEDBACK
    __tableargs__ = {
        'comment': 'Форма обратной связи пользователей'
    }

    contacts: Mapped[str] = mapped_column(
        # INFO: длина поля Telegram username превосходит длину номера телефона.
        String(length=USER_TELEGRAM_LEN),
        comment='телефон или телеграм',
    )
    data_process_approve: Mapped[bool] = mapped_column(
        comment='согласие на обработку персональных данных',
    )
    email: Mapped[str] = mapped_column(
        String(length=USER_EMAIL_LEN),
        comment='email',
    )
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )
    is_accepted: Mapped[bool] = mapped_column(
        comment='статус отправки в поддержку',
        default=False,
    )
    message: Mapped[str] = mapped_column(
        String(length=FEEDBACK_MESSAGE_LEN),
        comment='сообщение',
    )
    name: Mapped[str] = mapped_column(
        String(length=USER_USERNAME_LEN),
        comment='Имя',
    )
    reg_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время отправки',
        server_default=func.now(),
    )
