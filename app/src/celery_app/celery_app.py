"""Модуль инициализации Celery."""

from celery import Celery

from src.config.config import settings

celery_app: Celery = Celery(
    'tasks',
    backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_CELERY_BACKEND}',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_CELERY_BROKER}',
)

celery_app.autodiscover_tasks(
    [
        'src.celery_app.auth',
        'src.celery_app.feedback',
    ],
)

celery_app.conf.beat_schedule = {
    'delete_expired_pass_reset_tokens': {
        # Удаляет просроченные токены восстановления пароля.
        'task': 'src.celery_app.auth.tasks.delete_expired_pass_reset_tokens',
        'schedule': settings.ONE_DAY_SEC,  # INFO: время в секундах.
    },
    'send_missed_feedbacks_to_email': {
        # Проверяет базу данных и ищет неотправленные обращения.
        'task': 'src.celery_app.feedback.tasks.send_missed_feedbacks_to_email',
        'schedule': 60 * 5,  # INFO: время в секундах.
    },
}


"""Priority levels."""


PRIOR_NONE: int = 9

PRIOR_VERY_LOW: int = 8

PRIOR_LOW: int = 7

PRIOR_MEDIUM: int = 5

PRIOR_HIGH: int = 3

PRIOR_VERY_HIGH: int = 2

PRIOR_IMPORTANT: int = 1

PRIOR_MOST_IMPORTANT: int = 0
