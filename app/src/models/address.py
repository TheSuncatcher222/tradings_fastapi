"""
Модуль с ORM моделями базы данных стран и адресов.
"""

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import expression

from src.database.database import (
    Base,
    TableNames,
)

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

    __tablename__ = TableNames.address

    # Primary keys
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # Fields
    apartment: Mapped[int] = mapped_column(
        comment='номер квартиры',
        server_default=expression.null(),
    )
    building: Mapped[str] = mapped_column(
        String(length=ADDRESS_BUILDING_LEN),
        comment='номер дома',
    )
    city: Mapped[str] = mapped_column(
        String(length=ADDRESS_CITY_LEN),
        comment='название города',
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
    street: Mapped[str] = mapped_column(
        String(length=ADDRESS_STREET_LEN),
        comment='название улицы',
    )
    zip_code: Mapped[str] = mapped_column(
        String(length=ADDRESS_ZIP_CODE_LEN),
        comment='почтовый индекс',
    )

    # Foreign keys
    country_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{TableNames.country}.id',
            name=f'{TableNames.address}_{TableNames.country}_fkey',
            ondelete='RESTRICT',
        ),
        comment='ID страны',
    )

    # Relationships
    country: Mapped['Country'] = relationship()
    user: Mapped['User'] = relationship(
        back_populates='address',
    )

    def __str__(self) -> str:
        parts = [
            f'{self.zip_code}',
            f'{self.country.title_rus}',
            f'г. {self.city}',
            f'ул. {self.street}',
            f'д. {self.building}',
        ]
        if self.entrance:
            parts.append(f'парадная {self.entrance}')
        if self.floor:
            parts.append(f'этаж {self.floor}')
        if self.apartment:
            parts.append(f'кв. {self.apartment}')
        return ', '.join(parts)


class Country(Base):
    """Декларативная модель представления страны."""

    __tablename__ = TableNames.country
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
    title_eng: Mapped[str] = mapped_column(
        String(length=COUNTRY_NAME_ENG_LEN),
        comment='страна на английском',
    )
    title_rus: Mapped[str] = mapped_column(
        String(length=COUNTRY_NAME_RUS_LEN),
        comment='название страны на русском',
    )

    def __str__(self) -> str:
        return self.code
