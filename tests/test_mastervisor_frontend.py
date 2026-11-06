"""MasterVisor modular frontend smoke tests."""
import pytest
pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient
from usm.web import app

client = TestClient(app)

@pytest.mark.parametrize("module", [
    "dashboard", "machines", "components", "matrix", "memory",
    "tasks", "trace", "hardware", "recovery", "settings", "docs"
])
def test_module_exists_in_frontend(module):
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="page-' + module + '"' in response.text

def test_task_create_and_list():
    before = client.get("/api/tasks")
    assert before.status_code == 200
    result = client.post("/api/tasks", json={"architecture": "mos6502"})
    assert result.status_code == 200
    task_id = result.json()["id"]
    assert any(t["id"] == task_id for t in client.get("/api/tasks").json())

def test_task_rejects_unknown_architecture():
    assert client.post("/api/tasks", json={"architecture": "made-up"}).status_code == 422

def test_memory_dump():
    response = client.get("/api/memory", params={"address": 0, "count": 16})
    assert response.status_code == 200
    assert len(response.json()["lines"]) == 1

def test_memory_limit():
    assert client.get("/api/memory", params={"address": 0, "count": 300}).status_code == 422

def test_memory_unmapped_returns_markers():
    result = client.get("/api/memory", params={"address": 0xF00000, "count": 2})
    assert result.status_code == 200
    assert result.json()["errors"] == 2
