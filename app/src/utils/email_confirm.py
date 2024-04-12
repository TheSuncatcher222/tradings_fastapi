"""
Модуль с вспомогательными функциями приложения "auth".

Включает в себя функции генерации и отправки кода подтверждения почты.
"""

from src.celery_app.auth.tasks import send_email_confirm_code_to_email
from src.celery_app.celery_app import PRIOR_MEDIUM
from src.config.config import settings
from src.utils.itsdangerous import dangerous_token_generate


async def generate_email_confirm_code(user_id: int, user_email: str) -> str:
    """Генерирует код подтверждения почты пользователя."""
    return await dangerous_token_generate(
        data={
            'user_id': user_id,
            'user_email': user_email,
        }
    )


async def send_email_confirm_code(
    user_id: int,
    user_email: str,
    user_full_name: str,
) -> None:
    """Ставит задачу Celery для отправки ссылки подтверждения электронной почты."""
    confirm_code: str = await generate_email_confirm_code(
        user_id=user_id,
        user_email=user_email,
    )

    if settings.DEBUG_EMAIL:
        user_email: str = settings.SUPPORT_EMAIL_TO
        url_email_confirm: str = (
            f'http://127.0.0.1:8000/api/v1/auth/email-confirm/{confirm_code}'
        )
    else:
        url_email_confirm: str = (
            f'https://{settings.DOMAIN_NAME}/api/v1/auth/email-confirm/{confirm_code}'
        )

    send_email_confirm_code_to_email.apply_async(
        args=(user_full_name, url_email_confirm, user_email),
        priority=PRIOR_MEDIUM,
    )
    return
