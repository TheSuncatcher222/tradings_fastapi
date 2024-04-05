"""
Модуль со схемами валидации данных через Pydantic в приложении "user".
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.src.validators.user import (
    validate_company_name,
    validate_email,
    validate_password,
    validate_phone, validate_user_name,
    USER_NAME_FIRST_ERROR,
    USER_NAME_LAST_ERROR,
)


class UserRepresent(BaseModel):
    """Схема представления пользователя."""

    name_first: str
    name_last: str
    email: EmailStr
    email_is_confirmed: bool
    phone: Optional[str]
    phone_is_confirmed: bool
    registration_datetime: datetime


class UserUpdate(BaseModel):
    """Схема обновления пользователя."""
    name_first: Optional[str] = None
    name_last: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @validator('name_first')
    def validate_name_first(cls, value: str) -> str:
        """
        Производит валидацию поля "name_first".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=USER_NAME_FIRST_ERROR)

    @validator('name_last')
    def validate_name_last(cls, value: str) -> str:
        """
        Производит валидацию поля "name_last".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=USER_NAME_LAST_ERROR)

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Производит валидацию поля "email".

        Переводит символы email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_email(value=value)

    @validator('phone')
    def validate_phone(cls, value: str) -> str:
        """Производит валидацию поля "phone"."""
        return validate_phone(value=value)


class UserRegister(BaseModel):
    """Схема представления данных для регистрации пользователя."""

    name_first: str
    name_last: str
    email: EmailStr
    phone: Optional[PhoneNumber] = None
    password: str
    is_salesman: Optional[bool] = False
    company_name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    @validator('name_first')
    def validate_name_first(cls, value: str) -> str:
        """
        Производит валидацию поля "name_first".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=USER_NAME_FIRST_ERROR)

    @validator('name_last')
    def validate_name_last(cls, value: str) -> str:
        """
        Производит валидацию поля "name_last".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=USER_NAME_LAST_ERROR)

    @validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Производит валидацию поля "email":
            - переводит символы поля email в нижний регистр.
            - валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_email(value=value)

    @validator('password')
    def validate_password(cls, value: str) -> str:
        """Производит валидацию поля "password"."""
        return validate_password(value=value)

    @validator('phone')
    def validate_phone(cls, value: str) -> str:
        """
        Производит валидацию поля "phone":
            - необходимо сохранять только цифры (т.е. без "+", " ", "-", "(", ")")
            - для абонентов российских операторов необходимо начинать номер с 7, а не 8

        Валидное значение: 79112223344.
        Невалидное значение по всем критериям: +7 (911) 222-33-44.
        """
        return validate_phone(value=value)

    @validator('company_name', always=True)
    def validate_company_name(cls, value: str, values: dict) -> str:
        """
        Производит валидацию поля "company_name".

        Валидация производится только в том случа,
        если поле "is_salesman" равно True.
        """
        if not values.get('is_salesman'):
            return None
        return validate_company_name(value=value)

    @validator('description', always=True)
    def validate_description(cls, value: str, values: dict) -> str:
        """
        Производит валидацию поля "description".

        Валидация производится только в том случа,
        если поле "is_salesman" равно True.
        """
        if not values.get('is_organization'):
            return None
        if value is None:
            raise ValueError(
                'Введите адрес компании'
            )
        return value

    # TODO. Добавить валидацию изображения.
    @validator('image', always=True)
    def validate_image(cls, value: str, values: dict) -> None:
        """
        Производит валидацию поля "image".

        Валидация производится только в том случа,
        если поле "is_salesman" равно True.
        """
        if not values.get('is_organization'):
            return None
        return None

    @validator('is_salesman')
    def validate_is_organization(cls, value: str, values: dict) -> bool:
        """
        Производит валидацию поля "is_salesman"
        и связанных с ним полей "company_name" и "description".
        """
        if not all([values.get(key) for key in ('company_name', 'description')]):
            raise ValueError(
                'Не заполнены все обязательные поля для организации: "company_name", "description"'
            )
        return True
