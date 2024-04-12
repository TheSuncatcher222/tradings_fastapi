"""
Модуль с валидаторами полей моделей базы данных приложения "feedback".
"""

FEEDBACK_CONTACTS_LEN: int = 50
FEEDBACK_MESSAGE_LEN: int = 200
FEEDBACK_USERNAME_LEN: int = 50

TICKET_SUBJECT_MAX_LEN: str = 50
TICKET_TEXT_MAX_LEN: str = 200


def validate_feedback_contacts(value: str) -> str:
    """
    Производит валидацию поля 'contacts'.

    Производит проверку только по длине.
    """
    if value is not None and len(value) > FEEDBACK_CONTACTS_LEN:
        raise ValueError('Укажите корректные контактные данные')
    return value


def validate_feedback_data_process_approve(value: bool) -> str:
    """Производит валидацию поля 'data_process_approve'."""
    if not value:
        raise ValueError(
            'Для отправки обращения необходимо согласиться '
            'с обработкой персональных данных'
        )
    return value


def validate_feedback_email(value: str) -> str:
    """
    Переводит символы email в нижний регистр.

    Валидация структуры email осуществляется автоматически в Pydantic.
    """
    return value.lower()


def validate_feedback_message(value: str) -> str:
    """Производит валидацию поля 'message'."""
    value_len: int = len(value)
    if value_len > FEEDBACK_MESSAGE_LEN:
        raise ValueError(
            f'Текст обращения превышает {FEEDBACK_MESSAGE_LEN} символов '
            f'(сейчас {value_len})'
        )
    return value


def validate_feedback_username(value: str) -> str:
    """Производит валидацию поля 'username'."""
    value_len: int = len(value)
    if value_len > FEEDBACK_USERNAME_LEN:
        raise ValueError(
            f'Имя превышает допустимую длину в {FEEDBACK_USERNAME_LEN} символов '
            f'(сейчас {value_len} символов)'
        )
    return value


def validate_ticket_subject(value: str) -> str:
    """Производит валидацию поля 'subject'."""
    if len(value) == 0:
        raise ValueError(
            'Укажите тему обращения'
        )
    if len(value) > TICKET_SUBJECT_MAX_LEN:
        raise ValueError(
            f'Тема обращения не должна превышать {TICKET_SUBJECT_MAX_LEN} символов '
            f'(сейчас {len(value)})'
        )
    return value


def validate_ticket_text(value: str) -> str:
    """Производит валидацию поля 'text'."""
    if len(value) == 0:
        raise ValueError(
            'Укажите текст обращения'
        )
    if len(value) > TICKET_TEXT_MAX_LEN:
        raise ValueError(
            f'Текст обращения не должен превышать {TICKET_TEXT_MAX_LEN} символов '
            f'(сейчас {len(value)})'
        )
    return value
