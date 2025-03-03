"""
Главный модуль FastAPI сервиса.

Осуществляет запуск проекта, подключение базы данных, регистрацию эндпоинтов.
"""

from contextlib import asynccontextmanager
import os
import sys

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend as RedisCacheBackend
from redis import (
    asyncio as aioredis,
    Redis as RedisClass,
)
from starlette.middleware.cors import CORSMiddleware
from sqladmin import Admin
import uvicorn

# INFO: добавляет корневую директорию проекта в sys.path для возможности
#       использования абсолютных путей импорта данных из модулей.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.base_routers import router_api
from src.config.config import settings
from src.database.database import async_engine
from src.models.sqlalchemy_admin import (
    authentication_backend,
    admin_views,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Жизненный цикл FastAPI сервиса:
        - до yield: процессы подготовки приложения
        - yield: запуск приложения
        - после yield: процессы после завершения работы приложения
    """
    try:
        redis_fastapi: RedisClass = aioredis.from_url(
            url=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_CACHE_FASTAPI}',
            encoding="utf8",
            decode_responses=True,
        )
        FastAPICache.init(
            backend=RedisCacheBackend(redis=redis_fastapi),
            prefix='redis-fastapi-cache',
        )

        yield

    except Exception:
        pass

    await redis_fastapi.close()
    return


app: FastAPI = FastAPI(
    debug=settings.DEBUG,
    title='tradings',
    description='tradings hosting service',
    version='0.0.1',
    openapi_url='/api/docs/openapi.json' if settings.DEBUG else None,
    docs_url='/api/docs/swagger' if settings.DEBUG else None,
    redoc_url='/api/docs/redoc' if settings.DEBUG else None,
)

allowed_origins = [
    f'https://{settings.DOMAIN_NAME}',
]
if settings.DEBUG_CORS:
    allowed_origins += [
        'http://localhost:4200',
        'http://localhost:8080',
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=router_api,
    prefix='/api',
)

admin = Admin(
    app=app,
    engine=async_engine,
    authentication_backend=authentication_backend,
    base_url=f'/{settings.ADMIN_URL}/',
)
for admin_view in admin_views:
    admin.add_view(admin_view)

if __name__ == '__main__':
    """Автозапуск ASGI и сервиса."""
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        # INFO. С reload=True доступен только один worker.
        reload=True if settings.DEBUG else False,
        # TODO. Разобраться с временем жизни воркеров.
        workers=settings.WORKERS_AMOUNT,
        # INFO. Нужно, чтобы подгружались стили в SQLAdmin
        #       https://aminalaee.dev/sqladmin/cookbook/deployment_with_https/
        forwarded_allow_ips='*',
    )
