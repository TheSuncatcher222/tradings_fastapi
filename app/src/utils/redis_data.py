"""
Модуль с вспомогательными функциями для извлечения и сохранения данных в Redis.

Использование хранилища Redis для ручного извлечения и сохранения данных
осуществляется через функции redis_get и redis_set соответственно.

Для кеширования Response данных используется декоратор @cache_data
(инициализирован в lifespan при запуске FastAPI в main.py):

    ```
    from fastapi_cache.decorator import cache
    @router.get(...)
    @cache(expire=10)
    async def get(...):
        return Response(...)
    ```

"""

import json

from src.database.database import redis_engine


def redis_delete(key: str) -> None:
    """Удаляет данные из Redis по указанному ключу."""
    redis_engine.delete(key)
    return


def redis_get(
    key: str,
    get_ttl: bool = False,
) -> any:
    """
    Извлекает данные из Redis по указанному ключу
    в типах данных Python.

    Если get_ttl=True, то возвращается TTL в секундах (-1, если ключа не существует).
    """
    data: any = redis_engine.get(name=key)
    if data is not None:
        try:
            data: any = json.loads(s=data)
        except json.JSONDecodeError:
            pass

    if get_ttl:
        return data, redis_engine.ttl(name=key)

    return data


def redis_get_ttl(key: str) -> int:
    """
    Извлекает TTL из Redis по указанному ключу
    (-1, если ключа не существует).
    """
    return redis_engine.ttl(name=key)


def redis_set(key: str, value: any, ex_sec: int = 10) -> None:
    """
    Сохраняет данные в Redis по указанному ключу.

    Преобразует тип данных dict в JSON.
    """
    if isinstance(value, dict):
        value = json.dumps(value)
    redis_engine.set(
        name=key,
        value=value,
        ex=ex_sec,
    )
    return
