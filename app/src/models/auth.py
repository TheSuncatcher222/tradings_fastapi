"""
Модуль с ORM моделями базы данных приложения "auth".
"""

from datetime import datetime, timedelta

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.config import settings
from src.database.database import Base, table_names

TOKEN_MAX_LEN: int = 256


class UsedPassResetToken(Base):
    """
    Декларативная модель представления однажды использованных
    токенов восстановления пароля.
    """

    __tablename__ = table_names.used_pass_reset_token
    __tableargs__ = {
        'comment': 'Использованные токены восстановления пароля'
    }

    exp_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время окончания срока жизни',
        default=datetime.now() + timedelta(seconds=settings.ONE_DAY_SEC)
    )
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )
    token: Mapped[str] = mapped_column(
        String(length=TOKEN_MAX_LEN),
        comment='токен',
    )
