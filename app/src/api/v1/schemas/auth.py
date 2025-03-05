"""
Модуль со схемами валидации данных через Pydantic в приложении "auth".
"""

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationInfo,
    field_validator,
)

from src.validators.user import (
    validate_user_email,
    validate_user_new_password,
    validate_user_new_password_confirm,
    validate_user_password,
)


class AuthLoginSchema(BaseModel):
    """Схема представления данных для авторизации пользователя."""

    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        """Переводит символы поля email в нижний регистр."""
        return validate_user_email(value=value)


class AuthPasswordChangeSchema(BaseModel):
    """Схема представления данных для смены текущего пароля пользователя."""

    password: str
    new_password: str
    new_password_confirm: str

    @field_validator('new_password')
    def validate_new_password(cls, value: str, info: ValidationInfo) -> str:
        """Производит валидацию поля 'new_password'."""
        return validate_user_new_password(value=value, current_password=info.data.get('password'))

    @field_validator('new_password_confirm')
    def validate_new_password_confirm(cls, value: str, info: ValidationInfo) -> str:
        """Производит валидацию поля 'new_password_confirm'."""
        return validate_user_new_password_confirm(value=value, new_password=info.data.get('new_password'))


class AuthPasswordResetSchema(BaseModel):
    """
    Схема представления данных для первого этапа
    восстановления пароля: отправка сообщения на почту.
    """

    email: EmailStr

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Переводит символы поля email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_user_email(value=value)


class AuthPasswordResetConfirmSchema(BaseModel):
    """
    Схема представления данных для второго этапа
    восстановления пароля: смена пароля пользователя.
    """

    reset_token: str
    new_password: str
    new_password_confirm: str

    @field_validator('new_password')
    def validate_new_password(cls, value: str) -> str:
        """Производит валидацию поля 'new_password'."""
        return validate_user_password(value=value)

    @field_validator('new_password_confirm')
    def validate_new_password_confirm(cls, value: str, info: ValidationInfo) -> str:
        """Производит валидацию поля 'new_password_confirm'."""
        return validate_user_new_password_confirm(value=value, new_password=info.data.get('new_password'))


class JwtTokenAccessRepresentSchema(BaseModel):
    """Схема представления JWT токена доступа."""

    access: str
