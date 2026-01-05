from functools import lru_cache
from typing import Dict, Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import httpx

from app.core.schemas import CurrentUser
from app.core.errors import Unauthorized
from app.core.settings import settings

security = HTTPBearer(auto_error=False)


@lru_cache
def get_jwks():
    return httpx.get(settings.JWKS_URL).json()


def verify_token(token: str) -> Dict:
    try:
        return jwt.decode(
            token,
            get_jwks(),
            algorithms=["RS256"],
            audience="todo-api",
            issuer=settings.ISSUER,
        )
    except Exception:
        raise Unauthorized("Invalid or expired token")


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> CurrentUser:
    """Получает текущего пользователя из JWT токена"""
    if credentials is None:
        raise Unauthorized("Missing authentication token")

    token_data = verify_token(credentials.credentials)
    return CurrentUser(**token_data)
