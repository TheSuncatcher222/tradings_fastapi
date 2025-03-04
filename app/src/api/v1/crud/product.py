"""Модуль с классом CRUD запросов в базу данных для модели Product."""

from src.database.base_async_crud import BaseAsyncCrud
from src.models.product import (
    Product,
    ProductSubCategory,
)


class ProductSubCategoryV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице ProductSubCategory."""


product_sub_category_v1_crud = ProductSubCategoryV1Crud(
    model=ProductSubCategory,
    object_not_found_err='Подкатегория товаров не найдена',
    unique_columns=('title', 'product_category_id'),
    unique_columns_err='Такая подкатегория в категории уже существует',
)


class ProductV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице Product."""


product_v1_crud = ProductV1Crud(
    model=Product,
    # INFO. У разных продавцов могут быть одинаковые товары и/или их названия.
    #       Но у одного продавца не должно быть товаров с одинаковыми названиями.
    unique_columns=('title', 'salesman_id'),
)
