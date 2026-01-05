from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Todo List API"
    DEBUG: bool = False

    TODO_DB_URL: str

    AUTH_URL: str
    OAUTH_CLIENT_ID: str
    AUTH_ALGORITHMS: list[str] = ["RS256"]

    @property
    def ISSUER(self) -> str:
        return f"{self.AUTH_URL}/application/o/todo-api/"

    @property
    def JWKS_URL(self) -> str:
        return f"{self.ISSUER}jwks/"

    @property
    def AUTHORIZE_URL(self) -> str:
        return f"{self.AUTH_URL}/application/o/authorize/"

    @property
    def TOKEN_URL(self) -> str:
        return f"{self.AUTH_URL}/application/o/token/"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
