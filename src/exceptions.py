from fastapi import HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def init_exception_handlers(app_: FastAPI):
    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        for error in exc.errors():
            if error['type'] == 'extra_forbidden':
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "code": 400,
                        "message": f"Недопустимые поля: {', '.join(error.get('loc', []))}"
                    }
                )

        # Остальные ошибки валидации
        return JSONResponse(
            status_code=422,
            content={"status": "error", "details": exc.errors()}
        )


class CustomException(Exception):
    detail: str = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(CustomException):
    detail = "Объект с такими параметрами не найден"


class HotelNotFoundException(CustomException):
    detail = "Отель с таким ид не найден"


class RoomNotFoundException(CustomException):
    detail = "Номер с таким ид не найден"


class FacilitiesNotFoundException(CustomException):
    detail = "Удобство с таким ид не найдено"


class AllRoomIsBookedException(CustomException):
    detail = "Нет свободных номеров данного класса на выбранную дату"


class AlreadyExistedException(CustomException):
    detail = "Объект с такими параметрами уже существует"


class TooLongParameterException(CustomException):
    detail = "Вводимый параметр недопустимо длинный"


class TooManyObjectsException(CustomException):
    detail = (
        "По данным параметрам найдено несколько объектов, уточните параметры поиска"
    )


class NotAllNecessaryParamsException(CustomException):
    detail = "Переданы не все необходимые параметры"


class NotAllowedParameterException(CustomException):
    detail = "Указаны неверные параметры для изменения"


class IncorrectPasswordException(CustomException):
    detail = "Введен некорректный пароль"


class WrongAccessToken(CustomException):
    detail = "Некорректный токен."


class TimeoutAccessToken(CustomException):
    detail = "Время действия токена истекло."


class EmptyAttributesException(CustomException):
    detail = "Переданный атрибут не может быть пустым или все переданный атрибуты пустые"


class CustomHTTPException(HTTPException):
    status_code = 500
    detail: str | None = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Отель с таким id не найден"


class RoomNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Номер с таким id не найден"


class FacilitiesNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Указаны не существующие удобства"


class HotelOrRoomNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Отель с указанным id или номер с указанным id в этом отеле не найден"


class HotelAlreadyExistedHTTPException(CustomHTTPException):
    status_code = 409
    detail = "Отель с таким названием уже существует"


class UserAlreadyExistedHTTPException(CustomHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class UserNotExistedHTTPException(CustomHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не найден. Необходима регистрация."


class IncorrectPasswordHTTPException(CustomHTTPException):
    status_code = 401
    detail = "Неверно указан логин или пароль"


class IncorrectBookingDateHTTPException(CustomHTTPException):
    status_code = 400
    detail = "Дата выезда должна быть позже даты заезда"


class NotBookingDateHTTPException(CustomHTTPException):
    status_code = 400
    detail = "Не указана полностью временной диапазон date_from date_to"


class NotAccessTokenHTTPException(CustomHTTPException):
    status_code = 401
    detail = "Необходимо залогиниться"


class WrongAccessTokenHTTPException(CustomHTTPException):
    status_code = 401
    detail = "Необходимо залогиниться"


class TimeoutAccessTokenHTTPException(CustomHTTPException):
    status_code = 401
    detail = "Время действия токена истекло. Необходимо залогиниться"


class AllRoomIsBookedExceptionHTTPException(CustomHTTPException):
    status_code = 409
    detail = "Нет свободных номеров данного класса на выбранную дату"


class TooLongParameterHTTPException(CustomHTTPException):
    status_code = 400
    detail = "Вводимый параметр недопустимо длинный, проверьте правильность ввода всех параметров ИД"


class TooManyObjectsHTTPException(CustomHTTPException):
    status_code = 422
    detail = (
        "Поиск осуществляется не по уникальным параметрам,"
        " в результате по данным параметрам найдено несколько объектов, уточните параметры поиска"
    )


class NotAllowedParameterHTTPException(CustomHTTPException):
    status_code = 422
    detail = (
        "У данного объекта нет параметров/атрибутов, которые вы хотите изменить."
        " Уточните название изменяемых атрибутов"
    )

class EmptyPasswordHTTPException(CustomHTTPException):
    status_code = 400
    detail = (
        "Пароль не может быть пустым"
    )

class NotAnyAttributeHTTPException(CustomHTTPException):
    status_code = 400
    detail = (
        "Хотя бы одно поле должно быть непустым"
    )

class EmptyRequestBodyHTTPException(CustomHTTPException):
    status_code = 400
    detail = (
        "Не передано ни одного параметра"
    )

class FacilitiesAlreadyExistedHTTPException(CustomHTTPException):
    status_code = 409
    detail = "Удобство с таким названием уже существует"