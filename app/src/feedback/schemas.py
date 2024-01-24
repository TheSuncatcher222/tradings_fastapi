"""
Модуль со схемами валидации данных через Pydantic в приложении "feedback".
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, validator

from src.auth.schemas import TELEGRAM_USERNAME_LEN_MAX
from src.feedback.models import FEEDBACK_MESSAGE_LEN
from src.users.models import USER_USERNAME_LEN

FEEDBACK_CONTACT_LEN: int = TELEGRAM_USERNAME_LEN_MAX + len('https://t.me/')


class FeedbackSend(BaseModel):
    """Схема представления формы обратной связи пользователей."""

    name: str
    email: EmailStr
    contacts: Optional[str] = None
    message: str
    data_process_approve: bool

    @validator('name')
    def validate_name(cls, value: str) -> str:
        """Производит валидацию поля 'name'."""
        value_len: int = len(value)
        if value_len > USER_USERNAME_LEN:
            raise ValueError(
                f'Имя превышает допустимую длину в  {USER_USERNAME_LEN} символов '
                f'(сейчас {value_len} символов)'
            )
        return value

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Переводит символы поля email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return value.lower()

    @validator('contacts')
    def validate_contacts(cls, value: str) -> str:
        """
        Производит валидацию поля 'contacts'.

        Производит проверку только по длине.
        """
        if value is not None and len(value) > FEEDBACK_CONTACT_LEN:
            raise ValueError('Укажите корректные контактные данные')
        return value

    @validator('message')
    def validate_message(cls, value: str) -> str:
        """Производит валидацию поля 'message'."""
        value_len: int = len(value)
        if value_len > FEEDBACK_MESSAGE_LEN:
            raise ValueError(
                f'Текст обращения превышает {FEEDBACK_MESSAGE_LEN} символов '
                f'(сейчас {value_len})'
            )
        return value

    @validator('data_process_approve')
    def validate_data_process_approve(cls, value: bool) -> str:
        """Производит валидацию поля 'data_process_approve'."""
        if not value:
            raise ValueError(
                'Для отправки обращения необходимо согласиться '
                'с обработкой персональных данных'
            )
        return value
