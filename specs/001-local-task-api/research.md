# Research: Local Task Management API

**Feature**: Local Task Management API
**Date**: 2026-05-25
**Scope**: Phase 0 decisions for a minimal FastAPI + SQLite + pytest + uv PoC under `demo/`.

## Decision: Use FastAPI with Pydantic schemas

**Rationale**: The feature exposes a small REST-style HTTP JSON API. FastAPI gives a concise route layer, generated OpenAPI, and Pydantic request/response validation with little custom code.

**Alternatives considered**:

- Flask: smaller core, but request validation and OpenAPI would require more manual code or extra dependencies.
- Plain ASGI/Starlette: lower level than needed for this PoC.
- CLI/function-only API: rejected by clarified REST-style HTTP JSON contract.

## Decision: Use SQLite via Python standard library `sqlite3`

**Rationale**: The user requested SQLite local persistence. The standard library is enough for one table, simple CRUD, and local tests. Avoiding an ORM keeps the implementation small and reviewable.

**Alternatives considered**:

- SQLAlchemy: useful for larger applications, but adds an abstraction layer not needed for a single-table PoC.
- JSON file persistence: simpler storage, but the user explicitly requested SQLite for this plan.
- In-memory storage: rejected because persistence after local API restart is required.

## Decision: Keep the database schema to one `tasks` table

**Rationale**: The domain has one entity. A single table with a `status` check constraint and server-maintained timestamps directly matches the spec while keeping the data model easy to inspect.

**Alternatives considered**:

- Separate status history table: unnecessary because the feature only requires current status.
- Soft-delete flag: unnecessary for this PoC; hard delete satisfies "not visible and cannot be updated" with less code.

## Decision: Return a unified error object for all failure paths

**Rationale**: The spec requires `{ "error": { "code": "...", "message": "..." } }`. A small API error helper and custom validation exception handler can normalize validation, not-found, illegal status, and persistence errors.

**Alternatives considered**:

- FastAPI default validation response: rejected because it does not match the required unified error object.
- RFC 7807 problem details: considered in clarification, not selected.

## Decision: Use pytest with FastAPI TestClient and temporary SQLite files

**Rationale**: TestClient allows direct HTTP-level testing without starting a live server. Temporary SQLite files allow persistence behavior and failure paths to be tested without polluting `demo/data/`.

**Alternatives considered**:

- Live server tests only: slower and more brittle for a small PoC.
- Manual verification only: rejected by constitution and current user request for tests.
- In-memory SQLite tests only: insufficient for restart/persistence checks.

## Decision: Use uv with `demo/pyproject.toml`

**Rationale**: The user requested uv. Keeping `pyproject.toml`, `uv.lock`, scripts, and all runnable assets under `demo/` respects the repository boundary.

**Alternatives considered**:

- Root-level Python project files: rejected because runnable PoC assets must stay under `demo/`.
- pip/requirements.txt: not selected because uv is requested and gives repeatable local commands.

## Decision: Timestamp format is ISO 8601 UTC

**Rationale**: OpenAPI can represent timestamps with `format: date-time`, and ISO 8601 UTC strings are easy to compare in JSON responses and SQLite text columns.

**Alternatives considered**:

- Unix epoch integers: compact but less human-readable in contract examples.
- Local timezone strings: ambiguous across machines.

## Decision: List responses are ordered by creation time ascending

**Rationale**: The spec did not require custom ordering. Creation-time ascending is deterministic, simple, and makes examples predictable.

**Alternatives considered**:

- Unspecified DB order: risks flaky tests and unclear user expectations.
- Updated-time ordering: less intuitive for a basic task list.
