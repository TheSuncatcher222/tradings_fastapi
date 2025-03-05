"""
Модуль с валидаторами приложения "feedback".
"""


class FeedbackParams:
    """Класс с параметрами формы обратной связи пользователей."""

    CONTACTS_LEN_MAX: int = 50
    FILE_LEN_MAX: int = 255
    MESSAGE_LEN_MAX: int = 200
    SUBJECT_LEN_MAX: str = 50
    USERNAME_LEN_MAX: int = 50


def validate_feedback_contacts(value: str) -> str:
    """
    Производит валидацию поля 'contacts'.

    Производит проверку только по длине.
    """
    if value is not None and len(value) > FeedbackParams.CONTACTS_LEN_MAX:
        raise ValueError('Укажите корректные контактные данные')
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
    if value_len > FeedbackParams.MESSAGE_LEN_MAX:
        raise ValueError(
            f'Текст обращения превышает {FeedbackParams.MESSAGE_LEN_MAX} символов '
            f'(сейчас {value_len})',
        )
    return value


def validate_feedback_username(value: str) -> str:
    """Производит валидацию поля 'username'."""
    value_len: int = len(value)
    if value_len > FeedbackParams.USERNAME_LEN_MAX:
        raise ValueError(
            f'Имя превышает допустимую длину в {FeedbackParams.USERNAME_LEN_MAX} символов '
            f'(сейчас {value_len} символов)',
        )
    return value


def validate_feedback_subject(value: str) -> str:
    """Производит валидацию поля 'subject'."""
    if len(value) == 0:
        raise ValueError(
            'Укажите тему обращения',
        )
    if len(value) > FeedbackParams.SUBJECT_LEN_MAX:
        raise ValueError(
            f'Тема обращения не должна превышать {FeedbackParams.SUBJECT_LEN_MAX} символов '
            f'(сейчас {len(value)})',
        )
    return value


def validate_feedback_text(value: str) -> str:
    """Производит валидацию поля 'text'."""
    if len(value) == 0:
        raise ValueError(
            'Укажите текст обращения',
        )
    if len(value) > FeedbackParams.TEXT_LEN_MAX:
        raise ValueError(
            f'Текст обращения не должен превышать {FeedbackParams.TEXT_LEN_MAX} символов '
            f'(сейчас {len(value)})',
        )
    return value
