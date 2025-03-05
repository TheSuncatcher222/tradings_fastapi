"""
Модуль с валидаторами приложения "user".
"""

from re import fullmatch


class CompanyParams:
    """Класс с параметрами компаний."""

    DESCRIPTION_LEN_MAX: int = 250
    NAME_LEN_MAX: int = 30
    IMAGE_LEN_MAX: int = 200


class UserBankCardParams:
    """Класс с параметрами банковских карт пользователей."""

    CARDHOLDER_LEN_MAX: int = 30
    NUMBER_LEN_MAX: int = 16
    TITLE_LEN_MAX: int = 30


class UserParams:
    """Класс с параметрами пользователей."""

    # INFO: в pydantic.EmailStr разрешенные длины строк составляют 64@63.63
    EMAIL_LEN_MAX: int = 64 + 1 + 63 + 1 + 63

    NAME_FIRST_ERROR: str = 'Укажите правильное имя (например: Иван или Анна-Мария)'
    NAME_LAST_ERROR: str = 'Укажите правильную фамилию (например: Петров или Баронесса-Ивальди фон Бремзен)'
    # INFO: существуют фамилии с одной буквой, необходимо производить
    #       проверку на то, что имя не начинается и не заканчивается на "-".
    NAME_LEN_MAX: int = 25
    NAME_REGEXP: str = r'^[А-ЯЁа-яё\s\-]{1,25}$'

    PASSWORD_HASHED_LEN_MAX: int = 256
    PASSWORD_RAW_LEN_MAX: int = 50
    PASSWORD_RAW_LEN_MIN: int = 8
    PASSWORD_SPECIAL_CHARS: str = '!_@#$%^&+='

    # INFO. Номера в БД хранятся в формате набора цифр без иных знаков.
    #       7 - это городской номер без кодов
    #       20 - существующее значение в БД, принят запас по длине.
    PHONE_LEN_MAX: int = 20
    PHONE_REGEX: str = r'^[0-9]{7,20}$'
    PHONE_ERROR: str = 'Введите номер телефона, состоящий от 7 до 20 цифр в формате XХХХХХХХХХХ.'
    PHONE_ERROR_RUS: str = 'Для абонентов РФ необходимо указывать номер в формате 79ХХХХХХХХХ.'

    @classmethod
    def get_password_validators(cls) -> dict[str, str]:
        """Возвращает список валидаторов пароля."""
        return {
            lambda s: cls.PASSWORD_RAW_LEN_MIN <= len(s) <= cls.PASSWORD_RAW_LEN_MAX:
                f'\n- длина от {cls.PASSWORD_RAW_LEN_MIN} до {cls.PASSWORD_RAW_LEN_MAX} символов',
            lambda s: any(char.isdigit() for char in s):
                '\n- включает хотя бы одну цифру (0-9)',
            lambda s: any(char.islower() for char in s):
                '\n- включает хотя бы одну прописную букву (a-z)',
            lambda s: any(char.isupper() for char in s):
                '\n- включает хотя бы одну заглавную букву (A-Z)',
            lambda s: any(char in cls.PASSWORD_SPECIAL_CHARS for char in s):
                f'\n- включает хотя бы один специальный символ ({cls.PASSWORD_SPECIAL_CHARS})',
        }


def validate_user_company_description(value: str):
    """Производит валидацию описания компании."""
    if not value or len(value) > CompanyParams.DESCRIPTION_LEN_MAX:
        raise ValueError(f'Описание компании должно содержать от 1 до {CompanyParams.DESCRIPTION_LEN_MAX} символов')
    return value


def validate_user_company_name(value: str):
    """Производит валидацию названия компании продавца."""
    if not value or len(value) > CompanyParams.NAME_LEN_MAX:
        raise ValueError(f'Название компании должно содержать от 1 до {CompanyParams.NAME_LEN_MAX} символов')
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
        in UserParams.get_password_validators().items()
        if not condition(value)
    ]
    if len(errors) > 0:
        raise ValueError(
            'Ваш пароль не удовлетворят критериям:' +
            ''.join(errors),
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

    if not fullmatch(pattern=UserParams.PHONE_REGEX, string=value):
        raise ValueError(UserParams.PHONE_ERROR)
    if value.startswith('89'):
        raise ValueError(UserParams.PHONE_ERROR_RUS)
    return value


def validate_user_name(value: str, err: str) -> str:
    """
    Производит валидацию поля модели для имени или фамилии.

    Переводит символы поля в title регистр.
    """
    if (
        not fullmatch(UserParams.NAME_REGEXP, value)
        or
        value.startswith('-')
        or
        value.endswith('-')
    ):
        raise ValueError(err)
    return value.title()


def validate_user_new_password(value: str, current_password: str) -> str:
    """Валидатор для поля "new_password" схемы "AuthPasswordChangeSchema"."""
    if value and value == current_password:
        raise ValueError('Прежний и новый пароли должны отличаться.')
    return validate_user_password(value=value)


def validate_user_new_password_confirm(value: str, new_password: str) -> str:
    """Валидатор для поля "new_password_confirm" схемы "AuthPasswordChangeSchema"."""
    if value and value != new_password:
        raise ValueError('Пароли не совпадают.')
    return value
