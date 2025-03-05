"""
Модуль с ORM моделями базы данных приложения "user".
"""

from datetime import (
    date,
    datetime,
)
from decimal import Decimal
from typing import (
    Optional,
    TYPE_CHECKING,
)

from sqladmin import ModelView
from sqlalchemy import (
    Date,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import (
    expression,
    func,
)

from src.database.database import (
    Base,
    TableNames,
)
from src.validators.user import (
    CompanyParams,
    UserBankCardParams,
    UserParams,
)

if TYPE_CHECKING:
    from src.models.address import Address
    from src.models.product import Product


class User(Base):
    """Декларативная модель представления пользователя."""

    __tablename__ = TableNames.user
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
        String(length=UserParams.EMAIL_LEN_MAX),
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
    name_first: Mapped[str] = mapped_column(
        String(length=UserParams.NAME_LEN_MAX),
        comment='имя',
    )
    name_last: Mapped[str] = mapped_column(
        String(length=UserParams.NAME_LEN_MAX),
        comment='фамилия',
    )
    password_hashed: Mapped[Optional[str]] = mapped_column(
        String(length=UserParams.PASSWORD_HASHED_LEN_MAX),
        comment='хэш пароля',
    )
    phone: Mapped[str] = mapped_column(
        String(length=UserParams.PHONE_LEN_MAX),
        comment='номер телефона',
        nullable=True,
        server_default=expression.null(),
    )
    phone_is_confirmed: Mapped[bool] = mapped_column(
        comment='Статус подтвержденного номера телефона',
        server_default=expression.false(),
    )
    datetime_registration: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment='дата и время регистрации',
        server_default=func.now(),
    )

    # Foreign keys
    address_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            column=f'{TableNames.address}.id',
            name=f'{TableNames.user}_{TableNames.address}_fkey',
            ondelete='RESTRICT',
        ),
        comment='ID адреса',
        nullable=True,
        server_default=expression.null(),
    )
    user_salesman_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            column=f'{TableNames.user_salesman}.id',
            name=f'{TableNames.user}_{TableNames.user_salesman}_fkey',
            ondelete='RESTRICT',
        ),
        comment='ID продавца',
        nullable=True,
        server_default=expression.null(),
    )

    # Relationship
    address: Mapped['Address'] = relationship(
        'Address',
        back_populates='user',
    )
    bank_cards: Mapped[list['UserBankCard']] = relationship(
        'UserBankCard',
        back_populates='user',
    )
    products: Mapped[list['Product']] = relationship(
        'Product',
        back_populates='salesman',
    )
    user_salesman: Mapped['UserSalesman'] = relationship(
        'UserSalesman',
        back_populates='user',
    )

    @property
    def get_full_name(self) -> str:
        """Возвращает имя и фамилию пользователя."""
        return f'{self.name_first} {self.name_last}'

    def __str__(self) -> str:
        return f'{self.email} ({self.name_first} {self.name_last})'


class UserBankCard(Base):
    """Декларативная модель представления банковских карт пользователя."""

    __tablename__ = TableNames.user_bank_card
    __tableargs__ = {
        'comment': 'Банковские карты',
    }

    # Primary keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Columns
    card_number: Mapped[str] = mapped_column(
        String(length=UserBankCardParams.NUMBER_LEN_MAX),
        comment='номер',
    )
    expiration_date: Mapped[date] = mapped_column(
        Date(),
        comment='дата окончания срока действия',
    )
    cardholder: Mapped[str] = mapped_column(
        String(length=UserBankCardParams.CARDHOLDER_LEN_MAX),
        comment='имя владельца',
    )
    is_main: Mapped[bool] = mapped_column(
        comment='статус основной',
        server_default=expression.false(),
    )
    title: Mapped[str] = mapped_column(
        String(length=UserBankCardParams.TITLE_LEN_MAX),
        comment='название',
    )

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{TableNames.user}.id',
            name=f'{TableNames.user_bank_card}_{TableNames.user}_fkey',
            ondelete='CASCADE',
        ),
        comment='ID пользователя',
    )

    # Relationship
    user: Mapped['User'] = relationship(
        'User',
        back_populates='bank_cards',
    )


class UserSalesman(Base):
    """Декларативная модель представления продавца."""

    __tablename__ = TableNames.user_salesman

    # Primary keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Fields
    company_name: Mapped[str] = mapped_column(
        String(length=CompanyParams.NAME_LEN_MAX),
        comment='название компании',
    )
    description: Mapped[str] = mapped_column(
        String(length=CompanyParams.DESCRIPTION_LEN_MAX),
        comment='описание компании',
        nullable=True,
        server_default=expression.null(),
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(length=CompanyParams.IMAGE_LEN_MAX),
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
        'datetime_registration',
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
        User.datetime_registration,
        User.is_active,
        User.user_salesman_id,
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
        'datetime_registration',
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
        (UserSalesman.id, True),
    ]
    column_list = (
        'id',
        'user',
        'company_name',
        'is_verified',
        'rating',
    )
    column_searchable_list = (
        UserSalesman.id,
        UserSalesman.company_name,
    )
    column_sortable_list = (
        UserSalesman.id,
        UserSalesman.company_name,
        UserSalesman.is_verified,
        UserSalesman.rating,
    )

    # Details page.
    column_details_list = (
        'id',
        'user',
        'company_name',
        'description',
        'image',
        'is_verified',
        'rating',
    )

    # Other.
    pk_columns = (UserSalesman.id,)
    is_async = True
