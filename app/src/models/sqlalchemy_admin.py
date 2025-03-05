"""
Модуль с агрегацией ORM моделей для SQLAlchemy Admin for FastAPI.
"""

from fastapi import HTTPException
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.config.config import settings
from src.database.database import Base
from src.models import (
    #   - feedback
    FeedbackAdmin,
    #   - product
    ProductAdmin,
    ProductCategoryAdmin,
    #   - user
    UserAdmin,
    UserSalesmanAdmin,
)
from src.utils.auth import get_admin_payload
from src.utils.jwt import jwt_generate_pair

admin_views: list[Base] = [
    #   - feedback
    FeedbackAdmin,
    #   - product
    ProductAdmin,
    ProductCategoryAdmin,
    #   - user
    UserAdmin,
    UserSalesmanAdmin,
]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        username, password = form.get('username'), form.get('password')
        if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
            return False

        access_token, _, _, _ = await jwt_generate_pair(
            user_id=1,
            is_admin=True,
        )

        request.session.update({'token': access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get('token')

        if not token:
            return await request.form()

        try:
            await get_admin_payload(token=token)
        except HTTPException:
            return await request.form()

        return True


authentication_backend: AdminAuth = AdminAuth(secret_key="some")
