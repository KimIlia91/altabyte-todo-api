from typing import List
from sqlalchemy.orm import Session
from app.entities.todo.models import Todo

from .exceptions import TodoNotFound
from .schemas import TodoResponse, TodoCreateRequest, TodoUpdateRequest


class TodoService:
    """Сервис для работы с Todo"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TodoResponse]:
        """Получить все todos"""
        todos = self.db.query(Todo).all()
        return todos

    def get_by_id(self, id: int) -> TodoResponse:
        """Получить todo по id"""
        todo = self.db.query(Todo).filter(Todo.id == id).first()
        if todo is None:
            raise TodoNotFound(f"Todo with id {id} not found")
        return todo

    def create(self, request: TodoCreateRequest) -> TodoResponse:
        """Создать todo"""
        todo = Todo(**request.model_dump())
        with self.db.begin():
            self.db.add(todo)
            self.db.flush()
            self.db.refresh(todo)
        return todo

    def update(self, id: int, request: TodoUpdateRequest) -> TodoResponse:
        """Обновить todo"""
        with self.db.begin():
            todo = self.get_by_id(id)
            for field, value in request.model_dump().items():
                if value is not None:
                    setattr(todo, field, value)
            self.db.flush()
            self.db.refresh(todo)
        return todo

    def delete(self, id: int) -> None:
        """Удалить todo"""
        with self.db.begin():
            todo = self.get_by_id(id)
            self.db.delete(todo)
