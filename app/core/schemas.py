from typing import TypedDict, List
from pydantic import BaseModel, Field


class ValidationErrorItem(BaseModel):
    """Элемент ошибки валидации для OpenAPI"""

    field: str = Field(..., description="Название поля")
    message: str = Field(..., description="Сообщение об ошибке")


class ValidationErrorProblemDetails(BaseModel):
    """Схема ошибки валидации для OpenAPI"""

    type: str = Field(default="validation_error", description="Тип ошибки")
    title: str = Field(default="Validation error", description="Заголовок ошибки")
    status: int = Field(default=422, description="HTTP статус код")
    detail: str = Field(default="Invalid request data", description="Описание ошибки")
    instance: str = Field(..., description="URI экземпляра ошибки")
    errors: List[ValidationErrorItem] = Field(
        ..., description="Список ошибок валидации"
    )


class ProblemDetails(BaseModel):
    """Схема Problem Details для OpenAPI"""

    type: str = Field(..., description="Тип ошибки")
    title: str = Field(..., description="Заголовок ошибки")
    status: int = Field(..., description="HTTP статус код")
    detail: str = Field(..., description="Описание ошибки")
    instance: str = Field(..., description="URI экземпляра ошибки")
