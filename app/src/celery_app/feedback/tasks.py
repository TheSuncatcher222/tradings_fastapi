"""
Модуль с задачами для Celery в приложении "feedback".
"""

from sqlalchemy.orm import Session

from src.api.v1.crud.feedback import feedback_v1_crud_sync
from src.celery_app.celery_app import (
    CeleryPriority,
    celery_app,
)
from src.config.config import settings
from src.database.database import sync_session_maker
from src.models.feedback import Feedback
from src.utils.email_sending import send_mail
from src.utils.logger_json import (
    Logger,
    LoggerJsonFeedback,
)
from src.utils.feedback import delete_feedback_attachments

logger: Logger = LoggerJsonFeedback


@celery_app.task(
    name='src.celery_app.feedback.tasks.send_missed_feedbacks_to_email',
    ignore_result=True,
    priority=CeleryPriority.LOW,
)
def send_missed_feedbacks_to_email():
    """Проверяет наличие ни разу не отправленных обращений и организует их отправку."""
    with sync_session_maker() as session:
        feedbacks: list[Feedback] = feedback_v1_crud_sync.retrieve_all(
            session=session,
        )
        for feedback in feedbacks:
            try:
                __send_feedback_to_mail(
                    feedback=feedback,
                    session=session,
                )
            except Exception:
                continue
    return


def __send_feedback_to_mail(
    feedback: Feedback,
    session: Session,
) -> None:
    """
    Отправляет сообщение из формы обратной связи в тех.поддержку.

    Удаляет feedback и его медиа-файлы в случае успешной отправки.
    """
    subject: str = f'Обращение обратной связи номер {feedback.id}'
    content: str = (
        f'Имя: {feedback.username}'
        '\n'
        f'Контакты: {feedback.contacts}'
        '\n\n'
        f'Сообщение: {feedback.message}'
    )

    if not send_mail(
        subject=subject,
        content=content,
        to=settings.SUPPORT_EMAIL_TO,
        frm=feedback.email,
        attachments_paths=feedback.attachments,
    ):
        return

    delete_feedback_attachments(attachments_paths=feedback.attachments)
    feedback_v1_crud_sync.delete_by_id(
        obj_id=feedback.id,
        session=session,
    )

    return
