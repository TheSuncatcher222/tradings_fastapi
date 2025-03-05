"""
Модуль с эндпоинтами приложения "auth".
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Cookie,
    Depends,
)
from fastapi.responses import (
    JSONResponse,
    Response,
)

from src.api.v1.crud.user import user_v1_crud
from src.api.v1.schemas.auth import (
    AuthLoginSchema,
    AuthPasswordChangeSchema,
    AuthPasswordResetSchema,
    AuthPasswordResetConfirmSchema,
    JwtTokenAccessRepresentSchema,
)
from src.api.v1.schemas.user import UserRegisterSchema
from src.celery_app.auth.tasks import (
    send_password_has_changed_to_mail_task,
    send_password_restore_to_mail_task,
)
from src.config.config import (
    TimeIntervals,
    settings,
)
from src.database.database import (
    AsyncSession,
    RedisKeys,
    get_async_session,
)
from src.models.user import User
from src.utils.auth import (
    get_user,
    send_email_confirm_code,
)
from src.utils.custom_exception import (
    CustomValidationTypes,
    form_pydantic_like_validation_error,
)
from src.utils.itsdangerous import (
    dangerous_token_generate,
    dangerous_token_verify,
)
from src.utils.jwt import (
    jwt_decode,
    jwt_generate_pair,
)
from src.utils.logger_json import (
    Logger,
    LoggerJsonAuth,
)
from src.utils.password import hash_password
from src.utils.redis_data import (
    redis_delete,
    redis_get,
    redis_get_ttl,
    redis_set,
)

logger: Logger = LoggerJsonAuth

router_auth: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router_auth.post(
    path='/email-confirm/',
)
async def post_email_confirm_send(
    user: User = Depends(get_user),
):
    """Отправляет ссылку подтверждения электронной почты."""
    if user.email_is_confirmed:

        logger.info(msg=f'User id={user.id} try to confirm email that already confirmed.')

        return JSONResponse(
            content={'email_confirm': 'Электронная почта уже подтверждена'},
            status_code=status.HTTP_200_OK,
        )

    await send_email_confirm_code(
        user_id=user.id,
        user_email=user.email,
        user_full_name=user.get_full_name,
    )

    logger.info(msg=f'User id={user.id} successfully requested email confirm code.')

    return JSONResponse(
        content={'email_confirm': 'Ссылка для подтверждения отправлена на вашу электронную почту'},
        status_code=status.HTTP_200_OK,
    )


@router_auth.get(
    path='/email-confirm/{confirm_code}/',
)
async def get_email_confirm_verify(
    confirm_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Производит подтверждение электронной почты пользователя."""
    token_data: dict = await dangerous_token_verify(token=confirm_code)

    if token_data is None:
        detail: dict[str, any] = form_pydantic_like_validation_error(
            type_=CustomValidationTypes.VALUE_ERROR,
            loc=['url'],
            msg='Ссылка подтверждения электронной почты недействительна',
            input_={'url': f'{settings.DOMAIN_NAME}/pi/v1/auth/email-confirm/{confirm_code}'},
        )

        logger.info(
            msg=f'Someone try to confirm email with invalid confirm_code.',
            extra={"confirm_code": confirm_code},
        )

        raise HTTPException(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    await user_v1_crud.update_by_id(
        obj_id=token_data['user_id'],
        obj_data={'email_is_confirmed': True},
        perform_obj_unique_check=False,
        session=session,
    )

    logger.info(msg=f'User id={token_data["user_id"]} successfully confirmed email.')

    return JSONResponse(
        content={'email_confirm': 'Электронная почта успешно подтверждена'},
        status_code=status.HTTP_200_OK,
    )


@router_auth.post(
    path='/login/',
    response_model=JwtTokenAccessRepresentSchema,
    status_code=status.HTTP_200_OK,
)
async def post_login(
    user_data: AuthLoginSchema,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    """Осуществляет авторизацию пользователя на сайте."""
    user_data: dict[str, any] = user_data.model_dump()
    user: User = await user_v1_crud.retrieve_by_email(
        obj_email=user_data.get('email'),
        session=session,
    )

    if user.is_deleted:

        logger.info(msg=f'User id={user.id} try to login to the is_deleted account.')

        raise HTTPException(
            detail='Аккаунт заблокирован',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    bad_login_count: int | None = redis_get(key=RedisKeys.AUTH_USER_BAD_LOGIN_COUNT.format(user_email=user.email))
    bad_login_count: int = bad_login_count if bad_login_count is not None else 0

    if bad_login_count > settings.BAD_LOGIN_MAX_ATTEMPTS:

        logger.warning(
            msg=(
                f'User id={user.id} exceeds the number of {settings.BAD_LOGIN_MAX_ATTEMPTS}'
                f'login attempt in a row during last {settings.BAD_LOGIN_EXPIRATION_SEC}.'
            ),
        )

        ttl: int = redis_get_ttl(key=RedisKeys.AUTH_USER_BAD_LOGIN_COUNT.format(user_email=user.email))
        raise HTTPException(
            detail=f'Превышено количество попыток входа. Пожалуйста, повторите попытку через {ttl} с.',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    obj_raw_password=user_data.get('password')

    if user.hashed_password != hash_password(raw_password=obj_raw_password):
        bad_login_count += 1
        if bad_login_count > settings.BAD_LOGIN_MAX_ATTEMPTS:
            ex_sec: int = settings.BAD_LOGIN_BAN_SEC
        else:
            ex_sec: int = settings.BAD_LOGIN_EXPIRATION_SEC
        redis_set(
            key=RedisKeys.AUTH_USER_BAD_LOGIN_COUNT.format(user_email=user.email),
            value=bad_login_count,
            ex_sec=ex_sec,
        )

        logger.info(msg=f'User id={user.id} try to login to the account with bad password.')

        raise HTTPException(
            detail=user_v1_crud._raise_httpexception_404_not_found(),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    redis_delete(key=RedisKeys.AUTH_USER_BAD_LOGIN_COUNT.format(user_email=user.email))

    access_token, _, refresh_token, expires = jwt_generate_pair(
        user_id=user.id,
        is_admin=user.is_admin,
    )

    if settings.DEBUG:
        cookie_domain: str = 'localhost'
    else:
        cookie_domain = settings.DOMAIN_NAME

    response.set_cookie(
        key=settings.COOKIE_KEY_JWT_REFRESH,
        value=refresh_token,
        expires=expires,
        httponly=True,
        domain=cookie_domain,
        secure='true',
    )

    logger.info(msg=f'User id={user.id} successfully logged in.')

    return {'access': access_token}


@router_auth.post(
    path='/logout/',
)
async def post_logout(
    response: Response,
):
    """Осуществляет разлогинивание пользователя на сайте."""
    if settings.DEBUG:
        cookie_domain: str = 'localhost'
    else:
        cookie_domain = settings.DOMAIN_NAME

    response.delete_cookie(
        key=settings.COOKIE_KEY_JWT_REFRESH,
        httponly=True,
        domain=cookie_domain,
        secure='true',
    )
    response.status_code = status.HTTP_204_NO_CONTENT

    return response


@router_auth.post(
    path='/password-change/',
)
async def post_password_change(
    passwords: AuthPasswordChangeSchema,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Изменяет старый пароль на новый."""
    passwords: dict[str, str] = passwords.model_dump()

    hashed_password: str = hash_password(raw_password=passwords.get('password'))
    if hashed_password != user.hashed_password:
        detail: dict[str, any] = form_pydantic_like_validation_error(
            type_=CustomValidationTypes.VALUE_ERROR,
            loc=[
                'body',
                0,
                'password',
            ],
            msg='Указан неверный актуальный пароль',
            input_=passwords.get('password'),
        )

        logger.warning(msg=f'User id={user.id} try to change password with wrong password.')

        raise HTTPException(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    new_hashed_password: str = hash_password(raw_password=passwords.get('new_password'))
    await user_v1_crud.update_by_id(
        obj_id=user.id,
        obj_data={'hashed_password': new_hashed_password},
        session=session,
    )

    send_password_has_changed_to_mail_task.apply_async(
        args=(user.get_full_name, user.email),
    )

    logger.info(msg=f'User id={user.id} successfully changed password.')

    return JSONResponse(
        content={'password_change': 'Пароль успешно изменен'},
        status_code=status.HTTP_200_OK,
    )


@router_auth.post(
    path='/password-reset/',
)
async def post_password_reset(
    email: AuthPasswordResetSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет первый этап восстановления пароля:
    отправляет ссылку для восстановления пароля.
    """
    email: dict[str, str] = email.model_dump()
    email: str = email.get('email')
    user: User | None = await user_v1_crud.retrieve_by_email(
        obj_email=email,
        session=session,
        raise_404=False,
    )

    if user is None:

        logger.warning(msg=f'User with not existing email={email} try to reset password')

        return Response(status_code=status.HTTP_200_OK)

    reset_token: str = await dangerous_token_generate({'id': user.id})

    if settings.DEBUG_EMAIL:
        url_pass_reset_confirm: str = (
            f'http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/{reset_token}/'
        )
    else:
        url_pass_reset_confirm: str = (
            f'https://{settings.DOMAIN_NAME}/recovery-password/{reset_token}/'
        )
    send_password_restore_to_mail_task.apply_async(
        args=(url_pass_reset_confirm, user.email),
    )

    logger.info(msg=f'User with email={email} successfully requested password reset.')

    return Response(status_code=status.HTTP_200_OK)


@router_auth.post(
    path='/password-reset-confirm/',
)
async def post_password_reset_confirm(
    passwords: AuthPasswordResetConfirmSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет второй этап восстановления пароля:
    устанавливает новый пароль пользователя.
    """
    # TODO: логировать неуспешные попытки. Сделать задержку.
    headers: dict[str, str] = {'Referrer-Policy': 'no-referrer'}

    passwords: dict[str, str] = passwords.model_dump()
    reset_token: str = passwords.get('reset_token', '')
    token_data: dict = await dangerous_token_verify(
        token=reset_token,
        expiration=TimeIntervals.SECONDS_IN_1_DAY,
    )

    user: None = None
    redis_key: str = RedisKeys.USED_PASSWORD_RESET_TOKEN.format(reset_token=reset_token)
    if token_data:
        token: str | None = redis_get(key=redis_key)
        # INFO. Токен восстановления не может использоваться повторно.
        if not token:
            user: User | None = await user_v1_crud.retrieve_by_id(
                obj_id=token_data.get('id'),
                session=session,
                raise_404=False,
            )

    if user is None:
        if settings.DEBUG_EMAIL:
            url_pass_reset_confirm: str = (
                f'http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/{reset_token}/'
            )
        else:
            url_pass_reset_confirm: str = (
                f'https://{settings.DOMAIN_NAME}/recovery-password/{reset_token}/'
            )
        detail: dict[str, any] = form_pydantic_like_validation_error(
            type_=CustomValidationTypes.VALUE_ERROR,
            loc=[
                'url',
            ],
            msg='Ссылка восстановления пароля недействительна',
            input_=url_pass_reset_confirm,
        )

        logger.warning(
            msg=f'User try to reset password with not existing token.',
            extra={'reset_token': reset_token},
        )

        raise HTTPException(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    new_hashed_password: str = hash_password(raw_password=passwords.get('new_password'))

    redis_set(
        key=redis_key,
        value=1,
        ex_sec=TimeIntervals.SECONDS_IN_1_DAY,
    )
    await user_v1_crud.update_by_id(
        obj_id=user.id,
        obj_data={'hashed_password': new_hashed_password},
        session=session,
    )

    send_password_has_changed_to_mail_task.apply_async(
        args=(user.get_full_name, user.email),
    )

    logger.info(msg=f'User id={user.id} successfully reset password.')

    return JSONResponse(
        content={'password_reset': 'Пароль учетной записи успешно изменен'},
        status_code=status.HTTP_200_OK,
        headers=headers,
    )


@router_auth.post(
    path='/refresh/',
    response_model=JwtTokenAccessRepresentSchema,
    status_code=status.HTTP_200_OK,
)
async def post_refresh(
    refresh: Annotated[str, Cookie()] = '',
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет обновление токена доступа
    при предъявлении валидного токена обновления.
    """
    token_data: dict[str, any] = jwt_decode(jwt_token=refresh)
    if token_data.get('type') != settings.JWT_TYPE_REFRESH:
        raise HTTPException(
            detail='Указанный токен недействителен',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user: User = await user_v1_crud.retrieve_by_id(
        obj_id=token_data.get('sub'),
        session=session,
    )
    if user.is_deleted:

        logger.info(msg=f'User id={user.id} try to refresh password with is_deleted account.')

        raise HTTPException(
            detail='Аккаунт заблокирован',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access, *_ = jwt_generate_pair(
        user_id=token_data.get('sub'),
        is_admin=token_data.get('is_admin', False),
        is_to_refresh=True,
    )
    return {"access": access}


@router_auth.post(
    path='/register/',
)
async def post_register(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет регистрацию пользователя на сайте.

    Перед сохранением осуществляет хеширование пароля.
    """
    user_data: dict[str, any] = user_data.model_dump()

    user_data['hashed_password'] = hash_password(raw_password=user_data.pop('password'))
    new_user: User = await user_v1_crud.create(
        obj_data=user_data,
        session=session,
    )

    await send_email_confirm_code(user=new_user)

    logger.info(msg=f'User id={new_user.id} successfully registered and requested email confirm code.')

    return JSONResponse(
        content={
            'register': (
                'Для завершения процесса регистрации, пожалуйста, '
                'перейдите по ссылке, отправленной на указанную электронную почту'
            ),
        },
        status_code=status.HTTP_201_CREATED,
    )
