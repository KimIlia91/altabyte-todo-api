from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .errors import AppError


class ExceptionHandlers:
    """Обработчики исключений"""

    media_type = "application/json"

    @classmethod
    def register(cls, app: FastAPI):
        """Регистрирует обработчики исключений"""

        @app.exception_handler(AppError)
        async def app_error(req: Request, exc: AppError):
            """Обработчик ошибок приложения"""
            return JSONResponse(
                status_code=exc.status,
                media_type=cls.media_type,
                content={
                    "type": exc.type,
                    "title": exc.title,
                    "status": exc.status,
                    "detail": exc.detail,
                    "instance": str(req.url),
                },
            )

        @app.exception_handler(RequestValidationError)
        async def validation(req: Request, exc: RequestValidationError):
            """Обработчик ошибок валидации"""
            errors = [
                {"field": e["loc"][-1], "message": e["msg"]} for e in exc.errors()
            ]
            return JSONResponse(
                status_code=422,
                media_type=cls.media_type,
                content={
                    "type": "validation_error",
                    "title": "Validation error",
                    "status": 422,
                    "detail": "Invalid request data",
                    "instance": str(req.url),
                    "errors": errors,
                },
            )

        @app.exception_handler(Exception)
        async def fatal(req: Request, exc: Exception):
            """Обработчик непредвиденных ошибок"""
            return JSONResponse(
                status_code=500,
                media_type=cls.media_type,
                content={
                    "type": "internal_server_error",
                    "title": "Internal Server Error",
                    "status": 500,
                    "detail": "Unexpected error",
                    "instance": str(req.url),
                },
            )
