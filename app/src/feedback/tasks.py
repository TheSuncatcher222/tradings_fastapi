"""
Модуль с задачами для Celery в приложении "feedback".
"""

from email.message import EmailMessage
import smtplib

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql import select, update
from sqlalchemy.sql.selectable import Select

from src.feedback.models import Feedback
from src.celery_app import celery_app
from src.config import (
    SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER, SUPPORT_EMAIL_TO,
    USE_SSL, USE_TSL,
)
from src.database import sync_session_maker


@celery_app.task
def send_feedback_to_mail(feedback_data: dict) -> None:
    """
    Отправляет сообщение из формы обратной связи в тех.поддержку.

    Устанавливает объекту Feedback статус отправленного.
    """
    email: EmailMessage = EmailMessage()
    email['Subject'] = f'Сообщение из формы обратной связи от {feedback_data["email"]}'
    email['From'] = SMTP_USER
    email['To'] = SUPPORT_EMAIL_TO
    email.set_content(
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

    if USE_SSL:
        with smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT) as smtp:
            smtp.login(user=SMTP_USER, password=SMTP_PASSWORD)
            smtp.send_message(email)
    else:
        with smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT) as smtp:
            if USE_TSL:
                smtp.starttls()
            smtp.login(user=SMTP_USER, password=SMTP_PASSWORD)
            smtp.send_message(email)

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
