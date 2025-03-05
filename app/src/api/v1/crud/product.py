"""Модуль с классом CRUD запросов в базу данных для модели Product."""

from src.database.base_async_crud import BaseAsyncCrud
from src.models.product import Product


class ProductV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице Product."""


product_v1_crud = ProductV1Crud(
    model=Product,
    # INFO. У разных продавцов могут быть одинаковые товары и/или их названия.
    #       Но у одного продавца не должно быть товаров с одинаковыми названиями.
    unique_columns=('title', 'salesman_id'),
)
