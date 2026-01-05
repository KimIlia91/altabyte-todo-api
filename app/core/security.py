from fastapi import Depends, FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from jose import jwt
from typing import Optional
from functools import lru_cache

from app.core.schemas import CurrentUser
from app.core.errors import Unauthorized
from app.core.settings import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.Auth.AUTHORIZE_URL,
    tokenUrl=settings.Auth.TOKEN_URL,
    auto_error=False,
)


@lru_cache
def get_jwks():
    return httpx.get(settings.Auth.JWKS_URL).json()


def verify_token(token: str):
    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        return jwt.decode(
            token,
            key,
            algorithms=settings.Auth.AUTH_ALGORITHMS,
            audience=settings.Auth.OAUTH_CLIENT_ID,
            issuer=settings.Auth.ISSUER,
        )
    except Exception:
        raise Unauthorized("Invalid or expired token")


def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> CurrentUser:
    if not token:
        raise Unauthorized("Missing authentication token")
    payload = verify_token(token)
    return CurrentUser(**payload)


def configure_swagger_ui_oauth(app: FastAPI) -> None:
    """Настраивает OAuth конфигурацию для Swagger UI"""
    app.swagger_ui_init_oauth = {
        "clientId": settings.Auth.OAUTH_CLIENT_ID,
        "usePkceWithAuthorizationCodeGrant": True,
    }
