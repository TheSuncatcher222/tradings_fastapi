"""
Модуль со схемами валидации данных через Pydantic в приложении "feedback".
"""

from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)

from src.validators.feedback import (
    validate_feedback_contacts,
    validate_feedback_email,
    validate_feedback_message,
    validate_feedback_username,
)


class FeedbackSend(BaseModel):
    """Схема отправки формы обратной связи пользователей."""

    username: str
    email: EmailStr
    contacts: Optional[str] = None
    message: str

    @field_validator('username')
    def validate_username(cls, value: str) -> str:
        """Производит валидацию поля 'username'."""
        return validate_feedback_username(value=value)

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Переводит символы поля email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_feedback_email(value=value)

    @field_validator('contacts')
    def validate_contacts(cls, value: str) -> str:
        """
        Производит валидацию поля 'contacts'.

        Производит проверку только по длине.
        """
        return validate_feedback_contacts(value=value)

    @field_validator('message')
    def validate_message(cls, value: str) -> str:
        """Производит валидацию поля 'message'."""
        return validate_feedback_message(value=value)


class TicketRepresent(BaseModel):
    """Схема представления тикета пользователя в поддержку."""

    subject: str
    text: str
    attachments: list[Optional[str]] = []
