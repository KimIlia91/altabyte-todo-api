from typing import List
from fastapi import APIRouter, status
from app.core.schemas import ProblemDetails
from .dependencies import TodoServiceDep
from .schemas import TodoResponse, TodoCreateRequest, TodoUpdateRequest


class TodoController:
    """Контроллер для работы с задачами"""

    router = APIRouter(prefix="/todos", tags=["Todos"])

    @router.get("", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
    def get_all_todos(todo_service: TodoServiceDep):
        """Получает все задачи"""

        return todo_service.get_all()

    @router.get(
        "/{todo_id}",
        response_model=TodoResponse,
        status_code=status.HTTP_200_OK,
        responses={404: {"model": ProblemDetails}},
    )
    def get_todo_by_id(todo_id: int, todo_service: TodoServiceDep):
        """Получает задачу по ID"""

        return todo_service.get_by_id(todo_id)

    @router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
    def create_todo(request: TodoCreateRequest, todo_service: TodoServiceDep):
        """Создает задачу"""

        return todo_service.create(request)

    @router.put(
        "/{todo_id}",
        response_model=TodoResponse,
        status_code=status.HTTP_200_OK,
        responses={404: {"model": ProblemDetails}},
    )
    def update_todo(
        todo_id: int, request: TodoUpdateRequest, todo_service: TodoServiceDep
    ):
        """Обновляет задачу"""

        return todo_service.update(todo_id, request)

    @router.delete(
        "/{todo_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={404: {"model": ProblemDetails}},
    )
    def delete_todo_by_id(todo_id: int, todo_service: TodoServiceDep):
        """Удаляет задачу по ID"""

        todo_service.delete(todo_id)
