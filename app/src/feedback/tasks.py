"""
Модуль с задачами для Celery в приложении "feedback".
"""

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql import select, update
from sqlalchemy.sql.selectable import Select

from src.feedback.models import Feedback
from src.celery_app import celery_app
from src.config import SUPPORT_EMAIL_TO
from src.database import sync_session_maker
from src.user.utils import send_mail


@celery_app.task
def send_feedback_to_mail(feedback_data: dict) -> None:
    """
    Отправляет сообщение из формы обратной связи в тех.поддержку.

    Устанавливает объекту Feedback статус отправленного.
    """
    content: str = (
        f'Зарегистрировано новое обращение №{feedback_data["id"]} '
        f'от {feedback_data["reg_date"]}.'
        '\n\n'
        f'Имя: {feedback_data["name"]}'
        '\n\n'
        f'Почта: {feedback_data["email"]}'
        '\n\n'
        f'Контакты: {feedback_data["contacts"]}'
        '\n\n'
        f'Сообщение: {feedback_data["message"]}'
    )
    subject: str = f'Сообщение из формы обратной связи от {feedback_data["email"]}'

    send_mail(subject=subject, to=SUPPORT_EMAIL_TO, content=content)

    with sync_session_maker() as session:
        update_stmt = update(
            Feedback,
        ).where(
            Feedback.id == feedback_data['id'],
        ).values(
            is_accepted=True,
        )
        session.execute(update_stmt)
        session.commit()

    return


@celery_app.task(name='src.feedback.tasks.send_missed_feedbacks_to_email')
def send_missed_feedbacks_to_email():
    """Проверяет наличие неотправленных обращений и совершает повторную отправку."""
    with sync_session_maker() as session:
        query: Select = select(
            Feedback,
        ).where(
            Feedback.is_accepted == False,
        ).order_by(
            'id',
        ).limit(
            5,
        )
        result: ChunkedIteratorResult = session.execute(query)
        queryset: list = result.fetchall()
    for item in queryset:
        feedback: Feedback = item[0]
        feedback_data: dict[str, str] = {
            'contacts': feedback.contacts,
            'email': feedback.email,
            'id': feedback.id,
            'message': feedback.message,
            'name': feedback.name,
            'reg_date': feedback.reg_date,
        }
        try:
            send_feedback_to_mail(feedback_data=feedback_data)
        except Exception:
            # TODO: добавить логгер.
            pass
    return
