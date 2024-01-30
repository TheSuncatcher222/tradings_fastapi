"""
Модуль с ORM моделями базы данных приложения "product".
"""

from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import TABLE_PRODUCT, TABLE_PRODUCT_CATEGORY

PRODUCT_TITLE_LEN: int = 50
PRODUCT_DESCRIPTION_LEN: int = 200

PRODUCT_CATEGORY_TITLE_LEN: int = 50


class Base(DeclarativeBase):
    """Инициализирует фабрику создания декларативных классов моделей."""
    pass


class Product(Base):
    """Декларативная модель представления товаров."""

    __tablename__ = TABLE_PRODUCT
    __tableargs__ = {
        'comment': 'Товары',
    }

    category: Mapped['ProductCategory'] = relationship(
        back_populates='product',
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey(f'{TABLE_PRODUCT_CATEGORY}.id'),
        comment='id категории товаров'
    )
    description: Mapped[str] = mapped_column(
        String(length=PRODUCT_DESCRIPTION_LEN),
        comment='описание',
    )
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )
    # TODO: защитить от значения менее 0.
    in_stock: Mapped[int] = mapped_column(
        comment='в наличии',
    )
    price: Mapped[int] = mapped_column(
        comment='цена',
    )
    title: Mapped[str] = mapped_column(
        String(length=PRODUCT_TITLE_LEN),
        comment='название',
    )


class ProductCategory(Base):
    """Декларативная модель представления категорий товаров."""

    __tablename__ = TABLE_PRODUCT_CATEGORY
    __tableargs__ = {
        'comment': 'Категории товаров',
    }

    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(
        String(length=PRODUCT_CATEGORY_TITLE_LEN),
        comment='название',
    )
    product: Mapped[List['Product']] = relationship(
        back_populates='category',
    )
