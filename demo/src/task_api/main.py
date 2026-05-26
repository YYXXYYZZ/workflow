from __future__ import annotations

from pathlib import Path
from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import Response

from .database import DEFAULT_DB_PATH, initialize_database
from .errors import TaskApiError, error_response
from .models import CreateTaskRequest, ErrorResponse, TaskResponse, UpdateStatusRequest
from .repository import TaskRepository


def create_app(db_path: Path | str | None = None) -> FastAPI:
    app = FastAPI(title="Local Task Management API", version="0.1.0")
    resolved_db_path = Path(db_path) if db_path is not None else DEFAULT_DB_PATH
    app.state.db_path = resolved_db_path
    app.state.startup_error = None

    try:
        initialize_database(resolved_db_path)
    except TaskApiError as exc:
        app.state.startup_error = exc

    @app.exception_handler(TaskApiError)
    async def handle_task_api_error(
        _request: Request, exc: TaskApiError
    ):
        return error_response(exc.status_code, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request, _exc: RequestValidationError
    ):
        return error_response(400, "validation_error", "request validation failed")

    def get_repository() -> TaskRepository:
        if app.state.startup_error is not None:
            raise app.state.startup_error
        return TaskRepository(app.state.db_path)

    error_responses = {
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    }

    @app.post(
        "/tasks",
        response_model=TaskResponse,
        status_code=201,
        responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    )
    async def create_task(
        request: CreateTaskRequest,
        repository: TaskRepository = Depends(get_repository),
    ):
        return repository.create_task(request)

    @app.get(
        "/tasks",
        response_model=list[TaskResponse],
        responses={500: {"model": ErrorResponse}},
    )
    async def list_tasks(repository: TaskRepository = Depends(get_repository)):
        return repository.list_tasks()

    @app.patch(
        "/tasks/{task_id}/status",
        response_model=TaskResponse,
        responses=error_responses,
    )
    async def update_task_status(
        task_id: UUID,
        request: UpdateStatusRequest,
        repository: TaskRepository = Depends(get_repository),
    ):
        return repository.update_task_status(str(task_id), request.status)

    @app.delete(
        "/tasks/{task_id}",
        status_code=204,
        responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    )
    async def delete_task(
        task_id: UUID,
        repository: TaskRepository = Depends(get_repository),
    ):
        repository.delete_task(str(task_id))
        return Response(status_code=204)

    return app


app = create_app()
