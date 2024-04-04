"""
Модуль с задачами для Celery в приложении "auth".
"""

from datetime import datetime

from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql import delete

from src.models.auth import UsedPassResetToken
from src.celery_app.celery_app import celery_app
from src.database.database import sync_session_maker
from src.config.config import settings
from src.utils.email import send_mail


# TODO: вынести в CRUD.
@celery_app.task(name='src.celery_app.auth.tasks.delete_expired_pass_reset_tokens')
def delete_expired_pass_reset_tokens():
    """
    Удаляет использованные токены восстановления
    пароля с истекшим сроком жизни.
    """
    with sync_session_maker() as session:
        stmt: Select = delete(
            UsedPassResetToken,
        ).where(
            UsedPassResetToken.exp_date < datetime.utcnow(),
        )
        session.execute(stmt)
        session.commit()
    return


@celery_app.task
def send_email_confirm_code_to_email(
    user_full_name: str,
    url_email_confirm: str,
    to_email: str
) -> None:
    """Отправляет сообщение для подтверждения электронной почты пользователю."""
    # TODO: вынести в константы и использовать .format()
    content: str = (
        f'Здравствуйте, {user_full_name}.'
        '\n\n'
        f'Благодарим за регистрацию на {settings.DOMAIN_NAME}!'
        '\n\n'
        'Для подтверждения вашей электронной почты и начала работы '
        'с вашей учетной записью, пожалуйста, перейдите по ссылке ниже:'
        '\n\n'
        f'{url_email_confirm}.'
        '\n\n'
        'Если вы не регистрировались на {settings.DOMAIN_NAME}, просто проигнорируйте '
        'данное сообщение.'
        '\n\n'
        'С уважением,'
        '\n'
        f'Служба поддержки {settings.DOMAIN_NAME}'
    )
    subject: str = f'Подтверждение электронной почты | {settings.DOMAIN_NAME}'
    send_mail(subject=subject, to=to_email, content=content)
    return


@celery_app.task
def send_password_restore_to_mail(link: str, to_email: str) -> None:
    """Отправляет сообщение c ссылкой восстановления пароля пользователю."""
    # TODO: вынести в константы и использовать .format()
    content: str = (
        'Здравствуйте,'
        '\n\n'
        f'Вы запросили сброс пароля для вашей учетной записи на {settings.DOMAIN_NAME}. '
        'Для завершения процесса, пожалуйста, перейдите по следующей ссылке:'
        '\n\n'
        f'{link}'
        '\n\n'
        'Ссылка будет действительна в течении 24 часов.'
        '\n\n'
        'После перехода по ссылке вы сможете установить новый пароль '
        'для вашей учетной записи.'
        '\n\n'
        'Если вы не инициировали этот запрос, пожалуйста, проигнорируйте '
        'это сообщение или свяжитесь с нами в ответом письме.'
        '\n\n'
        'С уважением,'
        '\n'
        f'Служба поддержки {settings.DOMAIN_NAME}'
    )
    subject: str = f'Сброс пароля учетной записи | {settings.DOMAIN_NAME}'
    send_mail(subject=subject, to=to_email, content=content)
    return


@celery_app.task
def send_password_has_changed_to_mail(user_full_name: str, to_email: str) -> None:
    """Отправляет сообщение-оповещение о смене пароля пользователю."""
    # TODO: вынести в константы и использовать .format()
    content: str = (
        f'Здравствуйте, {user_full_name}.'
        '\n\n'
        'Уведомляем, что пароль для вашей учетной записи был только что изменен.'
        '\n\n'
        'Если вы не инициировали этот запрос, пожалуйста, немедленно '
        'свяжитесь с нами в ответом письме.'
        '\n\n'
        'С уважением,'
        '\n'
        f'Служба поддержки {settings.DOMAIN_NAME}'
    )
    subject: str = f'Изменение пароля учетной записи | {settings.DOMAIN_NAME}'
    send_mail(subject=subject, to=to_email, content=content)
    return
