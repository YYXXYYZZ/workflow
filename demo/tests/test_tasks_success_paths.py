from __future__ import annotations

from datetime import datetime
from pathlib import Path
from time import sleep
from uuid import UUID

from fastapi.testclient import TestClient


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def create_task(
    client: TestClient,
    title: str = "Write plan",
    description: str = "Finish Spec Kit plan",
    status: str | None = None,
) -> dict:
    payload = {"title": title, "description": description}
    if status is not None:
        payload["status"] = status

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201, response.text
    return response.json()


def assert_task_shape(task: dict) -> None:
    UUID(task["id"])
    assert isinstance(task["title"], str)
    assert isinstance(task["description"], str)
    assert task["status"] in {"todo", "doing", "done"}
    assert parse_timestamp(task["created_at"])
    assert parse_timestamp(task["updated_at"])


def test_create_task_defaults_status_and_returns_complete_task(client: TestClient) -> None:
    task = create_task(client, status=None)

    assert_task_shape(task)
    assert task["title"] == "Write plan"
    assert task["description"] == "Finish Spec Kit plan"
    assert task["status"] == "todo"


def test_create_task_accepts_explicit_status_and_trims_fields(client: TestClient) -> None:
    task = create_task(
        client,
        title="  Review API  ",
        description="  Check contract  ",
        status="doing",
    )

    assert task["title"] == "Review API"
    assert task["description"] == "Check contract"
    assert task["status"] == "doing"


def test_list_tasks_returns_empty_list_before_any_task(client: TestClient) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_complete_tasks_ordered_by_creation_time(
    client: TestClient,
) -> None:
    first = create_task(client, title="First", description="one")
    sleep(0.001)
    second = create_task(client, title="Second", description="two", status="done")

    response = client.get("/tasks")

    assert response.status_code == 200
    tasks = response.json()
    assert [task["id"] for task in tasks] == [first["id"], second["id"]]
    assert [task["title"] for task in tasks] == ["First", "Second"]
    for task in tasks:
        assert_task_shape(task)


def test_tasks_remain_visible_after_database_reinitialization(
    db_path: Path,
    client_factory,
) -> None:
    first_client = client_factory(db_path)
    created = create_task(first_client, title="Persist me", description="")

    second_client = client_factory(db_path)
    response = second_client.get("/tasks")

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [created["id"]]


def test_update_status_changes_updated_at_and_preserves_created_at(
    client: TestClient,
) -> None:
    created = create_task(client, status="todo")
    sleep(0.001)

    response = client.patch(
        f"/tasks/{created['id']}/status",
        json={"status": "doing"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == created["id"]
    assert updated["status"] == "doing"
    assert updated["created_at"] == created["created_at"]
    assert parse_timestamp(updated["updated_at"]) > parse_timestamp(
        created["updated_at"]
    )


def test_delete_task_removes_it_from_later_list_results(client: TestClient) -> None:
    created = create_task(client)

    delete_response = client.delete(f"/tasks/{created['id']}")
    list_response = client.get("/tasks")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_generated_openapi_contains_contract_endpoints(client: TestClient) -> None:
    generated_paths = client.app.openapi()["paths"]
    contract_text = (
        Path(__file__).resolve().parents[1] / "contracts" / "openapi.yaml"
    ).read_text()

    expected = {
        "/tasks": {"post", "get"},
        "/tasks/{task_id}/status": {"patch"},
        "/tasks/{task_id}": {"delete"},
    }
    for path, methods in expected.items():
        assert path in generated_paths
        assert methods.issubset(generated_paths[path])
        assert path in contract_text
