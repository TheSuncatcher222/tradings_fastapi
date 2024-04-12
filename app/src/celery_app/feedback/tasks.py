"""
Модуль с задачами для Celery в приложении "feedback".
"""

import shutil

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql import select, update
from sqlalchemy.sql.selectable import Select

from src.models.feedback import Feedback
from src.celery_app.celery_app import celery_app
from src.config.config import settings
from src.database.database import sync_session_maker
from src.utils.email import send_mail


@celery_app.task
def send_feedback_to_mail(feedback_data: dict) -> None:
    """
    Отправляет сообщение из формы обратной связи в тех.поддержку.

    Устанавливает объекту Feedback статус отправленного.
    """
    content: str = (
        f'Зарегистрировано новое обращение №{feedback_data["id"]} '
        f'от {feedback_data["created_datetime"]}.'
        '\n\n'
        f'Имя: {feedback_data["username"]}'
        '\n\n'
        f'Почта: {feedback_data["email"]}'
        '\n\n'
        f'Контакты: {feedback_data["contacts"]}'
        '\n\n'
        f'Сообщение: {feedback_data["message"]}'
    )
    subject: str = f'Сообщение из формы обратной связи от {feedback_data["email"]}'

    send_mail(subject=subject, to=settings.SUPPORT_EMAIL_TO, content=content)

    with sync_session_maker() as session:
        update_stmt = (
            update(Feedback)
            .where(Feedback.id == feedback_data['id'])
            .values(is_accepted=True)
        )
        session.execute(update_stmt)
        session.commit()

    return


@celery_app.task(name='src.celery_app.feedback.tasks.send_missed_feedbacks_to_email')
def send_missed_feedbacks_to_email():
    """Проверяет наличие неотправленных обращений и совершает повторную отправку."""
    with sync_session_maker() as session:
        query: Select = (
            select(Feedback)
            .where(Feedback.is_accepted == False)
            .order_by('id')
            .limit(20)
        )
        result: ChunkedIteratorResult = session.execute(query)
        # TODO. Зарефакторить.
        queryset: list = result.fetchall()
    for item in queryset:
        feedback: Feedback = item[0]
        feedback_data: dict[str, str] = {
            'contacts': feedback.contacts,
            'email': feedback.email,
            'id': feedback.id,
            'message': feedback.message,
            'username': feedback.username,
            'created_datetime': feedback.created_datetime,
        }
        try:
            send_feedback_to_mail(feedback_data=feedback_data)
        except Exception:
            # TODO: добавить логгер.
            pass
    return


# TODO. Может упасть с ошибкой. Проверить все Celery Tasks на отказоустойчивость.
@celery_app.task
def send_ticket_to_support(
    subject: str,
    content: str,
    frm: str,
    upload_dir: str,
    attachments: list[dict[str, str]] = [{}],
) -> None:
    """
    Отправляет тикет обращения пользователя в службу поддержки
    от лица пользователя.

    Удаляет временные медиа-файлы, которые пользователи
    приложили к тикету.
    """
    if settings.DEBUG_EMAIL:
        frm: str = settings.SMTP_USER
    try:
        send_mail(
            subject=subject,
            content=content,
            to=settings.SUPPORT_EMAIL_TO,
            frm=frm,
            attachments=attachments,
        )
        shutil.rmtree(upload_dir)
    except OSError as err:
        raise OSError(err)
    return
