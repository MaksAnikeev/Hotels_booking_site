from fastapi import APIRouter, Body, BackgroundTasks

from src.api.routers.utils import send_email_service
from src.schemas.email_shemas import EmailSendSchemas, example_send_message

router = APIRouter(prefix="/mail", tags=["Отправка почты от моего gmail"])


@router.post("/email")
async def send_email(
    background_tasks: BackgroundTasks,
    email_data: EmailSendSchemas = Body(openapi_examples=example_send_message),
):
    background_tasks.add_task(send_email_service, **email_data.model_dump(mode="json"))
    return {
        "status": "OK",
        "description": f"Отправляем сообщение '{email_data.message}' на адреса {email_data.emails}.",
    }
