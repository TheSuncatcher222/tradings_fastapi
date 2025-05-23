"""Базовый модуль хранения роутеров API v1."""

from fastapi import APIRouter

from src.api.v1.routers.auth import router_auth
from src.api.v1.routers.feedback import router_feedback
from src.api.v1.routers.product import router_product
from src.api.v1.routers.user import router_users

router_api_v1: APIRouter = APIRouter()

ROUTERS: list[APIRouter] = [
    router_auth,
    router_feedback,
    router_product,
    router_users,
]

for router in ROUTERS:
    router_api_v1.include_router(
        router=router,
    )
