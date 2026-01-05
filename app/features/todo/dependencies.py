from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from app.features.todo.service import TodoService
from app.core.databases import get_todo_db


def get_todo_service(db: Annotated[Session, Depends(get_todo_db)]) -> TodoService:
    """Dependency для получения сервиса Todo"""

    return TodoService(db)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]
