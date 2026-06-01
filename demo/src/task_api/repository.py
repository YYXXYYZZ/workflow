from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .database import connect, row_to_task
from .errors import TaskApiError, persistence_error, task_not_found
from .models import CreateTaskRequest, Status


class TaskRepository:
    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        try:
            return connect(self.db_path)
        except (OSError, sqlite3.Error) as exc:
            raise persistence_error() from exc

    def create_task(self, request: CreateTaskRequest) -> dict:
        task_id = str(uuid4())
        now = utc_now()
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO tasks (
                        id, title, description, status, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        task_id,
                        request.title,
                        request.description,
                        request.status.value,
                        now,
                        now,
                    ),
                )
            return {
                "id": task_id,
                "title": request.title,
                "description": request.description,
                "status": request.status.value,
                "created_at": now,
                "updated_at": now,
            }
        except TaskApiError:
            raise
        except (OSError, sqlite3.Error) as exc:
            raise persistence_error() from exc

    def list_tasks(self) -> list[dict]:
        try:
            with self._connect() as connection:
                rows = connection.execute(
                    """
                    SELECT id, title, description, status, created_at, updated_at
                    FROM tasks
                    ORDER BY created_at ASC
                    """
                ).fetchall()
            return [row_to_task(row) for row in rows]
        except TaskApiError:
            raise
        except (OSError, sqlite3.Error) as exc:
            raise persistence_error() from exc

    def update_task_status(self, task_id: str, status: Status) -> dict:
        now = utc_now()
        try:
            with self._connect() as connection:
                result = connection.execute(
                    """
                    UPDATE tasks
                    SET status = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (status.value, now, task_id),
                )
                if result.rowcount == 0:
                    raise task_not_found()
                row = connection.execute(
                    """
                    SELECT id, title, description, status, created_at, updated_at
                    FROM tasks
                    WHERE id = ?
                    """,
                    (task_id,),
                ).fetchone()
            if row is None:
                raise task_not_found()
            return row_to_task(row)
        except TaskApiError:
            raise
        except (OSError, sqlite3.Error) as exc:
            raise persistence_error() from exc

    def delete_task(self, task_id: str) -> None:
        try:
            with self._connect() as connection:
                result = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                if result.rowcount == 0:
                    raise task_not_found()
        except TaskApiError:
            raise
        except (OSError, sqlite3.Error) as exc:
            raise persistence_error() from exc


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
