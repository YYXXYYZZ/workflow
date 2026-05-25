# Implementation Plan: Local Task Management API

**Branch**: `001-local-task-api` | **Date**: 2026-05-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-local-task-api/spec.md`

**Language**: 正文描述使用中文；SDD、PoC、Spec Kit、API、contract、test、CI、PR
等特定名词保留惯用 English 用法。

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

在 `demo/` 目录内实现一个本地任务管理 REST API。PoC 使用 Python FastAPI 提供
`POST /tasks`、`GET /tasks`、`PATCH /tasks/{id}/status`、`DELETE /tasks/{id}`
四个 JSON endpoint，使用 SQLite 作为本地持久化，使用 pytest 覆盖成功路径和主要
失败路径，并使用 uv 管理 Python 环境和依赖。

## Technical Context

**Language/Version**: Python 3.12（由 uv 管理；不依赖系统 Python 版本）

**Primary Dependencies**: FastAPI、Uvicorn、Pydantic（FastAPI 依赖）、SQLite
标准库 `sqlite3`

**Storage**: SQLite 本地数据库文件，默认位于 `demo/data/tasks.sqlite3`；
test 使用临时 SQLite 文件隔离数据

**Testing**: pytest、FastAPI TestClient、httpx

**Target Platform**: 本地开发环境（macOS/Linux 均可），无需部署

**Project Type**: 本地 web-service PoC

**PoC Location**: `demo/` (all runnable PoC implementation files, tests,
fixtures, contract examples, and local scripts MUST stay under this directory)

**API Contracts**: OpenAPI design contract in
`specs/001-local-task-api/contracts/openapi.yaml`; runnable implementation,
tests, fixtures, and scripts remain under `demo/`

**Performance Goals**: Core API flow can be completed locally in under 2 minutes;
no throughput, concurrency, or production latency target for this PoC

**Constraints**: Implementation remains small and reviewable; no login,
multi-user support, frontend page, notification, or deployment; all runnable
PoC files stay in `demo/`; API returns unified error object; strict input
validation rejects unknown fields and system-maintained fields

**Scale/Scope**: Single local process, one SQLite database file, one Task entity,
four REST endpoints, success-path and failure-path tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Clarification complete: no critical `NEEDS CLARIFICATION` item blocks planning
      or implementation; non-goals and scope boundaries are explicit.
- [x] PoC boundary respected: every runnable implementation file, test, fixture,
      contract example, mock, and local script is planned under `demo/`.
- [x] Simplicity justified: architecture is the smallest clear design that satisfies
      the spec; any extra dependency, abstraction, or layer has a stated reason.
- [x] API contract explicit: every HTTP/CLI/event/file/module boundary has input,
      output, error semantics, and compatibility expectations documented.
- [x] Automated test evidence planned: tests or justified alternative validation map
      to the user stories and include repeatable commands.

**Gate Result**: PASS. No constitution violation is planned. FastAPI and pytest
are user-requested dependencies; SQLite uses the standard library to keep the
implementation smaller than an ORM-backed design.

## Project Structure

### Documentation (this feature)

```text
specs/001-local-task-api/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
demo/
├── pyproject.toml
├── uv.lock
├── data/
│   └── .gitkeep
├── src/
│   └── task_api/
│       ├── __init__.py
│       ├── database.py
│       ├── errors.py
│       ├── main.py
│       ├── models.py
│       └── repository.py
├── tests/
│   ├── conftest.py
│   ├── test_tasks_failure_paths.py
│   └── test_tasks_success_paths.py
├── contracts/
│   └── openapi.yaml
└── scripts/
    ├── run.sh
    └── test.sh
```

**Structure Decision**: Use a single small FastAPI package under
`demo/src/task_api/`. Keep DB access in `database.py`/`repository.py`, Pydantic
schemas in `models.py`, unified error helpers in `errors.py`, and app wiring in
`main.py`. Tests are split only by success and failure paths to avoid premature
test-layer complexity. `demo/contracts/openapi.yaml` is the runnable PoC copy if
contract examples are needed during implementation; the design source remains in
`specs/001-local-task-api/contracts/openapi.yaml`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations.

## Phase 0 Research Summary

See [research.md](./research.md).

Resolved decisions:

- Use FastAPI with Pydantic models for REST JSON and validation.
- Use SQLite through Python standard library `sqlite3`; do not introduce ORM.
- Use unified error helpers and custom validation handlers to preserve the
  required `{ "error": { "code": "...", "message": "..." } }` response.
- Use pytest with FastAPI TestClient and temporary SQLite DB files.
- Use uv from `demo/` for dependency management and repeatable commands.

## Phase 1 Design Summary

See [data-model.md](./data-model.md), [contracts/openapi.yaml](./contracts/openapi.yaml),
and [quickstart.md](./quickstart.md).

Post-design constitution re-check: PASS. Design keeps runnable PoC assets under
`demo/`, has explicit API contract, and maps tests to create/list/update/delete
success paths plus validation/not-found/illegal-status error paths.
