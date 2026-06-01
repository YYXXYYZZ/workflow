from __future__ import annotations

from fastapi.responses import JSONResponse


VALIDATION_ERROR = "validation_error"
TASK_NOT_FOUND = "task_not_found"
PERSISTENCE_ERROR = "persistence_error"


class TaskApiError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


def validation_error(message: str = "request validation failed") -> TaskApiError:
    return TaskApiError(400, VALIDATION_ERROR, message)


def task_not_found(message: str = "task not found") -> TaskApiError:
    return TaskApiError(404, TASK_NOT_FOUND, message)


def persistence_error(message: str = "task storage is unavailable") -> TaskApiError:
    return TaskApiError(500, PERSISTENCE_ERROR, message)
