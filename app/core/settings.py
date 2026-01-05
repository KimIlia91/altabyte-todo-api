from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Todo List API"
    DEBUG: bool = False

    TODO_DB_URL: str = "postgresql://postgres:EjaycfIOrLDfwFiLEDmKYflCiBeshguh@postgres.railway.internal:5432/railway"

    AUTH_URL: str = "https://server-production-5c965.up.railway.app"

    ISSUER: str = f"{AUTH_URL}/application/o/todo-api/"
    JWKS_URL: str = f"{ISSUER}jwks/"

    AUTHORIZE_URL: str = f"{AUTH_URL}/application/o/authorize/"
    TOKEN_URL: str = f"{AUTH_URL}/application/o/token/"

    OAUTH_CLIENT_ID: str = "TN7twonQvj8KHNnfQkfqnrN7kxnuRGFUgGnFcuH9"

    # class Config:
    #     env_file = ".env"
    #     case_sensitive = True
    #     env_file_encoding = "utf-8"
    #     extra = "ignore"


settings = Settings()
