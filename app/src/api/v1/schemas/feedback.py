"""
Модуль со схемами валидации данных через Pydantic в приложении "feedback".
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, validator

from src.validators.feedback import (
    validate_feedback_contacts,
    validate_feedback_data_process_approve,
    validate_feedback_email,
    validate_feedback_message,
    validate_feedback_username,
    validate_ticket_subject,
    validate_ticket_text,
)


class FeedbackSend(BaseModel):
    """Схема отправки формы обратной связи пользователей."""

    username: str
    email: EmailStr
    contacts: Optional[str] = None
    message: str
    data_process_approve: bool

    @validator('username')
    def validate_username(cls, value: str) -> str:
        """Производит валидацию поля 'username'."""
        return validate_feedback_username(value=value)

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Переводит символы поля email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_feedback_email(value=value)

    @validator('contacts')
    def validate_contacts(cls, value: str) -> str:
        """
        Производит валидацию поля 'contacts'.

        Производит проверку только по длине.
        """
        return validate_feedback_contacts(value=value)

    @validator('message')
    def validate_message(cls, value: str) -> str:
        """Производит валидацию поля 'message'."""
        return validate_feedback_message(value=value)

    @validator('data_process_approve')
    def validate_data_process_approve(cls, value: bool) -> str:
        """Производит валидацию поля 'data_process_approve'."""
        return validate_feedback_data_process_approve(value=value)


class TicketRepresent(BaseModel):
    """Схема представления тикета пользователя в поддержку."""

    subject: str
    text: str
    attachments: list[Optional[str]] = []


class TicketSend(BaseModel):
    """Схема представления отправки тикета пользователя в поддержку."""

    subject: str
    text: str

    @validator('subject')
    def validate_subject(cls, value: str) -> str:
        """Производит валидацию поля 'subject'."""
        return validate_ticket_subject(value=value)

    @validator('text')
    def validate_text(cls, value: str) -> str:
        """Производит валидацию поля 'text'."""
        return validate_ticket_text(value=value)
