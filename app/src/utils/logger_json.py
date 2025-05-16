"""
Модуль инициализации JSON логера.
"""

from logging import (
    Logger,
    StreamHandler,
    getLogger,
)

from pythonjsonlogger.jsonlogger import JsonFormatter

from src.config.config import settings

LOGGER_FORMAT_DEFAULT: str = (
    # INFO. Время создания записи лога в формате 'YYYY-MM-DD HH:MM:SS,MS'.
    '%(asctime)s '
    # INFO. Уровень логирования.
    '%(levelname)s '
    # INFO. Имя логера.
    '%(name)s '
    # INFO. Имя функции или метода, вызвавшей логирование.
    '%(funcName)s '
    # INFO. Путь к файлу, где было вызвано логирование.
    '%(pathname)s '
    # INFO. Номер строки в файле, где было вызвано логирование.
    '%(lineno)d '
    # INFO. Сообщение лога.
    '%(msg)s'
)

LOG_LEVEL_NOTSET: int = 0
LOG_LEVEL_DEBUG: int = 10
LOG_LEVEL_INFO: int = 20
LOG_LEVEL_WARNING: int = 30
LOG_LEVEL_ERROR: int = 40
LOG_LEVEL_CRITICAL: int = 50

LOG_LEVEL_DEFAULT: int = LOG_LEVEL_DEBUG if settings.DEBUG_LOGGING else LOG_LEVEL_INFO

logging_levels: dict[str, int] = {
    'NOTSET': LOG_LEVEL_NOTSET,
    'DEBUG': LOG_LEVEL_DEBUG,
    'INFO': LOG_LEVEL_INFO,
    'WARNING': LOG_LEVEL_WARNING,
    'ERROR': LOG_LEVEL_ERROR,
    'CRITICAL': LOG_LEVEL_CRITICAL,
}


class LoggerJson:
    """
    Логер с поддержкой JSON формата.

    Пример использования (extra необходимо указывать плоским словарем):
        # format: '%actual_datetime% %levelname% %name% %funcName% %pathname% %lineno% %msg%'
        my_logger_json = LoggerJson(logger_name='test_logger').logger
        my_logger_json.warning(
            msg='message',
            extra={
                'key': 'value',
            },
        )

    Вывод:
        {
            "asctime": "2000-00-01 00:00:00,000",
            "levelname": "WARNING",
            "name": "test_logger",
            "funcName": "<module>",
            "pathname": "c:\\test_case\\test.py",
            "lineno": 777,
            "msg": "message",
            "key": "value"
        }
    """
    def __init__(
        self,
        *,
        logger_name: str,
        log_min_level: int = LOG_LEVEL_INFO,
    ):
        self.logger: Logger = getLogger(name=logger_name)
        # INFO. Настройка формата логера.
        self.log_handler = StreamHandler()
        self.formatter = JsonFormatter(LOGGER_FORMAT_DEFAULT)
        self.log_handler.setFormatter(self.formatter)
        # INFO. Настройка логера.
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(log_min_level if log_min_level in logging_levels else LOG_LEVEL_INFO)


# INFO. Логгеры для модулей.


LoggerJsonAuth: Logger = LoggerJson(
    logger_name='Auth',
    log_min_level=LOG_LEVEL_DEFAULT,
).logger

LoggerJsonEmail: Logger = LoggerJson(
    logger_name='Email',
    log_min_level=LOG_LEVEL_DEFAULT,
).logger

LoggerJsonFeedback: Logger = LoggerJson(
    logger_name='Feedback',
    log_min_level=LOG_LEVEL_DEFAULT,
).logger

LoggerJsonRabbitMQ: Logger = LoggerJson(
    logger_name='RabbitMQ',
    log_min_level=LOG_LEVEL_DEFAULT,
).logger

LoggerJsonUser: Logger = LoggerJson(
    logger_name='User',
    log_min_level=LOG_LEVEL_DEFAULT,
).logger
