# Tasks: Local Task Management API

**Input**: Design documents from `specs/001-local-task-api/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Language**: 正文描述使用中文；SDD、PoC、Spec Kit、API、contract、test、CI、PR
等特定名词保留惯用 English 用法。

**Tests**: Automated test evidence is REQUIRED by the constitution and by the current spec. Include success-path and failure-path pytest coverage for implemented API behavior.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **PoC implementation**: all runnable source code, tests, fixtures, mocks, contract examples, and local scripts MUST stay under `demo/`
- **Source**: `demo/src/task_api/`
- **Tests**: `demo/tests/`
- **Runtime contracts/examples**: `demo/contracts/`
- **Documentation/design artifacts**: `specs/001-local-task-api/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the Python FastAPI PoC under `demo/`.

- [X] T001 Create project directories `demo/src/task_api/`, `demo/tests/`, `demo/contracts/`, `demo/scripts/`, and `demo/data/`
- [X] T002 Initialize uv project configuration with FastAPI, Uvicorn, pytest, and httpx dependencies in `demo/pyproject.toml`
- [X] T003 Generate uv lockfile for the demo project in `demo/uv.lock`
- [X] T004 Copy the design OpenAPI contract from `specs/001-local-task-api/contracts/openapi.yaml` to `demo/contracts/openapi.yaml`
- [X] T005 [P] Create local run script for uvicorn in `demo/scripts/run.sh`
- [X] T006 [P] Create local pytest script in `demo/scripts/test.sh`
- [X] T007 [P] Add package marker in `demo/src/task_api/__init__.py`
- [X] T008 [P] Add data directory keep file in `demo/data/.gitkeep`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models, database, error handling, and test fixtures required by every user story.

**CRITICAL**: No user story implementation should begin until this phase is complete.

- [X] T009 Define `Status`, task response schema, create request schema, update status request schema, and strict field validation in `demo/src/task_api/models.py`
- [X] T010 Implement unified API error helpers for `validation_error`, `task_not_found`, and `persistence_error` in `demo/src/task_api/errors.py`
- [X] T011 Implement SQLite connection setup, schema creation, row mapping, and configurable DB path support in `demo/src/task_api/database.py`
- [X] T012 Implement repository class skeleton with constructor and shared DB helpers in `demo/src/task_api/repository.py`
- [X] T013 Implement FastAPI app factory, dependency injection for repository, startup DB initialization, and validation exception handler in `demo/src/task_api/main.py`
- [X] T014 Create pytest fixtures for temporary SQLite DB files and FastAPI TestClient in `demo/tests/conftest.py`

**Checkpoint**: Foundation ready - each user story can now add endpoint-specific repository methods, route handlers, and tests.

---

## Phase 3: User Story 1 - 创建任务 (Priority: P1) MVP

**Goal**: Users can create a task through `POST /tasks` with strict validation and receive a complete task response.

**Independent Test**: A caller can create tasks with default or explicit legal status, see trimmed fields in the response, and receive unified validation errors for invalid create input.

### Tests for User Story 1

- [X] T015 [P] [US1] Add success tests for `POST /tasks` default status, explicit status, trimmed fields, and response fields in `demo/tests/test_tasks_success_paths.py`
- [X] T016 [P] [US1] Add failure tests for blank title, overlong title, overlong description, illegal status, unknown fields, and system-maintained fields, asserting exact `validation_error` codes in `demo/tests/test_tasks_failure_paths.py`

### Implementation for User Story 1

- [X] T017 [US1] Implement `create_task` repository method with UUID generation, ISO 8601 UTC timestamps, SQLite insert, and persistence error mapping in `demo/src/task_api/repository.py`
- [X] T018 [US1] Implement `POST /tasks` route returning 201 and unified errors in `demo/src/task_api/main.py`

**Checkpoint**: User Story 1 is independently functional and testable.

---

## Phase 4: User Story 2 - 查看任务列表 (Priority: P1)

**Goal**: Users can view all non-deleted tasks through `GET /tasks`, including empty-list and persisted-data behavior.

**Independent Test**: A caller can list zero tasks, list multiple tasks ordered by `created_at`, and still list created tasks after app/database reinitialization.

### Tests for User Story 2

- [X] T019 [P] [US2] Add success tests for `GET /tasks` empty list, multiple tasks, complete fields, and creation-time ordering in `demo/tests/test_tasks_success_paths.py`
- [X] T020 [US2] Add persistence test proving created tasks remain visible after app/database reinitialization using the same SQLite file in `demo/tests/test_tasks_success_paths.py`
- [X] T021 [P] [US2] Add failure tests for missing/corrupt SQLite initialization and repository persistence read errors returning exact `persistence_error` codes in `demo/tests/test_tasks_failure_paths.py`

### Implementation for User Story 2

- [X] T022 [US2] Implement `list_tasks` repository method ordered by `created_at` ascending with persistence error mapping in `demo/src/task_api/repository.py`
- [X] T023 [US2] Implement `GET /tasks` route returning an array of task responses and unified errors in `demo/src/task_api/main.py`

**Checkpoint**: User Stories 1 and 2 are independently functional and testable.

---

## Phase 5: User Story 3 - 更新任务状态 (Priority: P2)

**Goal**: Users can update an existing task status through `PATCH /tasks/{task_id}/status`.

**Independent Test**: A caller can change status from one legal value to another, observe `updated_at` changing while `created_at` remains stable, and receive unified errors for invalid status or missing tasks.

### Tests for User Story 3

- [X] T024 [P] [US3] Add success tests for `PATCH /tasks/{task_id}/status` legal status updates, stable `created_at`, changed `updated_at`, and response fields in `demo/tests/test_tasks_success_paths.py`
- [X] T025 [P] [US3] Add failure tests for invalid status, nonexistent task ID, PATCH unknown fields, and PATCH system-maintained fields, asserting exact `validation_error` and `task_not_found` codes in `demo/tests/test_tasks_failure_paths.py`

### Implementation for User Story 3

- [X] T026 [US3] Implement `update_task_status` repository method with not-found detection, timestamp update, and persistence error mapping in `demo/src/task_api/repository.py`
- [X] T027 [US3] Implement `PATCH /tasks/{task_id}/status` route returning updated task response and unified errors in `demo/src/task_api/main.py`

**Checkpoint**: User Stories 1, 2, and 3 are independently functional and testable.

---

## Phase 6: User Story 4 - 删除任务 (Priority: P3)

**Goal**: Users can delete an existing task through `DELETE /tasks/{task_id}`.

**Independent Test**: A caller can delete an existing task, observe it disappear from list responses, and receive not-found errors for repeated delete or update after deletion.

### Tests for User Story 4

- [X] T028 [P] [US4] Add success tests for `DELETE /tasks/{task_id}` returning 204 and removing the task from later `GET /tasks` results in `demo/tests/test_tasks_success_paths.py`
- [X] T029 [P] [US4] Add failure tests for deleting a nonexistent task, deleting an already deleted task, and updating a deleted task, asserting exact `task_not_found` codes in `demo/tests/test_tasks_failure_paths.py`

### Implementation for User Story 4

- [X] T030 [US4] Implement `delete_task` repository method with hard delete, affected-row not-found detection, and persistence error mapping in `demo/src/task_api/repository.py`
- [X] T031 [US4] Implement `DELETE /tasks/{task_id}` route returning 204 and unified errors in `demo/src/task_api/main.py`

**Checkpoint**: All user stories are independently functional and testable.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, contract alignment, and small cleanup.

- [X] T032 [P] Ensure FastAPI generated OpenAPI includes `POST /tasks`, `GET /tasks`, `PATCH /tasks/{task_id}/status`, and `DELETE /tasks/{task_id}` matching `demo/contracts/openapi.yaml` in `demo/tests/test_tasks_success_paths.py`
- [X] T033 [P] Add cross-check assertions that all failure-path tests return `{ "error": { "code": "...", "message": "..." } }` with exact expected `error.code` values and non-empty `error.message` in `demo/tests/test_tasks_failure_paths.py`
- [X] T034 Run `uv run pytest` from `demo/` and record the passing command in `specs/001-local-task-api/quickstart.md`
- [X] T035 Validate quickstart commands for install, run, core curl flow, and tests in `specs/001-local-task-api/quickstart.md`
- [X] T036 Confirm all runnable source code, tests, contract examples, scripts, fixtures, mocks, and generated dependency files are under `demo/` and document any exception in `specs/001-local-task-api/tasks.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; begins immediately.
- **Foundational (Phase 2)**: Depends on Phase 1; blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Phase 2; MVP.
- **User Story 2 (Phase 4)**: Depends on Phase 2 and benefits from US1-created test data, but can be implemented with direct fixture data if needed.
- **User Story 3 (Phase 5)**: Depends on Phase 2 and requires an existing task from US1 fixtures/tests.
- **User Story 4 (Phase 6)**: Depends on Phase 2 and requires an existing task from US1 fixtures/tests.
- **Polish (Phase 7)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 创建任务 (P1)**: Foundation only; delivers MVP create capability.
- **US2 查看任务列表 (P1)**: Foundation only; pairs with US1 for practical demo flow.
- **US3 更新任务状态 (P2)**: Foundation plus an existing task fixture.
- **US4 删除任务 (P3)**: Foundation plus an existing task fixture.

### Within Each User Story

- Write tests first and confirm they fail before implementation.
- Implement repository method before route handler.
- Run relevant pytest subset after each story.
- Keep all runtime assets under `demo/`.

## Parallel Opportunities

- Setup tasks T005-T008 can run in parallel after T001.
- User-story test tasks marked [P] can be written in parallel because they touch different scenario blocks or files.
- US2, US3, and US4 can be developed in parallel after Phase 2 if each uses isolated test fixtures.
- Polish checks T032 and T033 can run in parallel after all routes exist.

## Parallel Example: User Story 1

```bash
Task: "T015 [US1] Add success tests for POST /tasks in demo/tests/test_tasks_success_paths.py"
Task: "T016 [US1] Add failure tests for POST /tasks validation in demo/tests/test_tasks_failure_paths.py"
```

## Parallel Example: User Story 2

```bash
Task: "T019 [US2] Add list success tests in demo/tests/test_tasks_success_paths.py"
Task: "T021 [US2] Add list persistence failure test in demo/tests/test_tasks_failure_paths.py"
```

## Parallel Example: User Story 3

```bash
Task: "T024 [US3] Add update status success tests in demo/tests/test_tasks_success_paths.py"
Task: "T025 [US3] Add update status failure tests in demo/tests/test_tasks_failure_paths.py"
```

## Parallel Example: User Story 4

```bash
Task: "T028 [US4] Add delete success tests in demo/tests/test_tasks_success_paths.py"
Task: "T029 [US4] Add delete failure tests in demo/tests/test_tasks_failure_paths.py"
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1 创建任务).
3. Stop and validate `POST /tasks` success and failure tests.
4. Add Phase 4 (US2 查看任务列表) to make the local API demonstrable.

### Incremental Delivery

1. Setup + Foundation -> FastAPI app shell, SQLite schema, unified errors, pytest fixtures.
2. US1 -> create task.
3. US2 -> list tasks and persistence visibility.
4. US3 -> update status.
5. US4 -> delete task.
6. Polish -> contract alignment, quickstart validation, final full test run.

### Validation Commands

```bash
cd demo
uv sync
uv run pytest
```

## Notes

- [P] tasks = different files or independent scenario blocks with no dependency on incomplete tasks.
- [US1] through [US4] labels map directly to user stories in `spec.md`.
- All runnable PoC implementation files must remain under `demo/`.
- `specs/001-local-task-api/contracts/openapi.yaml` is the design contract; `demo/contracts/openapi.yaml` is the runnable PoC copy.
- 2026-05-26 implementation validation: all runnable PoC source code, tests, contract copy, scripts, generated dependency files, and runtime data paths are under `demo/`; no PoC runnable-file exceptions were found. The design contract remains under `specs/001-local-task-api/contracts/openapi.yaml` as a documentation artifact.
