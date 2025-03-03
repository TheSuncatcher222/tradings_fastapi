"""
Главный модуль тестирования FastAPI сервиса.

Осуществляет подготовку Pytest.
"""

import os
import sys
from typing import (
    AsyncGenerator,
    Generator,
)

from asyncpg import connect
from asyncpg.connection import Connection
from httpx import (
    ASGITransport,
    AsyncClient,
)
import pytest_asyncio as pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

# INFO: добавляет корневую директорию проекта в sys.path для возможности
#       использования абсолютных путей импорта данных из модулей.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.src.config.config import settings
from app.src.database.database import (
    Base,
    get_async_session,
)
from app.src.main import app

POSTGRES_DB: str = f'test_{settings.POSTGRES_DB}'
TEST_DATABASE_ASYNC_URL: str = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{POSTGRES_DB}'
TEST_DATABASE_SYNC_URL: str = f'postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{POSTGRES_DB}'

SQL_DISCONNECT_FROM_TEST_DB: str = (
    f"""
    DO $$
    BEGIN
        PERFORM pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{POSTGRES_DB}'
        AND pid <> pg_backend_pid();
    END $$;
    """
)

test_async_engine: AsyncEngine = create_async_engine(
    url=TEST_DATABASE_ASYNC_URL,
    echo=False,
    # INFO. Необходимо, чтобы все асинхронные операции были в одном event loop.
    poolclass=NullPool,
)
test_async_session_maker: async_sessionmaker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_async_engine,
    expire_on_commit=False,
    join_transaction_mode="create_savepoint",
)


@pytest.fixture()
async def test_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для работы с тестовым асинхронным сессиями."""
    async with test_async_session_maker() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture(scope="function", autouse=True)
def override_get_async_session(test_async_session: AsyncSession) -> Generator[None, None, None]:
    """Переопределяет Dependency с ключом "get_async_session" для тестов."""
    app.dependency_overrides[get_async_session] = lambda: test_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    """Создает тестовую БД для проведения тестов и удаляет ее после их завершения."""
    # INFO. Шаг 1. Создание тестовой БД с нуля.
    connection: Connection = await connect(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database="postgres",
    )
    try:
        await connection.execute(SQL_DISCONNECT_FROM_TEST_DB)
        await connection.execute(f'DROP DATABASE IF EXISTS "{POSTGRES_DB}"')
        await connection.execute(f'CREATE DATABASE "{POSTGRES_DB}"')
        async with test_async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    finally:
        # INFO. Шаг 2. Выполнение тестов.
        yield

        # INFO. Шаг 3. Удаление тестовой БД.
        await connection.execute(SQL_DISCONNECT_FROM_TEST_DB)
        await connection.execute(f'DROP DATABASE IF EXISTS "{POSTGRES_DB}"')
        await connection.close()


@pytest.fixture(scope="function", autouse=True)
async def truncate_test_db(test_async_session: AsyncSession) -> AsyncGenerator[None, None]:
    """Очистка тестовой БД перед каждым тестовым запуском."""
    await test_async_session.execute(text("TRUNCATE TABLE {} RESTART IDENTITY CASCADE".format(", ".join(Base.metadata.tables.keys()))))
    await test_async_session.commit()


@pytest.fixture(scope="session")
async def test_api_client() -> AsyncGenerator[AsyncClient, None]:
    """Создает тестовый API клиент."""
    async with AsyncClient(
        base_url='http://localhost:8001/api/v1/',
        transport=ASGITransport(app=app),
    ) as test_client:
        yield test_client
