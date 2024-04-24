"""
Модуль соединения с базой данных через SQLAlchemy.
"""

from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker,
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
    pass


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
    product_sub_category = 'table_product_sub_category'
    # user
    user = 'table_user'
    user_payment_data = 'table_user_payment_data'
    user_salesman = 'table_user_salesman'


table_names = TableNames()
