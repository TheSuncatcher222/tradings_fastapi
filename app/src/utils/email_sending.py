"""
Модуль с вспомогательными функциями приложения "user".
"""

from email import header
from email.message import EmailMessage
import smtplib
from pathlib import Path
from typing import Sequence

from app.src.config.config import (
    settings,
    DIR_EMAIL_LOCAL,
)
from app.src.utils.datetime_calc import datetime_now_utc
from app.src.utils.logger_json import (
    Logger,
    LoggerJsonEmail,
)
from app.src.utils.storage import parse_file_info

logger: Logger = LoggerJsonEmail


def send_mail(
    subject: str,
    content: str,
    to: str,
    frm: str = settings.SMTP_USER,
    attachments_paths: list[str] | None = None,
) -> bool:
    """
    Отправляет сообщение пользователю на электронную почту.

    Возвращает словарь, содержащий ошибки отправок.
    """
    email: EmailMessage = EmailMessage()
    email['Subject'] = subject
    email['From'] = frm
    email['To'] = to
    email.set_content(content)

    if attachments_paths:
        for file_path in attachments_paths:
            with open(file=file_path, mode='rb') as file:
                filename, maintype, subtype = parse_file_info(file=file)
                email.add_attachment(
                    file.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=filename,
                )

    errors: None | dict[str, str] = None
    try:
        if settings.DEBUG_EMAIL_SAVE_LOCAL:
            __save_email_to_local_file(email=email)
        elif settings.SMTP_PROTOCOL == 'TLS':
            with smtplib.SMTP(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
                errors: dict[str, str] = smtp.send_message(email) or {}
        else:
            with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
                smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
                errors: dict[str, str] = smtp.send_message(email) or {}
    except smtplib.SMTPServerDisconnected as err:
        errors: dict[str, str] = {'SMTPServerDisconnected': err}
    except Exception as err:
        errors: dict[str, str] = {'UnhandledException': err}

    if errors:
        __log_errors(
            errors=errors,
            email_data={
                'subject': subject,
                'to': to,
                'frm': frm,
            },
        )

    return True if not errors else False


def __decode_header_value(value: str) -> str:
    """Декодирует заголовки писем в человекочитаемый формат."""
    if not value:
        return ""
    decoded_parts: list[tuple[any]] = header.decode_header(value)
    return "".join(
        part.decode(encoding or "utf-8") if isinstance(part, bytes) else part
        for part, encoding in decoded_parts
    )

def __decode_email_body(email: EmailMessage) -> str:
    """Декодирует тело email, если оно закодировано в base64."""
    if email.get_content_maintype() == "multipart":
        for part in email.iter_parts():
            if part.get_content_maintype() == "text":
                return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
    else:
        return email.get_payload(decode=True).decode(email.get_content_charset() or "utf-8")
    return ""


def __log_errors(
    errors: dict[str, any],
    email_data: dict[str, any],
) -> None:
    """
    Логирует ошибки при отправке электронных писем.
    """
    err_messages: list[str] = []
    for key, value in errors.items():
        if isinstance(value, Sequence):
            value: str = '\n'.join(value)
        elif isinstance(value, Exception):
            value: str = str(value)
        err_messages.append(f'{key}: {value}')

    logger.critical(
        msg='Errors while sending emails:' + '\n'.join(err_messages),
        extra=email_data,
    )

    return


def __save_email_to_local_file(email: EmailMessage):
    """Сохраняет email в локальный .eml файл с расшифрованными заголовками."""
    subject: str = __decode_header_value(email["Subject"])
    to_addr: str = __decode_header_value(email["To"])
    body: str = __decode_email_body(email)
    datetime: str = datetime_now_utc(str_convert=True, str_format='%Y-%m-%d_%H-%M-%S-%f')

    DIR_EMAIL_LOCAL.mkdir(parents=True, exist_ok=True)
    email_path: Path = DIR_EMAIL_LOCAL / f"{datetime}_{to_addr}.eml"
    with email_path.open("w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"To: {to_addr}\n")
        f.write(f"Datetime: {datetime}\n\n")
        f.write(body)
    return
