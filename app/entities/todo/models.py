from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    func,
    TEXT,
    Index,
)
from app.entities.base import Base
from .enums import TodoPriority


class Todo(Base):
    """Модель задачи"""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    priority = Column(
        Enum(TodoPriority),
        nullable=False,
        default=TodoPriority.MEDIUM,
    )
    owner_id = Column(String(255), nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (Index("ix_todos_owner_id", "owner_id"),)
