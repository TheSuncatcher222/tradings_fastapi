"""
Модуль с эндпоинтами приложения "product".
"""

from fastapi import APIRouter, Depends

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select
from sqlalchemy.sql.selectable import Select

from src.database import AsyncSession, get_async_session
from src.product.models import Product, ProductCategory
from src.product.schemas import ProductSchema, ProductCategorySchema

router_product: APIRouter = APIRouter(
    prefix='/products',
    tags=['Products'],
)


@router_product.get(
    path='/items',
    response_model=list[ProductSchema],
)
async def products_list(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список товаров."""
    query: Select = select(Product).options(joinedload(Product.category))
    queryset: ChunkedIteratorResult = await session.execute(query)

    products: list[Product] = [row[0] for row in queryset]

    return products


@router_product.get(
    path='/categories',
    response_model=list[ProductCategorySchema],
)
async def products_categories_list(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список категорий товаров."""
    query: Select = select(ProductCategory)
    queryset: ChunkedIteratorResult = await session.execute(query)

    categories: list[ProductCategory] = [row[0] for row in queryset]

    return categories
