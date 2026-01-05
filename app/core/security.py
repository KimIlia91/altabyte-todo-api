from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2AuthorizationCodeBearer,
)
import httpx
from jose import jwt
from typing import Optional
from functools import lru_cache

from app.core.schemas import CurrentUser
from app.core.errors import Unauthorized
from app.core.settings import settings

# security = HTTPBearer(auto_error=False)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTHORIZE_URL,
    tokenUrl=settings.TOKEN_URL,
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
        print(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        print(key)
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience="todo-api",
            issuer=settings.ISSUER,
        )
    except Exception as e:
        print("Invalid or expired token", e)
        raise Unauthorized("Invalid or expired token")


# def get_current_user(
#     credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
# ) -> CurrentUser:
#     if not credentials:
#         raise Unauthorized("Missing authentication token")

#     payload = verify_token(credentials.credentials)
#     return CurrentUser(**payload)


def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    try:
        payload = verify_token(token)
        return CurrentUser(**payload)
    except Exception as e:
        print("Invalid or expired token", e)
        raise Unauthorized("Invalid or expired token")
