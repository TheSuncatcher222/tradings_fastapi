"""
Модуль с задачами для Celery в приложении "auth".
"""


from app.src.celery_app.celery_app import (
    CeleryPriority,
    celery_app,
)
from app.src.config.config import settings
from app.src.utils.email_sending import send_mail


# TODO. Вынести сообщения в HTML шаблон.


@celery_app.task(
    name='src.celery_app.auth.tasks.send_email_confirm_code_to_email_task',
    ignore_result=True,
    priority=CeleryPriority.MEDIUM,
)
def send_email_confirm_code_to_email_task(
    user_full_name: str,
    url_email_confirm: str,
    to_email: str,
) -> None:
    """Отправляет сообщение для подтверждения электронной почты пользователю."""
    subject: str = f'Регистрация в {settings.DOMAIN_NAME}'
    content: str = (
        f'Добрый день, {user_full_name}.'
        '\n\n'
        f'Спасибо за регистрацию на {settings.DOMAIN_NAME}!'
        '\n\n'
        'Чтобы подтвердить вашу электронную почту, перейдите по следующей ссылке:'
        '\n'
        f'{url_email_confirm}.'
        '\n\n'
        'Если вы не создавали аккаунт, просто игнорируйте это сообщение.'
        '\n\n'
        'С наилучшими пожеланиями,'
        '\n'
        f'Команда поддержки {settings.DOMAIN_NAME}'
    )
    send_mail(subject=subject, to=to_email, content=content)
    return


@celery_app.task(
    name='src.celery_app.auth.tasks.send_password_restore_to_mail_task',
    ignore_result=True,
    priority=CeleryPriority.MEDIUM,
)
def send_password_restore_to_mail_task(link: str, to_email: str) -> None:
    """Отправляет сообщение c ссылкой восстановления пароля пользователю."""
    subject: str = f'Сброс пароля аккаунта'
    content: str = (
        'Добрый день,'
        '\n\n'
        f'Вы запросили восстановление доступа к аккаунту на {settings.DOMAIN_NAME}. '
        'Чтобы продолжить, пожалуйста, воспользуйтесь следующей ссылкой в течении 24 часов:'
        '\n'
        f'{link}'
        '\n\n'
        'Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо. '
        'Также рекомендуем в этом случае сменить пароль учетной записи.'
        '\n\n'
        'С наилучшими пожеланиями,'
        '\n'
        f'Команда поддержки {settings.DOMAIN_NAME}'
    )
    send_mail(subject=subject, to=to_email, content=content)
    return


@celery_app.task(
    name='src.celery_app.auth.tasks.send_password_has_changed_to_mail_task',
    ignore_result=True,
    priority=CeleryPriority.MOST_IMPORTANT,
)
def send_password_has_changed_to_mail_task(user_full_name: str, to_email: str) -> None:
    """Отправляет сообщение-оповещение о смене пароля пользователю."""
    subject: str = f'Изменение пароля аккаунта'
    content: str = (
        f'Добрый день, {user_full_name}.'
        '\n\n'
        'Ваш пароль аккаунта был успешно изменён. Если вы не выполняли '
        'этого действия, пожалуйста, срочно свяжитесь с нами.'
        '\n\n'
        'С наилучшими пожеланиями,'
        '\n'
        f'Команда поддержки {settings.DOMAIN_NAME}'
    )
    send_mail(subject=subject, to=to_email, content=content)
    return
