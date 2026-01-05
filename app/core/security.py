from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from jose import jwt
from typing import Optional
from functools import lru_cache

from app.core.schemas import CurrentUser
from app.core.errors import Unauthorized
from app.core.settings import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTHORIZE_URL,
    tokenUrl=settings.TOKEN_URL,
    auto_error=False,
    scopes={
        "openid": "OpenID",
        "profile": "Profile",
        "email": "Email",
    },
)


@lru_cache
def get_jwks():
    return httpx.get(settings.JWKS_URL).json()


def verify_token(token: str):
    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.OAUTH_CLIENT_ID,
            issuer=settings.ISSUER,
        )
    except Exception:
        raise Unauthorized("Invalid or expired token")


def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> CurrentUser:
    if not token:
        raise Unauthorized("Missing authentication token")
    payload = verify_token(token)
    return CurrentUser(**payload)
