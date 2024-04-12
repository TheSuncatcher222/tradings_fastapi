"""Модуль с классом CRUD запросов в базу данных для модели UsedPassResetToken."""

from src.api.base_async_crud import BaseAsyncCrud
from src.models.feedback import Feedback


# TODO. Запретить прочие методы.
class FeedbackV1Crud(BaseAsyncCrud):
    """Класс CRUD запросов к базе данных к таблице Feedback."""

    pass


feedback_v1_crud = FeedbackV1Crud(model=Feedback)
