# Quickstart: Local Task Management API

**Feature**: Local Task Management API
**Date**: 2026-05-25

This quickstart describes the intended local workflow after implementation. All commands run from the repository root unless noted.

## Install Dependencies

```bash
cd demo
uv sync
```

## Run API Locally

```bash
cd demo
uv run uvicorn src.task_api.main:app --reload --host 127.0.0.1 --port 8000
```

Default SQLite path:

```text
demo/data/tasks.sqlite3
```

## Exercise Core Flow

Create a task:

```bash
curl -sS -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Write plan","description":"Finish Spec Kit plan","status":"todo"}'
```

List tasks:

```bash
curl -sS http://127.0.0.1:8000/tasks
```

Update status:

```bash
curl -sS -X PATCH http://127.0.0.1:8000/tasks/{task_id}/status \
  -H 'Content-Type: application/json' \
  -d '{"status":"doing"}'
```

Delete task:

```bash
curl -sS -X DELETE http://127.0.0.1:8000/tasks/{task_id}
```

## Run Tests

```bash
cd demo
uv run pytest
```

Expected test coverage:

- Success paths: create, list, update status, delete.
- Failure paths: invalid or blank title, overlong fields, invalid status, unknown fields, system-maintained fields, missing task, deleted task, unified error object.
- Persistence: local SQLite data remains readable after app/database reinitialization, and storage failures return the unified persistence error shape.

## Contract

Design contract:

```text
specs/001-local-task-api/contracts/openapi.yaml
```

If implementation needs a runnable PoC copy, keep it under:

```text
demo/contracts/openapi.yaml
```
