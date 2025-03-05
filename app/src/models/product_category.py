"""
Модуль с ORM моделями базы данных приложения "product".
"""

from sqladmin import ModelView
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
from src.validators.product_category import ProductCategoryParams


class ProductCategory(Base):
    """Декларативная модель представления категорий товаров."""

    __tablename__ = TableNames.product_category
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
        String(length=ProductCategoryParams.TITLE_LEN_MAX),
        comment='название',
    )

    # Foreign Keys
    head_category_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{TableNames.product_category}.id',
            name=f'{TableNames.product_category}_{TableNames.product_category}_fkey',
            ondelete='CASCADE',
        ),
        comment='ID родительской категории',
        nullable=True,
        server_default=expression.null(),
    )

    # Relationships
    head_category: Mapped['ProductCategory'] = relationship(
        'ProductCategory',
        back_populates='subcategories',
        remote_side='ProductCategory.id',
    )
    subcategories: Mapped[list['ProductCategory']] = relationship(
        'ProductCategory',
        back_populates='head_category',
        cascade='all, delete',
    )


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
        (ProductCategory.id, True),
    ]
    column_list = (
        'id',
        'title',
        'head_category',
    )
    column_searchable_list = (
        ProductCategory.id,
        ProductCategory.title,
        ProductCategory.head_category,
    )
    column_sortable_list = (
        ProductCategory.id,
        ProductCategory.title,
        ProductCategory.head_category,
    )

    # Details page.
    column_details_list = (
        'id',
        'title',
        'head_category',
        'subcategories',
    )

    # Other.
    pk_columns = (ProductCategory.id,)
    is_async = True
