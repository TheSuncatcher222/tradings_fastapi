"""
Модуль с эндпоинтами приложения "auth".
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql import insert, select
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.selectable import Select

from src.auth.schemas import (
    AuthLogin, AuthRegister, JwtTokenAccess, JwtTokenRefresh,
)
from src.auth.utils import hash_password, jwt_decode, jwt_generate_pair
from src.config import (
    DOMAIN_NAME,
    JSON_ERR_EMAIL_IS_ALREADY_REGISTERED, JSON_ERR_EMAIL_OR_PASS_INVALID,
    JSON_ERR_CREDENTIALS_TYPE, JWT_TYPE_REFRESH,
)
from src.database import AsyncSession, get_async_session
from src.users.models import User
from src.users.schemas import UserRepresent

router_auth: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router_auth.post(
    path='/login',
    response_model=JwtTokenAccess,
)
async def auth_login(
    user_data: AuthLogin,
    session: AsyncSession = Depends(get_async_session),
):
    """Осуществляет авторизацию пользователя на сайте."""
    user_data: dict[str, any] = user_data.model_dump()

    email: str = user_data.get('email')
    query: Select = select(User).where(User.email == email)
    queryset: ChunkedIteratorResult = await session.execute(query)
    user: User | None = queryset.scalars().first()

    raw_password: str = user_data.get('password')
    # TODO: рассмотреть логику проверки is.active
    if (
        user is None or
        hash_password(raw_password=raw_password) != user.hashed_password
    ):
        return JSONResponse(
            content=JSON_ERR_EMAIL_OR_PASS_INVALID,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token_access, _, token_refresh, expires = jwt_generate_pair(
        user_id=user.id,
        is_admin=user.is_admin,
    )

    response = JSONResponse(
        content=JwtTokenAccess(access=token_access).model_dump(),
        status_code=status.HTTP_200_OK,
    )

    response.set_cookie(
        key='refresh',
        value=token_refresh,
        expires=expires,
        httponly=True,
        domain=DOMAIN_NAME,
        secure='true',
    )

    return response


@router_auth.post(
    path='/refresh',
    response_model=JwtTokenAccess
)
async def auth_refresh(
    refresh_token: JwtTokenRefresh,
):
    """
    Осуществляет обновление токена доступа
    при предъявлении валидного токена обновления.
    """
    token_data: dict[str, any] = refresh_token.model_dump()
    token_data: dict[str, any] = jwt_decode(jwt_token=token_data['refresh'])
    if token_data.get('err_response', None) is not None:
        return token_data.get('err_response')
    if token_data.get('type') != JWT_TYPE_REFRESH:
        return JSONResponse(
            content=JSON_ERR_CREDENTIALS_TYPE,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    access_token, _ = jwt_generate_pair(
        user_id=token_data.get('sub'),
        is_admin=token_data.get('is_admin', False),
        refresh=True,
    )
    return {'access': access_token}


@router_auth.post(
    path='/register',
    response_model=UserRepresent,
)
async def auth_register(
    user_data: AuthRegister,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет регистрацию пользователя на сайте.

    Осуществляет хеширование пароля.
    """
    user_data = user_data.model_dump()

    email: str = user_data.get('email')
    query: Select = select(User).where(User.email == email)
    queryset: ChunkedIteratorResult = await session.execute(query)
    user: User | None = queryset.scalars().first()
    if user is not None:
        return JSONResponse(
            content=JSON_ERR_EMAIL_IS_ALREADY_REGISTERED,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    raw_password: str = user_data.pop('password')
    user_data['hashed_password']: str = hash_password(raw_password=raw_password)

    stmt: Insert = insert(User).values(**user_data).returning(User)
    result = await session.execute(stmt)
    await session.commit()

    new_user: User = result.fetchone()[0]

    return UserRepresent(
        id=new_user.id,
        name_first=new_user.name_first,
        name_last=new_user.name_last,
        email=new_user.email,
        phone=new_user.phone,
        telegram_username=new_user.telegram_username,
        account_balance=new_user.account_balance,
        reg_date=new_user.reg_date,
    )
