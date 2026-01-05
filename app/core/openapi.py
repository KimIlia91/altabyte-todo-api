from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.core.schemas import ValidationErrorProblemDetails, ProblemDetails


class CustomOpenAPI:
    """Класс для регистрации OpenAPI схемы в приложении"""

    @staticmethod
    def register(app: FastAPI) -> None:
        """Регистрирует кастомную OpenAPI схему в приложении"""

        def custom_openapi():
            """Генерирует кастомную OpenAPI схему"""
            if app.openapi_schema:
                return app.openapi_schema

            schema = get_openapi(
                title=app.title,
                version=app.version,
                description=app.description,
                routes=app.routes,
            )

            components = schema.setdefault("components", {})
            schemas = components.setdefault("schemas", {})

            def flatten(name: str, model):
                """Флаттенит модель в схему"""
                js = model.model_json_schema(
                    ref_template="#/components/schemas/{model}"
                )
                schemas[name] = js

                for k in list(js.get("$defs", {})):
                    schemas[k] = js["$defs"][k]
                js.pop("$defs", None)

            flatten("ValidationErrorProblemDetails", ValidationErrorProblemDetails)
            flatten("ProblemDetails", ProblemDetails)

            schemas.pop("HTTPValidationError", None)
            schemas.pop("ValidationError", None)

            for path in schema["paths"].values():
                for method in path.values():
                    if isinstance(method, dict) and "422" in method.get(
                        "responses", {}
                    ):
                        method["responses"]["422"]["content"] = {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ValidationErrorProblemDetails"
                                }
                            }
                        }

            for path in schema["paths"].values():
                for method in path.values():
                    if isinstance(method, dict):
                        responses = method.get("responses", {})
                        responses["500"] = {
                            "description": "Internal Server Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ProblemDetails"
                                    }
                                },
                            },
                        }

                        if method.get("security"):
                            responses["401"] = {
                                "description": "Unauthorized",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ProblemDetails"
                                        }
                                    },
                                },
                            }
                            responses["403"] = {
                                "description": "Forbidden",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ProblemDetails"
                                        }
                                    },
                                },
                            }

            app.openapi_schema = schema
            return app.openapi_schema

        app.openapi = custom_openapi
