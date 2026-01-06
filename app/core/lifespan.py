from contextlib import AsyncExitStack, asynccontextmanager
from fastapi import FastAPI

from app.core.auth.client import AuthClient


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Центральный lifespan приложения.

    Позволяет легко добавлять новые lifecycle-блоки:
    await stack.enter_async_context(OtherResource.lifespan(app))
    """
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(AuthClient.lifespan(app))
        yield
