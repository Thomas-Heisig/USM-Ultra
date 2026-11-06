import pytest
pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient
from usm.web import app
from usm.settings import SettingsStore
import usm.web as web

def test_settings_api_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(web, "settings_store", SettingsStore(tmp_path/"settings.json"))
    client=TestClient(app)
    assert client.get("/api/settings").json()["mode"] == "virtual"
    result=client.put("/api/settings",json={"trace_capacity": 8192,"theme":"light"})
    assert result.status_code == 200, result.text
    assert result.json()["trace_capacity"] == 8192
    assert client.get("/api/settings").json()["theme"] == "light"

def test_settings_api_rejects_physical(tmp_path, monkeypatch):
    monkeypatch.setattr(web, "settings_store", SettingsStore(tmp_path/"settings.json"))
    client=TestClient(app)
    assert client.put("/api/settings",json={"mode":"physical"}).status_code == 422

def test_capability_flags():
    client=TestClient(app)
    caps=client.get("/api/capabilities").json()
    assert caps["virtual_matrix"] is True
    assert caps["hardware_discovery"] is False
    assert caps["musashi"] is False

def test_documentation_links():
    client=TestClient(app)
    docs=client.get("/api/docs-index").json()
    assert any(d["path"]=="docs/SETTINGS.md" for d in docs)

def test_settings_frontend():
    response=TestClient(app).get("/")
    assert response.status_code==200
    assert "Einstellungen speichern" in response.text
    assert "/api/settings" in response.text
