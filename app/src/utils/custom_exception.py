"""
Модуль с вспомогательными функциями для формирования ошибок и их сообщений.
"""

from pydantic import ValidationError


class CustomValidationTypes:
    """Класс представления типов ошибок валидации Pydantic."""

    # INFO. Используется, если в форме отсутствует обязательное значение
    MISSING: str = 'Missing'
    # INFO. Используется, если пользователю по каким-то причинам запрещено действие
    NOT_ALLOWED: str = 'Not_allowed'
    # INFO. Используется, если у пользователя недостаточно средств для покупки
    NOT_ENOUGH_MONEY: str = 'Not_enough_money'
    # INFO. Используется, если в форму Pydantic введено некорректное значение
    VALUE_ERROR: str = 'Value_error'

    @classmethod
    def form_msg_from_type(
        cls,
        type_: str,
        msg: str,
    ) -> str:
        """Возвращает значение из типа ошибки."""
        if type_ == cls.MISSING:
            return f'Field required'
        if type_ == cls.NOT_ALLOWED:
            return f'Not Allowed, {msg}'
        if type_ == cls.NOT_ENOUGH_MONEY:
            return  f'Not enough money, {msg}'
        if type_ == cls.VALUE_ERROR or type_ == cls.VALUE_ERROR.lower():
            if msg.startswith('Value error,'):
                return msg
            return f'Value error, {msg}'
        return f'Error, {msg}'


def form_pydantic_like_validation_error(
    type_: str,
    loc: list[str] | None,
    msg: str,
    input_: dict[str, any],
) -> dict[str, any]:
    """Формирует ошибку валидации, повторяя структуру сообщения FastAPI."""
    msg: str = CustomValidationTypes.form_msg_from_type(type_=type_, msg=msg)
    return {
        'type': type_,
        'loc': loc,
        'msg': msg,
        'input': input_,
    }


def form_manual_pydantic_validation_error(
    PydanticValidationError: ValidationError,
) -> dict[str, any]:
    """Приводит ошибку валидации Pydantic к структуре сообщения FastAPI."""
    errors: list[dict[str, any]] = PydanticValidationError.errors()
    for err in errors:
        if err['type'] == 'string_type':
            err['type'] = CustomValidationTypes.MISSING
        err['msg'] = CustomValidationTypes.form_msg_from_type(
            type_=err['type'],
            msg=err['msg'],
        )
        err['loc'] = ['body', *err['loc']]
        err['ctx'] = {}
        del err['url']
    return errors
