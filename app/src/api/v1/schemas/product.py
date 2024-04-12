"""
Модуль со схемами валидации данных через Pydantic в приложении "product".
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.api.v1.schemas.user import UserRepresent

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
    salesman: UserRepresent
