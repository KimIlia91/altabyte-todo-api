from fastapi import FastAPI
from .core.handlers import ExceptionHandlers
from .core.openapi import CustomOpenAPI
from .features.todo.controller import TodoController
from .core.settings import settings


app = FastAPI(
    swagger_ui_init_oauth={
        "clientId": settings.OAUTH_CLIENT_ID,
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": "openid profile email",
    }
)

CustomOpenAPI.register(app)
ExceptionHandlers.register(app)
app.include_router(TodoController.router)
