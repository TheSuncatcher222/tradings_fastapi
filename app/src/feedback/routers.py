"""
Модуль с эндпоинтами приложения "feedback".
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.sql import insert
from sqlalchemy.sql.dml import Insert

from src.database import AsyncSession, get_async_session
from src.feedback.models import Feedback
from src.feedback.schemas import FeedbackSend
from src.feedback.tasks import send_feedback_to_mail

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
    feedback_data: dict[str, any] = feedback_data.model_dump()

    stmt: Insert = insert(Feedback).values(**feedback_data).returning(Feedback)
    result = await session.execute(stmt)
    await session.commit()

    new_feedback: Feedback = result.fetchone()[0]

    feedback_data['id']: int = new_feedback.id
    feedback_data['reg_date']: int = new_feedback.reg_date
    send_feedback_to_mail.delay(feedback_data)

    return JSONResponse(
        content={'feedback': 'Ваше сообщение успешно отправлено!'},
        status_code=status.HTTP_200_OK,
    )
