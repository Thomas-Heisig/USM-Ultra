import pytest
pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient
from usm.web import app

client = TestClient(app)

def test_component_catalog_api():
    response = client.get("/api/components")
    assert response.status_code == 200
    assert any(item["id"] == "m68000" for item in response.json())

def test_component_filter_api():
    response = client.get("/api/components?family=CPU")
    assert response.status_code == 200
    assert all(item["family"] == "CPU" for item in response.json())

def test_component_detail_api():
    response = client.get("/api/components/paula")
    assert response.status_code == 200
    assert "agnus" in response.json()["dependencies"]

def test_component_unknown_api():
    assert client.get("/api/components/unknown-chip").status_code == 404

def test_summary_api():
    response = client.get("/api/components/summary")
    assert response.status_code == 200
    assert response.json()["total"] > 20

def test_frontend_has_inventory():
    response = client.get("/")
    assert response.status_code == 200
    assert "Chip- und Komponenten-Katalog" in response.text
    assert "/api/components" in response.text
