from fastapi import FastAPI

from .core.handlers import ExceptionHandlers
from .core.openapi import CustomOpenAPI
from .features.todo.controller import TodoController
from .core.auth.security import configure_swagger_ui_oauth
from .core.lifespan import app_lifespan

app = FastAPI(lifespan=app_lifespan)

configure_swagger_ui_oauth(app)
CustomOpenAPI.register(app)
ExceptionHandlers.register(app)
app.include_router(TodoController.router)
