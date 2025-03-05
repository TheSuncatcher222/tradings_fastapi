"""Модуль с классом CRUD запросов в базу данных для модели UsedPassResetToken."""

from src.database.base_async_crud import BaseAsyncCrud
from src.database.base_sync_crud import BaseSyncCrud
from src.models.feedback import Feedback


# TODO. Запретить прочие методы.
class FeedbackV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице Feedback."""


feedback_v1_crud = FeedbackV1Crud(model=Feedback)


class FeedbackV1CrudSync(BaseSyncCrud):
    """Класс CRUD запросов к базе данных к таблице Feedback."""


feedback_v1_crud_sync = FeedbackV1CrudSync(model=Feedback)
