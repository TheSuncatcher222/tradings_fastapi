"""
Модуль с ORM моделями базы данных приложения "product".
"""

from typing import List, TYPE_CHECKING

from sqladmin import ModelView
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base, table_names
from src.validators.products import (
    PRODUCT_DESCRIPTION_LEN, PRODUCT_TITLE_LEN,
    PRODUCT_CATEGORY_TITLE_LEN,
)

if TYPE_CHECKING:
    from src.models.user import User


class Product(Base):
    """Декларативная модель представления товаров."""

    __tablename__ = table_names.product
    __tableargs__ = {
        'comment': 'Товары',
    }

    # Primary Keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Columns
    description: Mapped[str] = mapped_column(
        String(length=PRODUCT_DESCRIPTION_LEN),
        comment='описание',
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

    # Relationships
    sub_category: Mapped['ProductSubCategory'] = relationship(
        'ProductSubCategory',
        back_populates='products',
    )
    salesman: Mapped['User'] = relationship(
        'User',
        back_populates='products',
    )

    # Foreign Keys
    sub_category_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{table_names.product_sub_category}.product_category_id',
            ondelete='RESTRICT',
        ),
        comment='id под-категории товаров'
    )
    salesman_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{table_names.user}.id',
            ondelete='CASCADE',
        ),
        comment='id продавца',
    )


class ProductCategory(Base):
    """Декларативная модель представления категорий товаров."""

    __tablename__ = table_names.product_category
    __tableargs__ = {
        'comment': 'Категории товаров',
    }

    # Primary Keys
    id: Mapped[int] = mapped_column(
        comment='ID',
        primary_key=True,
    )

    # Columns
    title: Mapped[str] = mapped_column(
        String(length=PRODUCT_CATEGORY_TITLE_LEN),
        comment='название',
    )

    # Relationships
    product_sub_categories: Mapped['ProductSubCategory'] = relationship(
        'ProductSubCategory',
        back_populates='product_category',
    )


class ProductSubCategory(Base):
    """Декларативная модель представления под-категорий товаров."""

    __tablename__ = table_names.product_sub_category
    __tableargs__ = {
        'comment': 'Под-категории товаров',
    }

    # Primary Keys
    product_category_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{table_names.product_category}.id',
            ondelete='RESTRICT',
        ),
        comment='ID категории товаров',
        primary_key=True,
    )

    # Columns
    title: Mapped[str] = mapped_column(
        String(length=PRODUCT_CATEGORY_TITLE_LEN),
        comment='название',
    )

    # Relationships
    product_category: Mapped['ProductCategory'] = relationship(
        'ProductCategory',
        back_populates='product_sub_categories',
    )
    products: Mapped[List['Product']] = relationship(
        back_populates='sub_category',
    )


"""SQLAdmin."""


class ProductAdmin(ModelView, model=Product):

    # Metadata.
    name = 'Товар'
    name_plural = 'Товары'
    icon = 'fa-solid fa-cube'
    category = 'Товары'

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
        (Product.id, True),
    ]
    column_list = (
        'id',
        'salesman',
        'title',
        'category',
        'price',
        'in_stock',
    )
    column_searchable_list = (
        Product.id,
        Product.salesman,
        Product.title,
        Product.sub_category,
    )
    column_sortable_list = (
        Product.id,
        Product.salesman,
        Product.title,
        Product.sub_category,
        Product.price,
        Product.in_stock,
    )

    # Details page.
    column_details_list = (
        'id',
        'salesman',
        'title',
        'description',
        'sub_category',
        'price',
        'in_stock',
    )

    # Other.
    pk_columns = (Product.id,)
    is_async = True


class ProductCategoryAdmin(ModelView, model=ProductCategory):

    # Metadata.
    name = 'Категория товаров'
    name_plural = 'Категории товаров'
    icon = 'fa-solid fa-cubes'
    category = 'Товары'

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
        (Product.id, True),
    ]
    column_list = (
        'id',
        'title',
    )
    column_searchable_list = (
        ProductCategory.id,
        ProductCategory.title,
    )
    column_sortable_list = (
        ProductCategory.id,
        ProductCategory.title,
    )

    # Details page.
    column_details_list = (
        'id',
        'title',
    )

    # Other.
    pk_columns = (ProductCategory.id,)
    is_async = True
