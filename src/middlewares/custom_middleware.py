import logging
import time
from typing import Callable
from starlette.requests import Request
from starlette.responses import Response

from src.config import settings


async def check_middleware(request: Request, call_next: Callable):
    ip_address = request.client.host
    if ip_address in settings.MIDDLEWARE_HOST_LIST:
        start_time = time.perf_counter()
        response = await call_next(request)
        time_delta = time.perf_counter() - start_time
        logging.info(f"Время выполнения запроса: {round(time_delta, 3)} сек.")
        response.headers["X-Special"] = 'New info'
        return response
    else:
        return Response(status_code=429, content="запрос с неразрешенного  ip")

