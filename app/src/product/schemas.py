"""
Модуль со схемами валидации данных через Pydantic в приложении "product".
"""

from pydantic import BaseModel


class ProductCategorySchema(BaseModel):
    """Схема представления категорий товаров."""

    id: int
    title: str


class ProductSchema(BaseModel):
    """Схема представления товаров."""

    id: int
    title: str
    price: int
    in_stock: int
    category: ProductCategorySchema
    description: str
