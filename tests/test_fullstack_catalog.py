"""Catalog endpoints and 6502 monitor integration smoke tests."""
import pytest
from fastapi.testclient import TestClient
from usm.web import app

client = TestClient(app)

def test_machine_catalog_filters():
    response = client.get("/api/catalog/machines", params={"cpu": "m68000"})
    assert response.status_code == 200
    names = {m["name"] for m in response.json()}
    assert "Amiga 500" in names
    assert any("Atari" in name for name in names)
    assert all(m["cpu"] == "m68000" for m in response.json())

def test_document_library_filters():
    response = client.get("/api/catalog/documents", params={"system": "6502"})
    assert response.status_code == 200
    assert len(response.json()) >= 5
    assert all(d["system"] == "6502" for d in response.json())

def test_6502_monitor_session_and_reset():
    pytest.importorskip("py65")
    response = client.post("/api/machines/usm-6502/monitor/reset")
    assert response.status_code == 200
    assert response.json()["registers"]["pc"] == 0xE000
    step = client.post("/api/machines/usm-6502/monitor/step", json={"count": 1})
    assert step.status_code == 200
    assert step.json()["registers"]["pc"] == 0xE002
    state = client.get("/api/machines/usm-6502/session")
    assert state.status_code == 200
    assert state.json()["registers"]["pc"] == 0xE002
    paused = client.post("/api/machines/usm-6502/session/pause")
    assert paused.status_code == 200
    assert paused.json()["paused"] is True
    run = client.post("/api/machines/usm-6502/monitor/run", json={"count": 1})
    assert run.status_code == 200
    assert run.json()["steps"] == 1


@pytest.mark.parametrize("route", ["monitor/run", "monitor/step", "step"])
@pytest.mark.parametrize("count", [0, 100001])
def test_6502_step_requests_reject_out_of_range_counts(route, count):
    response = client.post(f"/api/machines/usm-6502/{route}", json={"count": count})
    assert response.status_code == 422
