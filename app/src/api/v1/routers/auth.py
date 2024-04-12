"""
Модуль с эндпоинтами приложения "auth".
"""

# TODO: заменить все JSONResponse на HTTPException.

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response

from src.api.v1.crud.auth import used_pass_reset_token_v1_crud
from src.api.v1.crud.user import user_v1_crud
from src.api.v1.schemas.auth import (
    AuthLogin, AuthPasswordChange, AuthPasswordReset,
    AuthPasswordResetConfirm, JwtTokenAccess,
)
from src.api.v1.schemas.user import UserRegister
from src.celery_app.auth.tasks import (
    send_password_has_changed_to_mail, send_password_restore_to_mail,
)
from src.celery_app.celery_app import PRIOR_LOW, PRIOR_IMPORTANT
from src.config.config import settings
from src.database.database import AsyncSession, get_async_session
from src.models.auth import UsedPassResetToken
from src.models.user import User
from src.utils.auth import get_current_user
from src.utils.email_confirm import send_email_confirm_code
from src.utils.itsdangerous import dangerous_token_generate, dangerous_token_verify
from src.utils.jwt import jwt_decode, jwt_generate_pair
from src.utils.password import hash_password

router_auth: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router_auth.post(
    path='/login/',
    response_model=JwtTokenAccess,
    status_code=status.HTTP_200_OK,
)
async def auth_login(
    user_data: AuthLogin,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    """Осуществляет авторизацию пользователя на сайте."""
    user_data: dict[str, any] = user_data.model_dump()
    user: User = await user_v1_crud.retrieve_by_email_and_password(
        obj_email=user_data.get('email'),
        obj_raw_password=user_data.get('password'),
        session=session,
    )

    if not user.is_active:
        raise HTTPException(
            detail='Аккаунт временно заблокирован',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access_token, _, refresh_token, expires = await jwt_generate_pair(
        user_id=user.id,
        is_admin=user.is_admin,
    )
    response.set_cookie(
        key=settings.COOKIE_KEY_JWT_REFRESH,
        value=refresh_token,
        expires=expires,
        httponly=True,
        domain=settings.DOMAIN_NAME,
        secure='true',
    )

    return {'access': access_token}


@router_auth.post(
    path='/logout/',
)
async def auth_logout(
    response: Response,
):
    """Осуществляет разлогирование пользователя на сайте."""
    response.delete_cookie(
        key=settings.COOKIE_KEY_JWT_REFRESH,
        httponly=True,
        domain=settings.DOMAIN_NAME,
        secure='true',
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_auth.post(
    path='/refresh/',
    response_model=JwtTokenAccess,
    status_code=status.HTTP_200_OK,
)
async def auth_refresh(
    refresh: Annotated[str, Cookie()] = '',
):
    """
    Осуществляет обновление токена доступа
    при предъявлении валидного токена обновления.
    """
    token_data: dict[str, any] = await jwt_decode(jwt_token=refresh, from_cookie=True)
    if token_data.get('type') != settings.JWT_TYPE_REFRESH:
        raise HTTPException(
            detail='Указанный токен недействителен',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token, _, _, _ = await jwt_generate_pair(
        user_id=token_data.get('sub'),
        is_admin=token_data.get('is_admin', False),
        is_to_refresh=True,
    )
    return access_token


@router_auth.post(
    path='/register/',
)
async def auth_register(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет регистрацию пользователя на сайте.

    Перед сохранением осуществляет хеширование пароля.
    """
    user_data: dict[str, any] = user_data.model_dump(exclude_unset=True)

    user_data['hashed_password'] = await hash_password(raw_password=user_data.pop('password'))
    if user_data.get('is_organization'):
        new_user: User = await user_v1_crud.create_organization(
            obj_values=user_data,
            session=session,
        )
    else:
        new_user: User = await user_v1_crud.create(
            obj_values=user_data,
            session=session,
        )

    await send_email_confirm_code(
        user_id=new_user.id,
        user_email=new_user.email,
        user_full_name=new_user.get_full_name,
    )

    return JSONResponse(
        content={
            'register': (
                'Для завершения процесса регистрации, пожалуйста, '
                'перейдите по ссылке, отправленной на указанную '
                'электронную почту'
            )
        },
        status_code=status.HTTP_201_CREATED,
    )


@router_auth.post(
    path='/password-change/',
)
async def auth_password_change(
    passwords: AuthPasswordChange,
    user: dict[str, any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Изменяет старый пароль на новый."""
    passwords: dict[str, str] = passwords.model_dump()

    hashed_password: str = await hash_password(raw_password=passwords.get('password'))
    if hashed_password != user.hashed_password:
        raise HTTPException(
            detail='Пароль недействителен',
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    new_hashed_password: str = await hash_password(raw_password=passwords.get('new_password'))
    await user_v1_crud.update_by_id(
        obj_id=user.id,
        obj_data={'hashed_password': new_hashed_password},
        session=session,
    )

    to_email: str = settings.SUPPORT_EMAIL_TO if settings.DEBUG_EMAIL else user.email
    send_password_has_changed_to_mail.apply_async(
        args=(user.get_full_name, to_email),
        priority=PRIOR_IMPORTANT,
    )

    return JSONResponse(
        content={'password_change': 'Пароль успешно изменен'},
        status_code=status.HTTP_200_OK,
    )


@router_auth.get(
    path='/email-confirm/{confirm_code}/',
)
async def email_confirm_verify(
    confirm_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Производит подтверждение электронной почты пользователя."""
    token_data: dict = await dangerous_token_verify(token=confirm_code)
    if token_data is None:
        raise HTTPException(
            detail='Ссылка подтверждения электронной почты более недействительна',
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    await user_v1_crud.update_email_by_id(
        obj_id=token_data['user_id'],
        new_email=token_data['user_email'],
        session=session,
    )
    return JSONResponse(
        content={'email_confirm': 'Электронная почта успешно подтверждена'},
        status_code=status.HTTP_200_OK,
    )


@router_auth.post(
    path='/email-confirm/',
)
async def email_confirm_send(
    user: User = Depends(get_current_user),
):
    """Отправляет ссылку подтверждения электронной почты."""
    if not user.email_is_confirmed:
        await send_email_confirm_code(
            user_id=user.id,
            user_email=user.email,
            user_full_name=user.get_full_name,
        )
        return JSONResponse(
            content={'email_confirm': 'Ссылка для подтверждения отправлена на вашу электронную почту'},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={'email_confirm': 'Электронная почта уже подтверждена'},
        status_code=status.HTTP_200_OK)


@router_auth.post(
    path='/password-reset/',
)
async def password_reset(
    email: AuthPasswordReset,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет первый этап восстановления пароля:
    отправляет ссылку для восстановления пароля.
    """
    email: dict[str, str] = email.model_dump()
    user: User | None = await user_v1_crud.retrieve_by_email(
        obj_email=email.get('email'),
        session=session,
    )

    if user is None:
        return Response(status_code=status.HTTP_200_OK)

    reset_token: str = await dangerous_token_generate({'id': user.id})

    if settings.DEBUG_EMAIL:
        to_email: str = settings.SUPPORT_EMAIL_TO
        url_pass_reset_confirm: str = (
            f'http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/{reset_token}'
        )
    else:
        to_email: str = user.email
        url_pass_reset_confirm: str = (
            f'https://{settings.DOMAIN_NAME}/api/auth/password-reset-confirm/{reset_token}'
        )
    send_password_restore_to_mail.apply_async(
        args=(url_pass_reset_confirm, to_email),
        priority=PRIOR_LOW,
    )

    return Response(status_code=status.HTTP_200_OK)


@router_auth.post(
    path='/password-reset-confirm/',
)
async def password_reset_confirm(
    passwords: AuthPasswordResetConfirm,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет второй этап восстановления пароля:
    устанавливает новый пароль пользователя.
    """
    # TODO: логировать неуспешные попытки. Сделать задержку.
    headers: dict[str, str] = {'Referrer-Policy': 'no-referrer'}

    passwords: dict[str, str] = passwords.model_dump()
    reset_token: str = passwords.get('reset_token')
    token_data: dict = await dangerous_token_verify(token=reset_token)

    user: None = None
    if token_data is not None:
        token: UsedPassResetToken | None = await used_pass_reset_token_v1_crud.retrieve_by_token(
            obj_token=reset_token,
            session=session,
        )
        # INFO. Токен восстановления не может использоваться повторно и
        #       записывается временно в базу данных.
        if token is None:
            user: User | None = await user_v1_crud.retrieve_by_id(obj_id=token_data.get('id'), session=session)
    if user is None:
        raise HTTPException(
            detail='Произошла ошибка. Пожалуйста, запросите новую ссылку восстановления пароля',
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    new_hashed_password: str = await hash_password(raw_password=passwords.get('new_password'))

    await user_v1_crud.update_by_id(
        obj_id=user.id,
        obj_data={'hashed_password': new_hashed_password},
        session=session,
    )
    await used_pass_reset_token_v1_crud.create(
        obj_values={'token': reset_token},
        session=session,
    )

    to_email: str = settings.SUPPORT_EMAIL_TO if settings.DEBUG_EMAIL else user.email
    send_password_has_changed_to_mail.apply_async(
        args=(user.get_full_name, to_email),
        priority=PRIOR_IMPORTANT,
    )

    return JSONResponse(
        content={'password_reset': 'Пароль учетной записи успешно изменен'},
        status_code=status.HTTP_200_OK,
        headers=headers,
    )
