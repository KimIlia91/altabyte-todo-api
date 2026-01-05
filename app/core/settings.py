from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Настройки приложения"""

    APP_NAME: str = "Todo List API"
    DEBUG: bool = False
    TODO_DB_URL: str

    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
