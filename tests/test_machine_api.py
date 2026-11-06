import pytest
pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient
from usm.web import app

def test_machine_catalog():
    response = TestClient(app).get("/api/machines")
    assert response.status_code == 200
    assert response.json()[0]["id"] == "usm-6502"

def test_machine_demo():
    pytest.importorskip("py65")
    response = TestClient(app).post("/api/machines/usm-6502/run")
    assert response.status_code == 200, response.text
    assert response.json()["result"]["uart_text"] == "USM-6502 OK"

def test_machine_ui_panel():
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert "6502-ROM starten" in response.text
