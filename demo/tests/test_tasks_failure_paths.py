from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from task_api.errors import persistence_error
from task_api.repository import TaskRepository


MISSING_TASK_ID = "00000000-0000-0000-0000-000000000000"


def assert_error(response, status_code: int, code: str) -> None:
    assert response.status_code == status_code, response.text
    body = response.json()
    assert set(body) == {"error"}
    assert body["error"]["code"] == code
    assert isinstance(body["error"]["message"], str)
    assert body["error"]["message"]


def test_create_rejects_blank_title_without_creating_task(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "   ", "description": "x"})

    assert_error(response, 400, "validation_error")
    assert client.get("/tasks").json() == []


def test_create_rejects_overlong_title(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "x" * 101})

    assert_error(response, 400, "validation_error")


def test_create_rejects_overlong_description(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Task", "description": "x" * 1001},
    )

    assert_error(response, 400, "validation_error")


def test_create_rejects_illegal_status(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Task", "status": "blocked"})

    assert_error(response, 400, "validation_error")


def test_create_rejects_unknown_fields(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Task", "priority": "high"})

    assert_error(response, 400, "validation_error")


def test_create_rejects_system_maintained_fields(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "id": MISSING_TASK_ID,
            "title": "Task",
            "created_at": "2026-05-26T00:00:00Z",
            "updated_at": "2026-05-26T00:00:00Z",
        },
    )

    assert_error(response, 400, "validation_error")


def test_missing_sqlite_file_initializes_as_empty_list(
    tmp_path: Path,
    client_factory,
) -> None:
    db_path = tmp_path / "missing.sqlite3"
    client = client_factory(db_path)

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []
    assert db_path.exists()


def test_corrupt_sqlite_file_returns_persistence_error(
    tmp_path: Path,
    client_factory,
) -> None:
    db_path = tmp_path / "tasks.sqlite3"
    db_path.write_text("not sqlite", encoding="utf-8")
    client = client_factory(db_path)

    response = client.get("/tasks")

    assert_error(response, 500, "persistence_error")


def test_repository_read_error_returns_persistence_error(
    client: TestClient,
    monkeypatch,
) -> None:
    def fail_list_tasks(self):
        raise persistence_error()

    monkeypatch.setattr(TaskRepository, "list_tasks", fail_list_tasks, raising=False)

    response = client.get("/tasks")

    assert_error(response, 500, "persistence_error")


def test_update_rejects_invalid_status(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()

    response = client.patch(
        f"/tasks/{created['id']}/status",
        json={"status": "blocked"},
    )

    assert_error(response, 400, "validation_error")


def test_update_nonexistent_task_returns_not_found(client: TestClient) -> None:
    response = client.patch(
        f"/tasks/{MISSING_TASK_ID}/status",
        json={"status": "done"},
    )

    assert_error(response, 404, "task_not_found")


def test_update_rejects_unknown_fields(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()

    response = client.patch(
        f"/tasks/{created['id']}/status",
        json={"status": "doing", "priority": "high"},
    )

    assert_error(response, 400, "validation_error")


def test_update_rejects_system_maintained_fields(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()

    response = client.patch(
        f"/tasks/{created['id']}/status",
        json={"status": "doing", "updated_at": "2026-05-26T00:00:00Z"},
    )

    assert_error(response, 400, "validation_error")


def test_delete_nonexistent_task_returns_not_found(client: TestClient) -> None:
    response = client.delete(f"/tasks/{MISSING_TASK_ID}")

    assert_error(response, 404, "task_not_found")


def test_delete_already_deleted_task_returns_not_found(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()

    first_response = client.delete(f"/tasks/{created['id']}")
    second_response = client.delete(f"/tasks/{created['id']}")

    assert first_response.status_code == 204
    assert_error(second_response, 404, "task_not_found")


def test_update_deleted_task_returns_not_found(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()
    client.delete(f"/tasks/{created['id']}")

    response = client.patch(
        f"/tasks/{created['id']}/status",
        json={"status": "done"},
    )

    assert_error(response, 404, "task_not_found")
