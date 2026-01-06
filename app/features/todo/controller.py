from typing import List
from fastapi import APIRouter, status
from app.core.schemas import ProblemDetails
from .dependencies import TodoServiceDep
from .schemas import TodoResponse, TodoCreateRequest, TodoUpdateRequest
from .dependencies import CurrentUserDep


class TodoController:
    """Контроллер для работы с задачами"""

    router = APIRouter(prefix="/todos", tags=["Todos"])

    @router.get("", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
    async def get_all_todos(
        todo_service: TodoServiceDep,
        current_user: CurrentUserDep,
    ):
        """Получает все задачи"""

        return await todo_service.get_all(current_user.sub)

    @router.get(
        "/{todo_id}",
        response_model=TodoResponse,
        status_code=status.HTTP_200_OK,
        responses={404: {"model": ProblemDetails}},
    )
    async def get_todo_by_id(
        todo_id: int,
        todo_service: TodoServiceDep,
        current_user: CurrentUserDep,
    ):
        """Получает задачу по ID"""
        
        return await todo_service.get_by_id(todo_id, current_user.sub)

    @router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
    async def create_todo(
        request: TodoCreateRequest,
        todo_service: TodoServiceDep,
        current_user: CurrentUserDep,
    ):
        """Создает задачу"""

        return await todo_service.create(request, current_user.sub)

    @router.put(
        "/{todo_id}",
        response_model=TodoResponse,
        status_code=status.HTTP_200_OK,
        responses={404: {"model": ProblemDetails}},
    )
    async def update_todo(
        todo_id: int,
        request: TodoUpdateRequest,
        todo_service: TodoServiceDep,
        current_user: CurrentUserDep,
    ):
        """Обновляет задачу"""

        return await todo_service.update(todo_id, request, current_user.sub)

    @router.delete(
        "/{todo_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={404: {"model": ProblemDetails}},
    )
    async def delete_todo_by_id(
        todo_id: int,
        todo_service: TodoServiceDep,
        current_user: CurrentUserDep,
    ):
        """Удаляет задачу по ID"""

        await todo_service.delete(todo_id, current_user.sub)
