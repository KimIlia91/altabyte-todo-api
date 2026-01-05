from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Todo List API"
    DEBUG: bool = False

    TODO_DB_URL: str

    AUTH_URL: str = "https://server-production-5c965.up.railway.app"
    ISSUER: str = f"{AUTH_URL}/application/o/todo-api/"
    JWKS_URL: str = f"{ISSUER}jwks/"
    AUTHORIZE_URL: str = f"{AUTH_URL}/application/o/authorize/"
    TOKEN_URL: str = f"{AUTH_URL}/application/o/token/"
    OAUTH_CLIENT_ID: str = "6VYHNJ8Cux0yz723FwNSIKd5WYgOAmkWz9mmZHhp"
    AUTH_ALGORITHMS: list[str] = ["RS256"]

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
