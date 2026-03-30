from fastapi import FastAPI

from src.middlewares.custom_middleware import check_middleware


def register_middleware(app_: FastAPI):
    app_.middleware("http")(check_middleware)
