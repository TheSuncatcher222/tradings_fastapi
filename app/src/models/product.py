"""
Модуль с ORM моделями базы данных приложения "product".
"""

from typing import (
    TYPE_CHECKING,
)

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

from src.database.database import (
    Base,
    TableNames,
)
from src.validators.product import ProductParams

if TYPE_CHECKING:
    from src.models.product_category import ProductCategory
    from src.models.user import User


class Product(Base):
    """Декларативная модель представления товаров."""

    __tablename__ = TableNames.product
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
        String(length=ProductParams.DESCRIPTION_LEN_MAX),
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
        String(length=ProductParams.TITLE_LEN_MAX),
        comment='название',
    )

    # Foreign Keys
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{TableNames.product_category}.id',
            name=f'{TableNames.product}_{TableNames.product_category}_fkey',
            ondelete='RESTRICT',
        ),
        comment='id под-категории товаров',
    )
    salesman_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=f'{TableNames.user}.id',
            name=f'{TableNames.product}_{TableNames.user}_fkey',
            ondelete='CASCADE',
        ),
        comment='id продавца',
    )

    # Relationships
    category: Mapped['ProductCategory'] = relationship(
        'ProductCategory',
    )
    salesman: Mapped['User'] = relationship(
        'User',
        back_populates='products',
    )


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
        Product.category,
    )
    column_sortable_list = (
        Product.id,
        Product.salesman,
        Product.title,
        Product.category,
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
