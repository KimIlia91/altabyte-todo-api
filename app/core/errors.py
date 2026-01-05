class AppError(Exception):
    """Базовая ошибка приложения"""
    type: str
    title: str
    status: int

    def __init__(self, detail: str):
        self.detail = detail


class NotFound(AppError):
    """Ошибка не найденного ресурса"""
    type = "not_found"
    status = 404

    def __init__(self, title: str, detail: str):
        self.title = title
        self.detail = detail
