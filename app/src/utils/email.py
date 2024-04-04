"""
Модуль с вспомогательными функциями приложения "user".
"""

from email.message import EmailMessage
import smtplib

from src.config.config import settings

ATTACHMENT_KEYS: set[str] = {'filepath', 'filename', 'maintype', 'subtype'}


def send_mail(
    subject: str,
    content: str,
    to: str,
    frm: str = settings.SMTP_USER,
    attachments: list[dict[str, str]] = [{}],
) -> None:
    """Отправляет сообщение пользователю на электронную почту."""
    email: EmailMessage = EmailMessage()
    email['Subject'] = subject
    email['From'] = frm
    email['To'] = to
    email.set_content(content)

    for attach in attachments:
        if not ATTACHMENT_KEYS.issubset(attach.keys()):
            continue
        with open(file=attach['filepath'], mode='rb') as file_obj:
            email.add_attachment(
                file_obj.read(),
                maintype=attach['maintype'],
                subtype=attach['subtype'],
                filename=attach['filename'],
            )

    if settings.SMTP_PROTOCOL == 'TLS':
        with smtplib.SMTP(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
            smtp.send_message(email)
    else:
        with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
            smtp.send_message(email)

    return
