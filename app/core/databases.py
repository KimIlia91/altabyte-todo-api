from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.settings import settings


todo_db_engine = create_async_engine(
    settings.TODO_DB_URL.replace("postgresql://", "postgresql+asyncpg://"),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
)

AsyncSessionTodoDbLocal = async_sessionmaker(
    bind=todo_db_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_todo_db() -> AsyncSession:
    """Dependency для получения сессии Todo БД"""

    async with AsyncSessionTodoDbLocal() as db:
        try:
            yield db
        finally:
            await db.close()
