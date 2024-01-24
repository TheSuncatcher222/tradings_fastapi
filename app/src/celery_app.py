from celery import Celery

from src.config import REDIS_HOST, REDIS_PORT

celery_app: Celery = Celery(
    'tasks',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
)

celery_app.autodiscover_tasks(['src.feedback'])

celery_app.conf.beat_schedule = {
    'send-missed-feedbacks-to-email-every-10-minutes': {
        'task': 'src.feedback.tasks.send_missed_feedbacks_to_email',
        'schedule': 60,  # INFO: время в секундах.
    },
}
