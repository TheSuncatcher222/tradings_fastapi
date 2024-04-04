"""
Главный модуль FastAPI сервиса.

Осуществляет запуск проекта, подключение базы данных, регистрацию эндпоинтов.
"""

import os
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqladmin import Admin
import uvicorn

# INFO: добавляет корневую директорию проекта в sys.path для возможности
#       использования абсолютных путей импорта данных из модулей.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.base_routers import router_api
from src.config.config import settings
from src.database.database import async_engine
from src.models.sqlalchemy_admin import authentication_backend, admin_views
from src.utils.logger import get_logger, Logger


app: FastAPI = FastAPI(
    debug=settings.DEBUG,
    title='tradings Tech',
    description='tradings Tech hosting service',
    version='0.0.1',
    openapi_url='/api/docs/openapi.json',
    docs_url='/api/docs/swagger',
    redoc_url='/api/docs/redoc',
)

logger: Logger = get_logger(name=__name__)

allowed_origins = [
    'http://localhost:80',
    'http://localhost:8000',
    'http://localhost:8080',
    f'https://{settings.DOMAIN_IP}',
    f'https://{settings.DOMAIN_NAME}',
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
    prefix='/api'
)

admin = Admin(
    app=app,
    engine=async_engine,
    authentication_backend=authentication_backend,
    base_url=f'/api/{settings.ADMIN_URL}/',
)

for admin_view in admin_views:
    admin.add_view(admin_view)

if __name__ == '__main__':
    """Автозапуск ASGI и сервиса."""
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        workers=4,
    )
