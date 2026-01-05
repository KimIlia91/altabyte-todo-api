from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""

    APP_NAME: str = "Todo List API"
    DEBUG: bool = False
    TODO_DB_URL: str = "postgresql://postgres:EjaycfIOrLDfwFiLEDmKYflCiBeshguh@postgres.railway.internal:5432/railway"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
