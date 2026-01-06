import httpx
from typing import Optional
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.settings import settings


class AuthClient:
    """Singleton HTTP клиент для работы с Auth API"""

    _instance: Optional[httpx.AsyncClient] = None

    @classmethod
    async def initialize(cls) -> None:
        """Инициализировать клиент"""
        if cls._instance is None:
            cls._instance = httpx.AsyncClient(timeout=10.0)

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        """Получить singleton HTTP клиент"""
        if cls._instance is None:
            await cls.initialize()
        return cls._instance

    @classmethod
    async def get_jwks(cls) -> dict:
        """Получить JWKS для верификации токенов"""
        client = await cls.get_client()
        response = await client.get(settings.JWKS_URL)
        response.raise_for_status()
        return response.json()

    @classmethod
    async def close(cls) -> None:
        """Закрыть клиент"""
        if cls._instance is not None:
            try:
                await cls._instance.aclose()
            except Exception:
                pass
            finally:
                cls._instance = None

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, app: FastAPI):
        """Lifespan для управления жизненным циклом клиента"""
        await cls.initialize()
        try:
            yield
        finally:
            await cls.close()
