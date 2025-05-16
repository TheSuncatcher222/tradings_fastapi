"""Модуль хранения настроек и переменных окружения сервиса."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DIR_SRC: Path = Path(__file__).parent.parent
DIR_MEDIA: Path = Path(DIR_SRC, 'media')
# INFO. Для хранения email сообщений локально при DEBUG_EMAIL==True.
DIR_EMAIL_LOCAL: Path = Path(DIR_MEDIA, 'email_local')


class Pagination:
    """Класс представления параметров пагинации."""

    LIMIT_DEFAULT: int = 15
    OFFSET_DEFAULT: int = 0


class TimeIntervals:
    """Класс представления таймаутов."""

    # Seconds.

    SECONDS_10: int = 10
    SECONDS_IN_1_MINUTE: int = 60
    SECONDS_IN_5_MINUTES: int = SECONDS_IN_1_MINUTE * 5
    SECONDS_IN_1_HOUR: int = SECONDS_IN_1_MINUTE * 60
    SECONDS_IN_1_DAY: int = SECONDS_IN_1_HOUR * 24

    # Days.

    DAYS_IN_1_MONTH: int = 30

    # Hours.

    HOURS_IN_1_DAY: int = 24
    HOURS_IN_1_MONTH: int = HOURS_IN_1_DAY * DAYS_IN_1_MONTH


class Settings(BaseSettings):
    """
    Класс представления переменных окружения.

    Пояснения к переменным окружения содержатся в app/src/config/.env.example
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="UTF-8",
        extra="allow",
    )

    """Настройки базы данных PostgreSQL."""
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str

    """Настройки базы данных Redis."""
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB_CELERY_BACKEND: int
    REDIS_DB_CELERY_BROKER: int
    REDIS_DB_CACHE: int
    REDIS_DB_CACHE_FASTAPI: int

    """Настройки брокера сообщений RabbitMQ."""
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str

    """Настройки SQLAlchemy Admin."""
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_SECRET_KEY: str

    """Настройки безопасности: тротлинг."""
    BAD_LOGIN_BAN_SEC: int
    BAD_LOGIN_MAX_ATTEMPTS: int
    BAD_LOGIN_EXPIRATION_SEC: int

    """Настройки безопасности: шифрование пароля."""
    HASH_NAME: str
    ITERATIONS: int
    PASS_ENCODE: str
    SALT: str

    """Настройки безопасности: Dangerous токены."""
    SECRET_KEY: str

    """Настройки безопасности: JWT токены."""
    COOKIE_KEY_JWT_REFRESH: str = 'refresh'
    JWT_ALGORITHM: str
    JWT_ACCESS_EXPIRATION_SEC: int
    JWT_REFRESH_EXPIRATION_SEC: int
    JWT_TYPE_ACCESS: str = 'access'
    JWT_TYPE_REFRESH: str = 'refresh'

    """Настройки почтового клиента SMTP."""
    SMTP_HOST: str
    SMTP_PASSWORD: str
    SMTP_PORT: int
    SMTP_PROTOCOL: str
    SMTP_USER: str
    SUPPORT_EMAIL_TO: str

    """Настройки сервера."""
    ADMIN_URL_PREFIX: str
    DEBUG: bool
    DEBUG_CORS: bool
    DEBUG_DB: bool
    DEBUG_EMAIL: bool
    DEBUG_LOGGING: bool
    DOMAIN_IP: str
    DOMAIN_NAME: str
    WORKERS_AMOUNT: int


settings = Settings()
