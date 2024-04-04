"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции аутентификации и получения данных пользователей.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.celery_app.celery_app import PRIOR_MEDIUM
from src.celery_app.auth.tasks import send_email_confirm_code_to_email
from src.config.config import settings
from src.utils.itsdangerous import dangerous_token_generate
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


async def generate_email_confirm_code(user_id: int) -> str:
    """Генерирует код подтверждения почты пользователя."""
    return await dangerous_token_generate(data={'user_id': user_id})


async def send_email_confirm_code(
    user_id: int,
    user_email: str,
    user_full_name: str,
) -> None:
    """Ставит задачу Celery для отправки ссылки подтверждения электронной почты."""
    confirm_code: str = await generate_email_confirm_code(user_id=user_id)

    if settings.DEBUG_EMAIL:
        user_email: str = settings.SUPPORT_EMAIL_TO
        url_email_confirm: str = (
            f'http://127.0.0.1:8000/api/v1/auth/email-confirm/{confirm_code}'
        )
    else:
        url_email_confirm: str = (
            f'https://{settings.DOMAIN_NAME}/api/v1/auth/email-confirm/{confirm_code}'
        )

    send_email_confirm_code_to_email.apply_async(
        args=(user_full_name, url_email_confirm, user_email),
        priority=PRIOR_MEDIUM,
    )
    return


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
