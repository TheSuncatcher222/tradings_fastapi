"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции шифрования паролей.
"""

from hashlib import pbkdf2_hmac
from src.config.config import settings

SALT: bytes = (settings.SALT).encode(settings.PASS_ENCODE)


def hash_password(raw_password: str) -> str:
    """Создает хэш пароля для сохранения в базе данных."""
    hashed_password: str = str(
        # TODO: перейти на passlib
        #       https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#install-passlib
        pbkdf2_hmac(
            hash_name=settings.HASH_NAME,
            password=raw_password.encode(settings.PASS_ENCODE),
            salt=SALT,
            iterations=settings.ITERATIONS,
        ),
    )
    return hashed_password
