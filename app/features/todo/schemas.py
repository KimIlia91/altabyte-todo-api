from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.entities.todo.enums import TodoPriority


class TodoResponse(BaseModel):
    """Схема ответа для Todo"""

    id: int
    title: str
    description: str | None
    completed: bool
    priority: TodoPriority
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class TodoCreateRequest(BaseModel):
    """Схема запроса для создания задачи"""

    title: str = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM)


class TodoUpdateRequest(BaseModel):
    """Схема запроса для обновления задачи"""

    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    priority: TodoPriority | None = Field(default=None)
    completed: bool | None = Field(default=None)
