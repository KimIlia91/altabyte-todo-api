from app.core.errors import NotFound


class TodoNotFound(NotFound):
    """Задача не найдена"""

    def __init__(self, detail: str):
        super().__init__(title="Todo not found", detail=detail)
