"""Модуль инициализации Celery."""

from celery import Celery

from src.config.config import (
    TimeIntervals,
    settings,
)

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
        'schedule': TimeIntervals.SECONDS_IN_1_DAY,
    },
    'send_missed_feedbacks_to_email': {
        # Проверяет базу данных и ищет неотправленные обращения.
        'task': 'src.celery_app.feedback.tasks.send_missed_feedbacks_to_email',
        'schedule': TimeIntervals.SECONDS_IN_5_MINUTES,
    },
}


class CeleryPriority:
    """
    Класс с приоритетами задач Celery.
    """

    NONE: int = 9
    VERY_LOW: int = 8
    LOW: int = 7
    MEDIUM: int = 5
    HIGH: int = 3
    VERY_HIGH: int = 2
    IMPORTANT: int = 1
    MOST_IMPORTANT: int = 0
