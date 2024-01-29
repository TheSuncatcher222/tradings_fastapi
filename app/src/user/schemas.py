"""
Модуль со схемами валидации данных через Pydantic в приложении "user".
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRepresent(BaseModel):
    """Схема представления пользователя."""

    id: int
    name_first: str
    name_last: str
    email: EmailStr
    phone: Optional[str] = None
    telegram_username: Optional[str] = None
    account_balance: int
    reg_date: datetime
