"""
Модуль с ORM моделями базы данных приложения "user".
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

from sqladmin import ModelView
from sqlalchemy import DateTime, DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression, func

from src.database.database import Base, table_names
from src.validators.user import (
    USER_EMAIL_LEN,
    USER_HASH_PASS_LEN,
    USER_PHONE_LEN,
    USER_USERNAME_LEN,

    USER_SALESMAN_COMPANY_DESCRIPTION_LEN,
    USER_SALESMAN_COMPANY_IMAGE_LEN,
    USER_SALESMAN_COMPANY_NAME_LEN,
)

if TYPE_CHECKING:
    from src.models.product import Product


class User(Base):
    """Декларативная модель представления пользователя."""

    __tablename__ = table_names.user
    __tableargs__ = {
        'comment': 'Пользователи',
    }

    # Primary keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Columns
    email: Mapped[str] = mapped_column(
        String(length=USER_EMAIL_LEN),
        comment='email',
        unique=True,
    )
    email_is_confirmed: Mapped[bool] = mapped_column(
        comment='Статус подтвержденной почты',
        server_default=expression.false(),
    )
    is_active: Mapped[bool] = mapped_column(
        comment='статус активного',
        server_default=expression.true(),
    )
    is_admin: Mapped[bool] = mapped_column(
        comment='статус администратора',
        server_default=expression.false(),
    )
    is_salesman: Mapped[bool] = mapped_column(
        comment='статус продавца',
        server_default=expression.false(),
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(length=USER_HASH_PASS_LEN),
        comment='хэш пароля',
    )
    name_first: Mapped[str] = mapped_column(
        String(length=USER_USERNAME_LEN),
        comment='имя',
    )
    name_last: Mapped[str] = mapped_column(
        String(length=USER_USERNAME_LEN),
        comment='фамилия',
    )
    # TODO: сделать поле phonenumber.
    phone: Mapped[str] = mapped_column(
        String(length=USER_PHONE_LEN),
        comment='номер телефона',
        nullable=True,
        server_default=expression.null(),
    )
    phone_is_confirmed: Mapped[bool] = mapped_column(
        comment='Статус подтвержденного номера телефона',
        server_default=expression.false(),
    )
    registration_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время регистрации',
        server_default=func.now(),
    )

    # Relations
    products: Mapped[list['Product']] = relationship(
        'Product',
        back_populates='salesman',
    )
    user_salesman: Mapped['UserSalesman'] = relationship(
        back_populates='user',
    )

    @property
    def get_full_name(self) -> str:
        """Возвращает имя и фамилию пользователя."""
        return f'{self.name_first} {self.name_last}'

    def __str__(self) -> str:
        return f'{self.email} ({self.name_first} {self.name_last})'


class UserSalesman(Base):
    """Декларативная модель представления продавца."""

    __tablename__ = table_names.user_salesman

    # Primary keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{table_names.user}.id',
            ondelete='CASCADE',
        ),
        comment='ID пользователя-продавца',
        primary_key=True,
    )

    # Fields
    company_name: Mapped[str] = mapped_column(
        String(length=USER_SALESMAN_COMPANY_NAME_LEN),
        comment='название компании',
    )
    description: Mapped[str] = mapped_column(
        String(length=USER_SALESMAN_COMPANY_DESCRIPTION_LEN),
        comment='описание компании',
        nullable=True,
        server_default=expression.null(),
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(length=USER_SALESMAN_COMPANY_IMAGE_LEN),
        comment='изображение компании',
        nullable=True,
        server_default=expression.null(),
    )
    is_verified: Mapped[bool] = mapped_column(
        comment='статус верификации',
        server_default=expression.false(),
    )
    rating: Mapped[Decimal] = mapped_column(
        # INFO. Рейтинг имеет формат "5.00".
        DECIMAL(precision=3, scale=2),
        comment='рейтинг',
        server_default=expression.func.cast(0.00, DECIMAL(3, 2)),
    )

    # Relations
    user: Mapped['User'] = relationship(
        back_populates='user_salesman',
    )


"""SQLAdmin."""


class UserAdmin(ModelView, model=User):

    # Metadata.
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    category = 'Пользователи'

    # Permissions.
    can_create = True
    can_view_details = True
    can_export = True
    can_edit = True
    can_delete = True

    # Pagination options.
    page_size = 25
    page_size_options = (
        25,
        50,
        100,
        200,
    )

    # List page.
    column_default_sort = [
        (User.id, True),
    ]
    column_list = (
        'id',
        'name_first',
        'name_last',
        'email',
        'phone',
        'registration_datetime',
        'is_active',
        'is_salesman',
    )
    column_searchable_list = (
        User.id,
        User.name_first,
        User.name_last,
        User.email,
        User.phone,
    )
    column_sortable_list = (
        User.id,
        User.name_first,
        User.name_last,
        User.email,
        User.phone,
        User.registration_datetime,
        User.is_active,
        User.is_salesman,
    )

    # Details page.
    column_details_list = (
        'id',
        'name_first',
        'name_last',
        'email',
        'email_is_confirmed',
        'phone',
        'phone_is_confirmed',
        'registration_datetime',
        'is_active',
        'is_admin',
        'is_salesman',
        'user_salesman',
    )

    # Other.
    pk_columns = (User.id,)
    is_async = True


class UserSalesmanAdmin(ModelView, model=UserSalesman):

    # Metadata.
    name = 'Продавец'
    name_plural = 'Продавцы'
    icon = 'fa-solid fa-user-tie'
    category = 'Пользователи'

    # Permissions.
    can_create = True
    can_view_details = True
    can_export = True
    can_edit = True
    can_delete = True

    # Pagination options.
    page_size = 25
    page_size_options = (
        25,
        50,
        100,
        200,
    )

    # List page.
    column_default_sort = [
        (UserSalesman.user_id, True),
    ]
    column_list = (
        'user_id',
        'user',
        'company_name',
        'is_verified',
        'rating',
    )
    column_searchable_list = (
        UserSalesman.user_id,
        UserSalesman.company_name,
    )
    column_sortable_list = (
        UserSalesman.user_id,
        UserSalesman.company_name,
        UserSalesman.is_verified,
        UserSalesman.rating,
    )

    # Details page.
    column_details_list = (
        'user_id',
        'user',
        'company_name',
        'description',
        'image',
        'is_verified',
        'rating',
    )

    # Other.
    pk_columns = (UserSalesman.user_id,)
    is_async = True
