from fastapi import HTTPException


class CustomException(Exception):
    detail: str = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(CustomException):
    detail = "Объект с такими параметрами не найден"


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


class CustomHTTPException(HTTPException):
    status_code = 500
    detail: str | None = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Отель с таким id не найден"


class HotelOrRoomNotFoundHTTPException(CustomHTTPException):
    status_code = 404
    detail = "Отель с указанным id или номер с указанным id в этом отеле не найден"
