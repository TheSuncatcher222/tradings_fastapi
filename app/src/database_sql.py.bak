"""
Модуль соединения с базой данных посредством
библиотеки Databases и написанием чистых SQL запросов.

Не используется.
"""

# INFO: databases 0.8.0 requires sqlalchemy<1.5,>=1.4.42
from databases import Database

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db: Database = Database(url=DATABASE_URL)


"""Управление соединением в базой данных."""


async def connect_to_database():
    """Осуществляет соединение с базой данных."""
    await db.connect()


async def disconnect_from_database():
    """Осуществляет отключение от базы данных."""
    await db.disconnect()


"""Пример запроса."""


async def query_example(email: str):

    def _validate_email(email: str) -> str:
        """
        Производит валидацию email и защищает от SQL инъекций.
        Лучше использовать Pydantic.
        """
        # Какая-та логика
        return email

    validated_email: str = _validate_email(email=email)
    query: str = (
        'SELECT email '
        'FROM TABLE_NAME '
        'WHERE email = :email'
        ';'
    )
    values: dict[str, any] = {
        'email': validated_email,
    }
    await db.execute(query=query, values=values)
    return
