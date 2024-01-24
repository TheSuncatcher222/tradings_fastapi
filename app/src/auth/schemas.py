"""
Модуль со схемами валидации данных через Pydantic в приложении "auth".
"""

from re import fullmatch
from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.users.models import USER_USERNAME_LEN

NL: str = '\n'

USER_PASS_RAW_LEN_MAX: int = 50
USER_PASS_RAW_LEN_MIN: int = 8
PASS_SPECIAL_CHARS: str = '!_@#$%^&+='

PASS_CHARS_VALIDATORS: dict[str, str] = {
    lambda s: USER_PASS_RAW_LEN_MIN <= len(s) <= USER_PASS_RAW_LEN_MAX: f'{NL}- длина от {USER_PASS_RAW_LEN_MIN} до {USER_PASS_RAW_LEN_MAX} символов',
    lambda s: any(char.isdigit() for char in s): '\n- включает хотя бы одну цифру (0-9)',
    lambda s: any(char.islower() for char in s): '\n- включает хотя бы одну прописную букву (a-z)',
    lambda s: any(char.isupper() for char in s): '\n- включает хотя бы одну заглавную букву (A-Z)',
    lambda s: any(char in PASS_SPECIAL_CHARS for char in s): f'{NL}- включает хотя бы один специальный символ ({PASS_SPECIAL_CHARS})',
}

TELEGRAM_USERNAME_LEN_MIN: int = 5
TELEGRAM_USERNAME_LEN_MAX: int = 32
TELEGRAM_USERNAME_SPECIAL_CHARS: str = '!_@#$%^&+='
TELEGRAM_USERNAME_REG_EXP: str = r'^[a-zA-Z](?!.*__)[a-zA-Z0-9_]{3,29}[a-zA-Z0-9]$'


class AuthLogin(BaseModel):
    """Схема представления данных для авторизации пользователя."""

    email: str
    password: str

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """Переводит символы поля email в нижний регистр."""
        return value.lower()


class AuthRegister(BaseModel):
    """Схема представления данных для регистрации пользователя."""

    # TODO: добавить валидатор.
    name_first: str
    # TODO: добавить валидатор.
    name_last: str
    email: EmailStr
    # TODO: использовать "pip install pydantic-extra-types".
    phone: Optional[PhoneNumber] = None
    # TODO: добавить валидатор.
    telegram_username: Optional[str] = None
    password: str

    @validator('name_first')
    def validate_name_first(cls, value: str) -> str:
        """
        Производит валидацию поля 'name_first'.

        Переводит символы поля в title регистр.
        """
        value_len: int = len(value)
        if value_len > USER_USERNAME_LEN:
            raise ValueError(
                f'Имя превышает допустимую длину в {USER_USERNAME_LEN} символов'
                f'(сейчас {value_len} символов)'
            )
        return value.title()

    @validator('name_last')
    def validate_name_last(cls, value: str) -> str:
        """
        Производит валидацию поля 'name_last'.

        Переводит символы поля в title регистр.
        """
        value_len: int = len(value)
        if value_len > USER_USERNAME_LEN:
            raise ValueError(
                f'Фамилия превышает допустимую длину в {USER_USERNAME_LEN} символов'
                f'(сейчас {value_len} символов)'
            )
        return value.title()

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Переводит символы поля email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return value.lower()

    @validator('password')
    def validate_password(cls, value: str) -> str:
        """Производит валидацию поля 'password'."""
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

    @validator('phone')
    def validate_phone(cls, value: str) -> str:
        """Производит валидацию поля 'phone'."""
        if value.startswith('8'):
            value: str = '+7' + value[1:]
        return value

    @validator('telegram_username')
    def validate_telegram_username(cls, value: str) -> str:
        """Производит валидацию поля 'telegram_username'."""
        if fullmatch(pattern=TELEGRAM_USERNAME_REG_EXP, string=value) is None:
            raise ValueError(
                'Введите корректное имя пользователя Telegram'
            )
        return value


class JwtTokenAccess(BaseModel):
    """Схема представления JWT токена доступа."""

    access: str


class JwtTokenRefresh(BaseModel):
    """Схема представления JWT токена обновления."""

    refresh: str
