"""
Модуль с эндпоинтами приложения "feedback".
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.v1.crud.feedback import feedback_v1_crud
from src.api.v1.schemas.feedback import FeedbackSend
from src.database.database import AsyncSession, get_async_session

router_feedback: APIRouter = APIRouter(
    prefix='/feedbacks',
    tags=['Feedback'],
)


@router_feedback.post(
    path='/send',
)
async def feedback_send(
    feedback_data: FeedbackSend,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Осуществляет регистрацию обращения пользователя из формы обратной связи.
    """
    await feedback_v1_crud.create(
        obj_values=feedback_data.model_dump(),
        session=session,
    )
    return JSONResponse(
        content={'feedback': 'Ваше сообщение успешно отправлено'},
        status_code=status.HTTP_201_CREATED,
    )
