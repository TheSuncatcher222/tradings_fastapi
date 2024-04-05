"""
Модуль со схемами валидации данных через Pydantic в приложении "auth".
"""

from pydantic import BaseModel, EmailStr, validator

from src.api.v1.schemas.user import PASS_CHARS_VALIDATORS


class AuthLogin(BaseModel):
    """Схема представления данных для авторизации пользователя."""

    email: str
    password: str

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """Переводит символы поля email в нижний регистр."""
        return value.lower()


class AuthPasswordChange(BaseModel):
    """Схема представления данных для смены текущего пароля пользователя."""

    password: str
    new_password: str
    new_password_confirm: str

    @validator('new_password')
    def validate_new_password(cls, value: str, values: dict) -> str:
        """Производит валидацию поля 'new_password'."""
        if value == values.get('password'):
            raise ValueError(
                'Прежний и новый пароли должны отличаться'
            )
        errors: list[str] = [
            err_message
            for condition, err_message
            in PASS_CHARS_VALIDATORS.items()
            if not condition(value)
        ]
        if len(errors) > 0:
            raise ValueError(
                'Введите пароль, который удовлетворяет критериям:' +
                ''.join(errors)
            )
        return value

    @validator('new_password_confirm')
    def validate_new_password_confirm(cls, value: str, values: dict) -> str:
        """Производит валидацию поля 'new_password_confirm'."""
        if value != values.get('new_password'):
            raise ValueError(
                'Пароли не совпадают'
            )
        return value


class AuthPasswordReset(BaseModel):
    """
    Схема представления данных для первого этапа
    восстановления пароля: отправка сообщения на почту.
    """

    email: EmailStr

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Переводит символы поля email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return value.lower()


class AuthPasswordResetConfirm(BaseModel):
    """
    Схема представления данных для второго этапа
    восстановления пароля: смена пароля пользователя.
    """

    reset_token: str
    new_password: str
    new_password_confirm: str

    @validator('new_password')
    def validate_new_password(cls, value: str, values: dict) -> str:
        """Производит валидацию поля 'new_password'."""
        if value == values.get('password'):
            raise ValueError(
                'Прежний и новый пароли должны отличаться'
            )
        errors: list[str] = [
            err_message
            for condition, err_message
            in PASS_CHARS_VALIDATORS.items()
            if not condition(value)
        ]
        if len(errors) > 0:
            raise ValueError(
                'Введите пароль, который удовлетворяет критериям:' +
                ''.join(errors)
            )
        return value

    @validator('new_password_confirm')
    def validate_new_password_confirm(cls, value: str, values: dict) -> str:
        """Производит валидацию поля 'new_password_confirm'."""
        if value != values.get('new_password'):
            raise ValueError(
                'Пароли не совпадают'
            )
        return value


class JwtTokenAccess(BaseModel):
    """Схема представления JWT токена доступа."""

    access: str
