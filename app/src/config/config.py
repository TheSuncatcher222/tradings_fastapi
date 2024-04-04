"""Модуль хранения настроек и переменных окружения сервиса."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DIR_SRC: Path = Path(__file__).parent.parent
DIR_MEDIA: Path = Path(DIR_SRC, 'media')


class Settings(BaseSettings):
    """
    Класс представления переменных окружения.

    Описание переменных указано в .env.example файле.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="UTF-8",
        extra="allow",
    )

    """Данные проекта."""
    DOMAIN_IP: str
    DOMAIN_NAME: str

    """Настройки базы данных PostgreSQL."""
    DB_HOST: str = 'tradings_postgresql_host'
    DB_PORT: int = 5432
    POSTGRES_DB: str = 'tradings_db'
    POSTGRES_PASSWORD: str = 'db_pass'
    POSTGRES_USER: str = 'db_user'

    """Настройки SQLAlchemy Admin."""
    ADMIN_PASSWORD: str = 'admin'
    ADMIN_SECRET_KEY: str = 'string'
    ADMIN_USERNAME: str = 'admin'

    """Настройки базы данных Redis."""
    REDIS_HOST: str = 'tradings_redis_host'
    REDIS_PORT: int = '6379'

    """Настройки безопасности: шифрование пароля."""
    HASH_NAME: str = 'md5'
    ITERATIONS: int = 1000
    PASS_ENCODE: str = 'ASCII'
    SALT: str = 'string'

    """Настройки безопасности: JWT токены."""
    COOKIE_KEY_JWT_REFRESH: str = 'refresh'
    JWT_ALGORITHM: str = 'HS128'
    JWT_ACCESS_EXPIRATION_SEC: int = 60
    JWT_REFRESH_EXPIRATION_SEC: int = 86400
    JWT_TYPE_ACCESS: str = 'access'
    JWT_TYPE_REFRESH: str = 'refresh'

    """Настройки безопасности: Dangerous токены."""
    ONE_DAY_SEC: int = 60 * 60 * 24
    SECRET_KEY: str = 'string'

    """Настройки почтового клиента SMTP."""
    SMTP_HOST: str
    SMTP_PASSWORD: str
    SMTP_PORT: int
    SMTP_PROTOCOL: str
    SMTP_USER: str
    SUPPORT_EMAIL_TO: str

    """Настройки сервера."""
    DEBUG: bool = True
    DEBUG_DB: bool = True
    DEBUG_EMAIL: bool = True


settings = Settings()
