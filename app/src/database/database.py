"""
Модуль соединения с базой данных через SQLAlchemy.
"""

from typing import AsyncGenerator

from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.config import settings

DATABASE_ASYNC_URL: str = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}'
DATABASE_SYNC_URL: str = f'postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}'


async_engine: AsyncEngine = create_async_engine(
    url=DATABASE_ASYNC_URL,
    echo=settings.DEBUG_DB,
)

async_session_maker: async_sessionmaker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


sync_engine = create_engine(
    url=DATABASE_SYNC_URL,
    echo=settings.DEBUG_DB,
)

sync_session_maker: sessionmaker = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    """Инициализирует фабрику создания декларативных классов моделей."""


class TableNames():
    """Содержит в себе названия таблиц проекта."""
    # address
    address = 'table_address'
    country = 'table_country'
    # auth
    used_pass_reset_token = 'table_used_pass_reset_token'
    # feedback
    feedback = 'table_feedback'
    # product
    product = 'table_product'
    product_category = 'table_product_category'
    # user
    user = 'table_user'
    user_bank_card = 'table_user_bank_card'
    user_salesman = 'table_user_salesman'


class RedisKeys:
    """
    Класс представления Redis ключей.

    INFO. Лучше не превышать длину ключа в 255 символа.
    """

    __PREFIX: str = 'tradings_app_cache_'

    # Auth
    __PREFIX_AUTH: str = __PREFIX + 'auth_'
    AUTH_USER_BAD_LOGIN_COUNT: str = __PREFIX_AUTH + 'user_bad_login_count_' + '{user_email}'
    USED_PASSWORD_RESET_TOKEN: str = __PREFIX_AUTH + 'used_password_reset_token_' + '{reset_token}'


    @classmethod
    def all_keys(cls) -> tuple[str]:
        # TODO. Нужно взять из Redis все текущие ключи по факту.
        return (
            # cls.AUTH_USER_BAD_LOGIN_COUNT,
            # cls.USED_PASSWORD_RESET_TOKEN,
            cls.SERVICE_PRICE_LIST_DICT,
        )


redis_engine: Redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_CACHE,
    decode_responses=True,
)
