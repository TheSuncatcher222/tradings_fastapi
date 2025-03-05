"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции аутентификации и получения данных пользователей.
"""

from typing import (
    Annotated,
    Optional,
)

from fastapi import (
    HTTPException,
    Request,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from src.api.v1.crud.user import user_v1_crud
from src.celery_app.auth.tasks import send_email_confirm_code_to_email_task
from src.config.config import settings
from src.database.database import (
    AsyncSession,
    get_async_session,
)
from src.models.user import User
from src.utils.itsdangerous import dangerous_token_generate
from src.utils.jwt import jwt_decode
from src.utils.logger_json import (
    Logger,
    LoggerJsonAuth,
)

logger: Logger = LoggerJsonAuth

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_admin_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict[str, any]:
    """
    Возвращает информацию об администраторе из данных JWT токена доступа.
    Если пользователь не администратор, то вызывает HTTPException.
    """
    payload: dict[str, any] = await __get_jwt_payload(token=str(token))
    user_id: int = int(payload.get('sub'))
    is_admin: bool = payload.get('is_admin', False)

    if not is_admin:

        logger.warning(
            msg=(f'User id={user_id} try to access without admin rights'),
            extra={'token': token},
        )

        # TODO. Проверить, что возвращается в сеть то же самое, что и при обычном 404.
        raise HTTPException(
            detail=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    logger.info(msg=f'Admin-user id={user_id} successfully accessed.')

    return {
        'id': user_id,
        'is_admin': is_admin,
    }


async def get_user_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict[str, any]:
    """Возвращает информацию о пользователе из данных JWT токена доступа."""
    payload: dict[str, any] = await __get_jwt_payload(token=str(token))

    user_data: dict[str, any] = {'id': int(payload.get('sub'))}
    is_admin: bool = payload.get('is_admin', False)
    if is_admin:
        user_data['is_admin'] = is_admin

    logger.info(msg=f'User id={user_data.get("id")} successfully accessed. User is admin: {is_admin}.')

    return user_data


async def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Возвращает объект пользователя из данных JWT токена доступа."""
    return await __get_user(token=token, session=session)


async def get_active_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User | None:
    """
    Возвращает объект пользователя из данных JWT токена доступа.

    Если статус is_active False, то вызывает HTTPException с кодом 403.
    """
    user: User = await __get_user(token=token, session=session)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Ваша учетная запись заблокирована для выполнения этого действия',
        )
    return user


async def __get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Возвращает объект пользователя из данных JWT токена доступа."""
    payload: dict[str, any] = await __get_jwt_payload(token=str(token))
    user: User = await user_v1_crud.retrieve_by_id(
        obj_id=int(payload.get('sub')),
        session=session,
    )

    msg: str = f'User id={user.id} successfully accessed.'
    if user.is_admin:
        msg += ' User is admin.'
    logger.info(msg=msg)

    return user

async def __optional_oauth2_scheme(
    request: Request,
) -> Optional[str]:
    """
    Возвращает токен или None, если токен не предоставлен.
    """
    authorization: str = request.headers.get("Authorization")
    if authorization:
        scheme, token = get_authorization_scheme_param(authorization)
        if scheme.lower() == "bearer":
            return token
    return None


async def get_user_or_anonymous(
    token: Optional[str] = Depends(__optional_oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User | None:
    """
    Возвращает объект пользователя из данных JWT токена доступа.

    Если пользователь не найден, то возвращает None.
    """
    if token is None:
        return None
    return await get_user(token=token, session=session)


async def send_email_confirm_code(
    user: User,
) -> None:
    """Ставит задачу Celery для отправки ссылки подтверждения электронной почты."""
    confirm_code: str = await dangerous_token_generate(data={'user_id': user.id})

    logger.info(
        msg=f'Successfully generated email confirm code for user id={user.id}.',
        extra={'confirm_code': confirm_code},
    )

    if settings.DEBUG_EMAIL:
        url_email_confirm: str = f'http://127.0.0.1:8000/api/v1/auth/email-confirm/{confirm_code}'
    else:
        url_email_confirm: str = f'https://{settings.DOMAIN_NAME}/api/v1/auth/email-confirm/{confirm_code}'
    send_email_confirm_code_to_email_task.apply_async(
        kwargs={
            'user_full_name': user.get_full_name,
            'url_email_confirm': url_email_confirm,
            'to_email': user.email,
        },
    )

    logger.info(
        msg=(
            f'Successfully add Celery task "send_email_confirm_code_to_email_task" '
            f'for user id={user.id}.'
        ),
    )

    return


async def __get_jwt_payload(token: str) -> dict[str, any]:
    """
    Производит валидацию JWT токена и возвращает payload.

    Вызывает HTTPException в случае ошибки валидации.
    """
    payload: dict[str, any] = jwt_decode(jwt_token=token)

    if payload.get('type') != settings.JWT_TYPE_ACCESS:

        logger.info(
            msg=f'JWT token type is not {settings.JWT_TYPE_ACCESS}.',
            extra={
                'token': token,
                'type': payload.get('type'),
            },
        )

        raise HTTPException(
            detail='Указанный токен недействителен',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return payload
