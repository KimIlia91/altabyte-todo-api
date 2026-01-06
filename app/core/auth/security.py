from fastapi import Depends, FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from typing import Optional

from app.core.schemas import CurrentUser
from app.core.errors import Unauthorized
from app.core.settings import settings
from app.core.auth.client import AuthClient

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTHORIZE_URL,
    tokenUrl=settings.TOKEN_URL,
    auto_error=False,
)


async def verify_token(token: str):
    try:
        jwks = await AuthClient.get_jwks()
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        return jwt.decode(
            token,
            key,
            algorithms=settings.AUTH_ALGORITHMS,
            audience=settings.OAUTH_CLIENT_ID,
            issuer=settings.ISSUER,
        )
    except Exception:
        raise Unauthorized("Invalid or expired token")


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> CurrentUser:
    if not token:
        raise Unauthorized("Missing authentication token")
    payload = await verify_token(token)
    return CurrentUser(**payload)


def configure_swagger_ui_oauth(app: FastAPI) -> None:
    """Настраивает OAuth конфигурацию для Swagger UI"""
    app.swagger_ui_init_oauth = {
        "clientId": settings.OAUTH_CLIENT_ID,
        "usePkceWithAuthorizationCodeGrant": True,
    }
