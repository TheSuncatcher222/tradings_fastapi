"""
Модуль со схемами валидации данных через Pydantic в приложении "user".
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator,
)

from src.validators.user import (
    UserParams,
    validate_user_company_name,
    validate_user_email,
    validate_user_password,
    validate_user_phone,
    validate_user_name,
)


class UserRepresent(BaseModel):
    """Схема представления пользователя."""

    name_first: str
    name_last: str
    email: EmailStr
    email_is_confirmed: bool
    phone: Optional[str]
    phone_is_confirmed: bool
    datetime_registration: datetime


class UserUpdate(BaseModel):
    """Схема обновления пользователя."""

    name_first: Optional[str] = None
    name_last: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @field_validator('name_first')
    def validate_name_first(cls, value: str) -> str:
        """
        Производит валидацию поля "name_first".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=UserParams.NAME_FIRST_ERROR)

    @field_validator('name_last')
    def validate_name_last(cls, value: str) -> str:
        """
        Производит валидацию поля "name_last".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=UserParams.NAME_LAST_ERROR)

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Производит валидацию поля "email".

        Переводит символы email в нижний регистр.

        Валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_user_email(value=value)

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        """Производит валидацию поля "phone"."""
        return validate_user_phone(value=value)


class UserRegisterSchema(BaseModel):
    """Схема представления данных для регистрации пользователя."""

    name_first: str
    name_last: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    is_salesman: Optional[bool] = False
    company_name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    @field_validator('name_first')
    def validate_name_first(cls, value: str) -> str:
        """
        Производит валидацию поля "name_first".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=UserParams.NAME_FIRST_ERROR)

    @field_validator('name_last')
    def validate_name_last(cls, value: str) -> str:
        """
        Производит валидацию поля "name_last".

        Переводит символы поля в title регистр.
        """
        return validate_user_name(value=value, err=UserParams.NAME_LAST_ERROR)

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        """
        Производит валидацию поля "email":
            - переводит символы поля email в нижний регистр.
            - валидация структуры email осуществляется автоматически в Pydantic.
        """
        return validate_user_email(value=value)

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        """Производит валидацию поля "password"."""
        return validate_user_password(value=value)

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        """
        Производит валидацию поля "phone":
            - необходимо сохранять только цифры (т.е. без "+", " ", "-", "(", ")")
            - для абонентов российских операторов необходимо начинать номер с 7, а не 8

        Валидное значение: 79112223344.
        Невалидное значение по всем критериям: +7 (911) 222-33-44.
        """
        return validate_user_phone(value=value)

    @field_validator('company_name')
    def validate_company_name(cls, value: str, values: dict) -> str:
        """
        Производит валидацию поля "company_name".

        Валидация производится только в том случа,
        если поле "is_salesman" равно True.
        """
        if not values.get('is_salesman'):
            return None
        return validate_user_company_name(value=value)

    @field_validator('description')
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
                'Введите адрес компании',
            )
        return value

    @field_validator('image')
    def validate_image(cls, value: str, values: dict) -> None:
        """
        Производит валидацию поля "image".

        Валидация производится только в том случа,
        если поле "is_salesman" равно True.
        """
        if not values.get('is_organization'):
            return None
        return None

    @model_validator(mode='before')
    def validate_is_organization(cls, self: dict) -> dict:
        """
        Производит валидацию поля "is_salesman"
        и связанных с ним полей "company_name" и "description".
        """
        if not all([self.get(key) for key in ('company_name', 'description')]):
            raise ValueError(
                'Не заполнены все обязательные поля для организации: "company_name", "description"',
            )
        return True


class UserSalesmanCompanyForProductRepresent(BaseModel):
    """Схема представления данных компании продавца в запросах к Product."""

    company_name: str
    image: str | None = None
    rating: Decimal


class UserSalesmanRepresentForProduct(BaseModel):
    """Схема представления пользователя в запросах к Product."""

    name_first: str
    name_last: str
    email: EmailStr
    company: UserSalesmanCompanyForProductRepresent
