"""
Модуль с валидаторами полей моделей базы данных приложения "user".
"""

from re import fullmatch

NL: str = '\n'

COMPANY_DESCRIPTION_MAX: int = 250
COMPANY_NAME_MAX: int = 30

# INFO: в pydantic.EmailStr разрешенные длины строк составляют 64@63.63
USER_EMAIL_LEN: int = 64 + 63 + 63
USER_HASH_PASS_LEN: int = 256
USER_PHONE_LEN: int = 20
USER_USERNAME_LEN: int = 25

USER_NAME_FIRST_ERROR: str = (
    'Укажите правильное имя (например: Иван или Анна-Мария)'
)
USER_NAME_LAST_ERROR: str = (
    'Укажите правильную фамилию (например: Петров или Баронесса-Ивальди фон Бремзен)'
)
# INFO: существуют фамилии с одной буквой, необходимо производить
#       проверку на то, что имя не начинается и не заканчивается на "-".
# INFO: src.models.user.USER_USERNAME_LEN = 25
USER_NAME_MAX_REGEXP: str = r'^[А-ЯЁа-яё\s\-]{1,25}$'

# INFO. Номера в БД хранятся в формате набора цифр без иных знаков.
#       7 - это городской номер без кодов
#       20 - существующее значение в БД, принят запас по длине.
USER_PHONE_MAX_LEN: int = 20
USER_PHONE_REGEX: str = r'^[0-9]{7,20}$'
USER_PHONE_ERROR: str = (
    'Введите номер телефона, состоящий от 7 до 20 цифр в формате XХХХХХХХХХХ.'
)
USER_PHONE_RUS_ERROR: str = (
    'Для абонентов РФ необходимо указывать номер в формате 79ХХХХХХХХХ.'
)

USER_PASS_RAW_LEN_MAX: int = 50
USER_PASS_RAW_LEN_MIN: int = 8
PASS_SPECIAL_CHARS: str = '!_@#$%^&+='

PASS_CHARS_VALIDATORS: dict[str, str] = {
    lambda s: USER_PASS_RAW_LEN_MIN <= len(s) <= USER_PASS_RAW_LEN_MAX: f'{NL}- длина от {USER_PASS_RAW_LEN_MIN} до {USER_PASS_RAW_LEN_MAX} символов',
    lambda s: any(char.isdigit() for char in s): '\n- включает хотя бы одну цифру (0-9)',
    lambda s: any(char.islower() for char in s): '\n- включает хотя бы одну прописную букву (a-z)',
    lambda s: any(char.isupper() for char in s): '\n- включает хотя бы одну заглавную букву (A-Z)',
    lambda s: any(char in PASS_SPECIAL_CHARS for char in s): f'{NL}- включает хотя бы один специальный символ ({PASS_SPECIAL_CHARS})',
}

USER_SALESMAN_COMPANY_DESCRIPTION_LEN: int = 200
USER_SALESMAN_COMPANY_IMAGE_LEN: int = 200
USER_SALESMAN_COMPANY_NAME_LEN: int = 50


def validate_user_company_description(cls, value: str, values: dict):
    """Производит валидацию описания компании."""
    if len(value) == 0 or len(value) > COMPANY_DESCRIPTION_MAX:
        raise ValueError(
            f'Описание компании должно содержать от 1 до {COMPANY_DESCRIPTION_MAX} символов'
        )
    return value


def validate_user_company_name(value: str):
    """Производит валидацию названия компании продавца."""
    if len(value) == 0 or len(value) > COMPANY_NAME_MAX:
        raise ValueError(
            f'Название компании должно содержать от 1 до {COMPANY_NAME_MAX} символов'
        )
    return value


def validate_user_email(value: str) -> str:
    """
    Переводит символы email в нижний регистр.

    Валидация структуры email осуществляется автоматически в Pydantic.
    """
    return value.lower()


def validate_user_password(value: str) -> str:
    """Производит валидацию пароля."""
    errors: list[str] = [
        err_message
        for condition, err_message
        in PASS_CHARS_VALIDATORS.items()
        if not condition(value)
    ]
    if len(errors) > 0:
        raise ValueError(
            'Введите пароль, который удовлетворяет критериям:' +
            ''.join(errors)
        )
    return value


def validate_user_phone(value: str) -> str:
    """
    Производит валидацию номера телефона:
        - необходимо сохранять только цифры (т.е. без "+", " ", "-", "(", ")")
        - для абонентов российских операторов необходимо начинать номер с 7, а не 8

    Валидное значение: 79112223344.
    Невалидное значение по всем критериям: +7 (911) 222-33-44.
    """

    """
        Дополнительная информация по валидации:
        1) Все коды Российских мобильных операторов начинаются с 9ХХ
        2) все коды иных стран, которые начинаются с +8 не содержат далее цифры 9:
            +81  - Япония
            +82 - Южная Корея
            +84 - Вьетнам
            +850 - Северная Корея
            +852 - Гон-Конг
            +853 - Макао
            +855 - Камбоджа
            +856 - Лаос
            +86  - Китай
            +880 - Бангладеш
            +886 - Тайвань
    """

    if not fullmatch(pattern=USER_PHONE_REGEX, string=value):
        raise ValueError(USER_PHONE_ERROR)
    if value.startswith('89'):
        raise ValueError(USER_PHONE_RUS_ERROR)
    return value


def validate_user_name(value: str, err: str) -> str:
    """
    Производит валидацию поля модели для имени или фамилии.

    Переводит символы поля в title регистр.
    """
    if (
        not fullmatch(USER_NAME_MAX_REGEXP, value) or
        value.startswith('-') or
        value.endswith('-')
    ):
        raise ValueError(err)
    return value.title()
