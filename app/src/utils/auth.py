"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции аутентификации и получения данных пользователей.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.api.v1.crud.user import user_v1_crud
from src.config.config import settings
from src.database.database import AsyncSession, get_async_session
from src.models.user import User
from src.utils.jwt import jwt_decode

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_admin_payload(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict[str, any]:
    """
    Возвращает информацию об администраторе из данных JWT токена доступа.
    Если пользователь не администратор, то вызывает HTTPException.
    """
    payload: dict[str, any] = await _get_jwt_payload(token=str(token))

    if not payload.get('is_admin'):
        raise HTTPException(
            detail='Доступ запрещен',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return {
        'id': int(payload.get('sub')),
        'is_admin': payload.get('is_admin'),
    }


# TODO. Исключить! Так как не добавляет запись в базу о посещении сайта.
async def get_current_user_payload(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict[str, any]:
    """Возвращает информацию о пользователе из данных JWT токена доступа."""
    payload: dict[str, any] = await _get_jwt_payload(token=str(token))

    user_data: dict[str, any] = {'id': int(payload.get('sub'))}
    is_admin: bool = payload.get('is_admin', False)
    if is_admin:
        user_data['is_admin'] = is_admin
    is_salesman: bool = payload.get('is_admin', False)
    if is_salesman:
        user_data['is_salesman'] = payload.get('is_salesman', False)

    return user_data


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Возвращает объект пользователя из данных JWT токена доступа."""
    payload: dict[str, any] = await _get_jwt_payload(token=str(token))
    # INFO. Использование retrieve_by_id не имеет смысла,
    #       так как update_by_id также возвращает объект User,
    #       а надо обновить его поле last_login.
    user: User = await user_v1_crud.retrieve_by_id(
        obj_id=int(payload.get('sub')),
        session=session,
    )
    return user


async def _get_jwt_payload(token: str) -> dict[str, any]:
    """
    Производит валидацию JWT токена и возвращает payload.

    Вызывает HTTPException в случае ошибки валидации.
    """
    payload: dict[str, any] = await jwt_decode(jwt_token=token)
    if payload.get('type') != settings.JWT_TYPE_ACCESS:
        raise HTTPException(
            detail='Указанный токен недействителен',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return payload
