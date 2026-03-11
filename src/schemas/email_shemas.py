from pydantic import BaseModel, Field, EmailStr


class EmailSendSchemas(BaseModel):
    emails: list[EmailStr] = Field(..., description="список email адресов")
    message: str = Field("", description="текст сообщение")
    subject: str = Field("", description="тема сообщения")


example_send_message = {
    "1": {
        "summary": "Себе",
        "value": {
            "emails": ["anikeev.maks@rambler.ru"],
            "message": "Я пишу тебе с приветом рассказать что солнце встало",
            "subject": "Ха-ха От Backend_Course",
        },
    },
    "2": {
        "summary": "Дэри",
        "value": {
            "emails": ["anikeevadarina29@gmail.com"],
            "message": "Дэри, Я пишу тебе с приветом рассказать, что солнце встало",
            "subject": "От папы",
        },
    },
    "3": {
        "summary": "Куся",
        "value": {
            "emails": ["ultrakat22@gmail.com"],
            "message": "Поцелуйчик от меня. Я тебя люблю!",
            "subject": "От Кусю",
        },
    },
    "4": {
        "summary": "Общая",
        "value": {
            "emails": [
                "ultrakat22@gmail.com",
                "anikeevadarina29@gmail.com",
                "anikeev.maks@rambler.ru",
            ],
            "message": "Всем привет от папы!!!",
            "subject": "Проверка общей рассылки",
        },
    },
}
