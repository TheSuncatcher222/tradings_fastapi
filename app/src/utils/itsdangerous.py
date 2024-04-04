"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции работы с библиотекой ItsDangerous.
"""

from itsdangerous import URLSafeTimedSerializer, BadSignature

from src.config.config import settings

SALT: bytes = (settings.SALT).encode(settings.PASS_ENCODE)


async def dangerous_token_generate(data: dict[str, any]) -> str:
    """Генерирует уникальный токен, содержащий данные из параметров функции."""
    serializer: URLSafeTimedSerializer = await _get_dangerous_serializer()
    return serializer.dumps(obj=data)


async def dangerous_token_verify(token, expiration: int = settings.ONE_DAY_SEC) -> any:
    """
    Верифицирует и возвращает данные из уникального токена.

    Если токен невалидный - возвращает None.
    """
    serializer: URLSafeTimedSerializer = await _get_dangerous_serializer()
    try:
        return serializer.loads(token, max_age=expiration)
    except BadSignature:
        return None


async def _get_dangerous_serializer() -> URLSafeTimedSerializer:
    """Инициализирует сериализатор генерации токенов."""
    return URLSafeTimedSerializer(
        secret_key=settings.SECRET_KEY,
        salt=SALT,
    )
