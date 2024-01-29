"""
Модуль с вспомогательными функциями приложения "user".
"""

from email.message import EmailMessage
import smtplib

from src.config import SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_PROTOCOL, SMTP_USER


def send_mail(content: str, subject: str, to: str) -> None:
    """Отправляет сообщение пользователю на электронную почту."""
    email: EmailMessage = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = to
    email.set_content(content)

    if SMTP_PROTOCOL == 'TLS':
        with smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(user=SMTP_USER, password=SMTP_PASSWORD)
            smtp.send_message(email)
    else:
        with smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT) as smtp:
            smtp.login(user=SMTP_USER, password=SMTP_PASSWORD)
            smtp.send_message(email)

    return
