from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from task_api.main import create_app


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "tasks.sqlite3"


@pytest.fixture
def client_factory() -> Callable[[Path], TestClient]:
    clients: list[TestClient] = []

    def factory(path: Path) -> TestClient:
        client = TestClient(create_app(path))
        clients.append(client)
        return client

    yield factory

    for client in clients:
        client.close()


@pytest.fixture
def client(db_path: Path, client_factory: Callable[[Path], TestClient]) -> TestClient:
    return client_factory(db_path)
