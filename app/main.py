from fastapi import FastAPI
from .core.handlers import ExceptionHandlers
from .core.openapi import CustomOpenAPI
from .features.todo.controller import TodoController


app = FastAPI()

CustomOpenAPI.register(app)
ExceptionHandlers.register(app)
app.include_router(TodoController.router)
