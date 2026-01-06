from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.features.todo.service import TodoService
from app.core.databases import get_todo_db
from app.core.auth.security import get_current_user
from app.core.schemas import CurrentUser as CurrentUserModel

CurrentUserDep = Annotated[CurrentUserModel, Depends(get_current_user)]


def get_todo_service(db: Annotated[AsyncSession, Depends(get_todo_db)]) -> TodoService:
    """Dependency для получения сервиса Todo"""

    return TodoService(db)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]