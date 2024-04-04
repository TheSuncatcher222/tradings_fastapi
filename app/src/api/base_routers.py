"""Базовый модуль хранения роутеров всех версий API."""

from fastapi import APIRouter

from src.api.v1.base_routers import router_api_v1

router_api: APIRouter = APIRouter()

router_api.include_router(
    router=router_api_v1,
    prefix='/v1'
)
