from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.settings import settings


todo_db_engine = create_engine(
    settings.TODO_DB_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionTodoDbLocal = sessionmaker(
    bind=todo_db_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_todo_db() -> Session:
    """Dependency для получения сессии Todo БД"""

    db = SessionTodoDbLocal()
    try:
        yield db
    finally:
        db.close()
