"""
Модуль с ORM моделями базы данных приложения "user".
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from src.config import TABLE_USER

# INFO: в pydantic.EmailStr разрешенные длины строк составляют 64@63.63
USER_EMAIL_LEN: int = 64 + 63 + 63
USER_HASH_PASS_LEN: int = 256
USER_PHONE_LEN: int = 20
USER_TELEGRAM_LEN: int = 32
USER_USERNAME_LEN: int = 25


class Base(DeclarativeBase):
    """Инициализирует фабрику создания декларативных классов моделей."""
    pass


class User(Base):
    """Декларативная модель представления пользователя."""

    __tablename__ = TABLE_USER
    __tableargs__ = {
        'comment': 'Пользователи'
    }

    account_balance: Mapped[int] = mapped_column(
        comment='остаток средств на балансе',
        server_default='0'
    )
    # INFO: подтверждается автоматически.
    email: Mapped[str] = mapped_column(
        String(length=USER_EMAIL_LEN),
        comment='email',
        unique=True,
    )
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )
    is_active: Mapped[bool] = mapped_column(
        comment='статус активного',
        default=True,
    )
    is_admin: Mapped[bool] = mapped_column(
        comment='статус администратора',
        default=False,
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(length=USER_HASH_PASS_LEN),
        comment='хэш пароля',
    )
    name_first: Mapped[str] = mapped_column(
        String(length=USER_USERNAME_LEN),
        comment='имя',
        nullable=True,
    )
    name_last: Mapped[str] = mapped_column(
        String(length=USER_USERNAME_LEN),
        comment='фамилия',
        nullable=True,
    )
    # TODO: сделать поле phonenumber.
    phone: Mapped[str] = mapped_column(
        String(length=USER_PHONE_LEN),
        comment='номер телефона',
        nullable=True,
    )
    phone_is_verified: Mapped[bool] = mapped_column(
        comment='статус подтвержденного номера телефона',
        default=False,
    )
    reg_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время регистрации',
        server_default=func.now(),
    )
    telegram_username: Mapped[str] = mapped_column(
        String(length=USER_TELEGRAM_LEN),
        comment='telegram профиль',
        nullable=True,
    )
    telegram_is_verified: Mapped[bool] = mapped_column(
        comment='статус подтвержденного telegram профиля',
        default=False,
    )

    def __str__(self) -> str:
        return f'{self.email} ({self.name_first} {self.name_last})'
