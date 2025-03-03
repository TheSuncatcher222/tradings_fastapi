"""Модуль с классом CRUD запросов в базу данных для модели Product."""

from src.database.database import AsyncSession, Base
from src.database.base_async_crud import BaseAsyncCrud
from src.models.product import Product, ProductSubCategory
from src.models.user import User


class ProductSubCategoryV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице ProductSubCategory."""

    async def retrieve_by_id(self, *, obj_id: int, session: AsyncSession) -> Base:
        return await super().retrieve_by_id(obj_id=obj_id, session=session)


product_sub_category_v1_crud = ProductSubCategoryV1Crud(
    model=ProductSubCategory,
    object_not_found_err='Такая под-категория товаров не найдена',
    unique_columns=('title', 'product_category_id'),
    unique_columns_err='Такая под-категория в категории уже существует',
)


# TODO. Запретить прочие методы.
class ProductV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице Product."""

    async def create(
        self,
        *,
        obj_values: dict[str, any],
        user: User,
        session: AsyncSession,
    ) -> Base:
        # await product_sub_category_v1_crud.retrieve_by_id(
        #     obj_id=obj_values['sub_category_id'],
        #     session=session,
        # )
        obj_values['salesman_id'] = user.id
        return await super().create(obj_values=obj_values, session=session)

    # async def create(
    #     self,
    #     *,
    #     obj_values: dict[str, any],
    #     user: User,
    #     session: AsyncSession,
    # ) -> Product:
    #     """Создает один объект в базе данных."""
    #     obj_values['salesman_id'] = user.id
    #     return await super().create(obj_values=obj_values, session=session)


product_v1_crud = ProductV1Crud(
    model=Product,
    # INFO. У разных продавцов могут быть
    #       одинаковые товары и/или их названия.
    #       Но у одного продавца не должно быть
    #       одинаковых товаров и товаров с одинаковыми названиями.
    unique_columns=('title', 'salesman_id'),
)
