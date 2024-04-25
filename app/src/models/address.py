"""
Модуль с ORM моделями базы данных стран и адресов.
"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from src.database.database import Base, table_names

ADDRESS_BUILDING_LEN: int = 8
ADDRESS_CITY_LEN: int = 128
ADDRESS_STREET_LEN: int = 128
ADDRESS_ZIP_CODE_LEN: int = 16

COUNTRY_CODE_ENG_LEN: int = 3
COUNTRY_NAME_ENG_LEN: int = 32
COUNTRY_NAME_RUS_LEN: int = 32

if TYPE_CHECKING:
    from src.models.user import User


class Address(Base):
    """Декларативная модель представления адреса."""

    __tablename__ = table_names.address

    # Primary keys
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # Fields
    zip_code: Mapped[str] = mapped_column(
        String(length=ADDRESS_ZIP_CODE_LEN),
        comment='почтовый индекс',
    )
    country: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{table_names.country}.id',
            ondelete='RESTRICT',
        ),
        comment='ID страны',
    )
    city: Mapped[str] = mapped_column(
        String(length=ADDRESS_CITY_LEN),
        comment='название города',
    )
    street: Mapped[str] = mapped_column(
        String(length=ADDRESS_STREET_LEN),
        comment='название улицы',
    )
    building: Mapped[str] = mapped_column(
        String(length=ADDRESS_BUILDING_LEN),
        comment='номер дома',
    )
    entrance: Mapped[int] = mapped_column(
        comment='номер подъезда',
        nullable=True,
        server_default=expression.null(),
    )
    floor: Mapped[int] = mapped_column(
        comment='номер этажа',
        server_default=expression.null(),
    )
    apartment: Mapped[int] = mapped_column(
        comment='номер квартиры',
        server_default=expression.null(),
    )

    # Relationships
    user: Mapped['User'] = relationship(
        back_populates='address',
    )

    def __str__(self) -> str:
        address: str = (
            f'{self.zip_code}, '
            # TODO. Сделать через словарь поиск названия страны по ID.
            # f'{self.country}, '
            f'г. {self.city}, '
            f'ул. {self.street}, '
            f'д. {self.building}'
        )
        if self.entrance:
            address += f', парадная {self.entrance}'
        if self.floor:
            address += f', этаж {self.floor}'
        if self.apartment:
            address += f', кв. {self.apartment}'
        return address


class Country(Base):
    """Декларативная модель представления пользователя."""

    __tablename__ = table_names.country
    __tableargs__ = {
        'comment': 'Страны',
    }

    # Primary keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )
    code: Mapped[str] = mapped_column(
        String(length=3),
        comment='трехбуквенный код страны',
    )
    name_eng: Mapped[str] = mapped_column(
        String(length=COUNTRY_NAME_ENG_LEN),
        comment='страна на английском',
    )
    name_rus: Mapped[str] = mapped_column(
        String(length=COUNTRY_NAME_RUS_LEN),
        comment='название страны на русском',
    )

    def __str__(self) -> str:
        return self.name_rus
