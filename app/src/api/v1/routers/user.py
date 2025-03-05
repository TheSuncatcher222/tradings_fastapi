"""
Модуль с эндпоинтами приложения "user".
"""

from fastapi import APIRouter, Depends, status

from src.api.v1.crud.user import user_v1_crud
from src.api.v1.schemas.user import (
    UserRepresent,
    UserUpdate,
)
from src.database.database import AsyncSession, get_async_session
from src.utils.auth import get_user

router_users: APIRouter = APIRouter(
    prefix='/users',
    tags=['User'],
)


@router_users.get(
    path='/me/',
    response_model=UserRepresent,
    status_code=status.HTTP_200_OK,
)
async def user_me(
    current_user: dict[str, any] = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает данные активного пользователя."""
    return await user_v1_crud.retrieve_by_id(
        obj_id=current_user.id,
        session=session,
    )


@router_users.patch(
    path='/me/',
    response_model=UserRepresent,
    status_code=status.HTTP_200_OK,
)
async def user_me_update(
    user_update: UserUpdate,
    current_user: dict[str, any] = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Изменяет данные активного пользователя."""
    return await user_v1_crud.update_by_id(
        obj_id=current_user.id,
        obj_data=user_update.model_dump(exclude_unset=True),
        session=session,
    )
