"""
Модуль с эндпоинтами приложения "user".
"""

from fastapi import APIRouter, Depends

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql import select
from sqlalchemy.sql.selectable import Select

from src.auth.utils import get_current_user_id
from src.database import AsyncSession, get_async_session
from src.user.models import User
from src.user.schemas import UserRepresent

router_users: APIRouter = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router_users.get(
    path='/me',
    response_model=UserRepresent,
)
async def user_me(
    user_data: dict[str, any] = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает данные активного пользователя."""
    if 'err_response' in user_data:
        return user_data['err_response']

    query: Select = select(User).where(User.id == user_data.get('id'))
    queryset: ChunkedIteratorResult = await session.execute(query)
    user: User | None = queryset.scalars().first()

    return user
