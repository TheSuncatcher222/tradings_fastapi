"""
Модуль с эндпоинтами приложения "product".
"""

from fastapi import (
    APIRouter,
    Depends,
)

from src.api.v1.crud.product import product_v1_crud
from src.api.v1.schemas.product import (
    ProductCreateSchema,
    ProductRepresentSchema,
)
from src.database.database import (
    AsyncSession,
    get_async_session,
)
from src.models.user import User
from src.utils.auth import get_user

router_product: APIRouter = APIRouter(
    prefix='/products',
    tags=['Product'],
)


@router_product.post(
    path='/',
    response_model=ProductRepresentSchema,
)
async def product_create(
    product_data: ProductCreateSchema,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Регистрирует новый продукт."""
    return await product_v1_crud.create(
        obj_values=product_data.model_dump(),
        user=user,
        session=session,
    )


@router_product.get(
    path='/',
    response_model=list[ProductRepresentSchema],
)
async def product_retrieve_all(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает все продукты.

    Сортировка производится по id в порядке убывания: от новинок к старым.
    """
    return await product_v1_crud.retrieve_all(
        offset=offset,
        limit=limit,
        session=session,
    )
