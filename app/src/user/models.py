"""
Модуль с ORM моделями базы данных приложения "user".
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config import Base, TABLE_USER

# INFO: в pydantic.EmailStr разрешенные длины строк составляют 64@63.63
USER_EMAIL_LEN: int = 64 + 63 + 63
USER_HASH_PASS_LEN: int = 256
USER_PHONE_LEN: int = 20
USER_TELEGRAM_LEN: int = 32
USER_USERNAME_LEN: int = 25


class User(Base):
    """Декларативная модель представления пользователя."""

    __tablename__ = TABLE_USER
    __tableargs__ = {
        'comment': 'Пользователи',
    }

    account_balance: Mapped[int] = mapped_column(
        comment='остаток средств на балансе',
        server_default='0'
    )
    # INFO: нужно подтверждение.
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
    products: Mapped[List['Product']] = relationship(  # noqa (F821)
        back_populates='seller',
    )
    reg_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время регистрации',
        server_default=func.now(),
    )
    # INFO: нужно подтверждение.
    telegram_username: Mapped[str] = mapped_column(
        String(length=USER_TELEGRAM_LEN),
        comment='telegram профиль',
        nullable=True,
    )

    def __str__(self) -> str:
        return self.email
