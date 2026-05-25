# Data Model: Local Task Management API

**Feature**: Local Task Management API
**Date**: 2026-05-25

## Entity: Task

Represents one locally managed task.

| Field | Type | Required | Source | Validation / Rule |
|---|---|---:|---|---|
| `id` | string | yes | system | Stable UUID string; user input for this field is rejected |
| `title` | string | yes | user | Trim before write; length after trim must be 1-100 characters |
| `description` | string | yes | user | Trim before write; default empty string; max 1000 characters |
| `status` | string enum | yes | user/system | Allowed values: `todo`, `doing`, `done`; default `todo` on create |
| `created_at` | string date-time | yes | system | ISO 8601 UTC string set on create; user input rejected |
| `updated_at` | string date-time | yes | system | ISO 8601 UTC string set on create and status update; user input rejected |

## SQLite Table

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL CHECK (status IN ('todo', 'doing', 'done')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

## State Rules

- New tasks default to `todo` unless `status` is explicitly `todo`, `doing`, or `done`.
- Status can move from any allowed value to any allowed value.
- Status update changes `updated_at` and never changes `created_at`.
- Delete is a hard delete. Deleted tasks are absent from list responses and later update/delete attempts return not found.

## Validation Rules

- Unknown request fields are rejected.
- System-maintained fields (`id`, `created_at`, `updated_at`) are rejected in user requests.
- Invalid `status` values are rejected before storage.
- Validation failures return unified error object with `error.code = "validation_error"`.
- Missing or deleted task returns unified error object with `error.code = "task_not_found"`.
- SQLite read/write failures return unified error object with `error.code = "persistence_error"`.

## Query Rules

- `GET /tasks` returns all tasks ordered by `created_at` ascending.
- Empty storage returns an empty list.
- Default SQLite path is `demo/data/tasks.sqlite3`; tests use temporary database files.
