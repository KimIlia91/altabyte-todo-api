from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.todo.models import Todo
from sqlalchemy import select

from .exceptions import TodoNotFound
from .schemas import TodoResponse, TodoCreateRequest, TodoUpdateRequest


class TodoService:
    """Сервис для работы с Todo"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, owner_id: str) -> List[TodoResponse]:
        """Получить все todos"""
        stmt = select(Todo).filter(Todo.owner_id == owner_id)
        result = await self.db.execute(stmt)
        todos = result.scalars().all()
        return todos

    async def get_by_id(self, id: int, owner_id: str) -> TodoResponse:
        """Получить todo по id"""
        stmt = select(Todo).filter(Todo.id == id, Todo.owner_id == owner_id)
        result = await self.db.execute(stmt)
        todo = result.scalar_one_or_none()
        if todo is None:
            raise TodoNotFound(f"Todo with id {id} not found")
        return todo

    async def create(self, request: TodoCreateRequest, owner_id: str) -> TodoResponse:
        """Создать todo"""
        todo = Todo(**request.model_dump(), owner_id=owner_id)
        async with self.db.begin():
            self.db.add(todo)
            await self.db.flush()
            await self.db.refresh(todo)
        return todo

    async def update(
        self, id: int, request: TodoUpdateRequest, owner_id: str
    ) -> TodoResponse:
        """Обновить todo"""
        async with self.db.begin():
            todo = await self.get_by_id(id, owner_id)
            update_data = request.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:
                    setattr(todo, field, value)
            await self.db.flush()
            await self.db.refresh(todo)
        return todo

    async def delete(self, id: int, owner_id: str) -> None:
        """Удалить todo"""
        async with self.db.begin():
            todo = await self.get_by_id(id, owner_id)
            await self.db.delete(todo)
