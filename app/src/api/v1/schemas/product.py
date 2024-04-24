"""
Модуль со схемами валидации данных через Pydantic в приложении "product".
"""

from pydantic import BaseModel

from src.api.v1.schemas.user import UserSalesmanRepresentForProduct


class ProductCategorySchema(BaseModel):
    """Схема представления категорий товаров."""

    id: int
    title: str


class ProductCreateSchema(BaseModel):
    """Схема создания нового продукта."""

    title: str
    price: int
    in_stock: int
    sub_category_id: int
    description: str


class ProductRepresentSchema(BaseModel):
    """Схема представления товаров."""

    id: int
    title: str
    price: int
    in_stock: int
    category: ProductCategorySchema
    description: str
    salesman: UserSalesmanRepresentForProduct
