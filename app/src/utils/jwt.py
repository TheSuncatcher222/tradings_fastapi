"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции работы с JWT токенами.
"""

from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from src.config.config import settings


async def jwt_generate_pair(
    user_id: int,
    is_admin: bool = False,
    is_to_refresh: bool = False,
    is_salesman: bool = False,
) -> tuple[str, int, str, int]:
    """
    Создает пару JWT токенов доступа и обновления с payload:
        - id: ID пользователя
        - exp: дата окончания срока жизни (Unix Epoch)
        - is_admin: статус администратора (если пользователь им является)

    Возвращает кортеж, содержащий данные в следующем порядке:
        1) JWT access
        2) JWT access expires
        3) JWT refresh
        4) JWT refresh expires

    Если "is_to_refresh == True" - создает и возвращает только токен доступа.
    """
    payload: dict[str, dict[str, any]] = {
        'sub': str(user_id)
    }
    if is_admin:
        payload['is_admin'] = is_admin
    if is_salesman:
        payload['is_salesman'] = is_salesman

    access_token, exp_access = await _jwt_generate(
        payload=payload,
        token_type=settings.JWT_TYPE_ACCESS,
    )
    if is_to_refresh:
        refresh_token = None
        exp_refresh = None
    else:
        refresh_token, exp_refresh = await _jwt_generate(
            payload=payload,
            token_type=settings.JWT_TYPE_REFRESH,
        )

    return access_token, exp_access, refresh_token, exp_refresh


async def jwt_decode(jwt_token: str) -> dict[str, any]:
    """
    Читает, валидирует информацию JWT токена.

    Возвращает данные из payload.

    Вызывает HTTPException при возникновении исключений:
        - ExpiredSignatureError: если подпись недействительна
        - JWTClaimsError: если истек срок действия
        - JWTError: произошла ошибка чтения
    """
    try:
        return jwt.decode(
            token=jwt_token,
            key=settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM,],
        )
    except (ExpiredSignatureError, JWTClaimsError, JWTError):
        raise HTTPException(
            detail='Токен недействителен или срок его действия истек',
            status_code=401,
        )


async def _jwt_generate(payload: dict[str, any], token_type: str) -> tuple[str, int]:
    """
    Создает JWT токен с указанными параметрами payload и token_type.

    Возвращает токен и время жизни (Unix).
    """
    if token_type == settings.JWT_TYPE_ACCESS:
        exp_time_sec: int = settings.JWT_ACCESS_EXPIRATION_SEC
    elif token_type == settings.JWT_TYPE_REFRESH:
        exp_time_sec: int = settings.JWT_REFRESH_EXPIRATION_SEC
    else:
        token_type: str = 'unknown'
        exp_time_sec: int = 0

    exp_datetime: datetime = datetime.now() + timedelta(seconds=exp_time_sec)
    exp_unix: int = int(exp_datetime.timestamp())
    payload['exp'] = exp_unix
    payload['iss'] = settings.DOMAIN_NAME
    payload['type'] = token_type

    token: str = jwt.encode(
        claims=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token, exp_unix
