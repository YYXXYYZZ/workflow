from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .errors import persistence_error


DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "tasks.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL CHECK (status IN ('todo', 'doing', 'done')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


def connect(db_path: Path | str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Path | str) -> None:
    try:
        with connect(db_path) as connection:
            connection.executescript(SCHEMA)
    except (OSError, sqlite3.Error) as exc:
        raise persistence_error() from exc


def row_to_task(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
