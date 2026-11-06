import json
import pytest
from usm.settings import SettingsStore, SettingsError, validate, DEFAULTS

def test_defaults(tmp_path):
    assert SettingsStore(tmp_path/"settings.json").read() == DEFAULTS

def test_persistent_settings(tmp_path):
    path = tmp_path/"settings.json"
    store = SettingsStore(path)
    store.update({"trace_capacity": 32768, "locale": "en"})
    assert SettingsStore(path).read()["trace_capacity"] == 32768
    assert json.loads(path.read_text())["locale"] == "en"

@pytest.mark.parametrize("bad", [
    {"mode": "physical"}, {"mode": "hybrid"}, {"auto_fallback": True},
    {"hardware_policy": "prefer_verified"}, {"trace_capacity": 0},
    {"trace_capacity": True}, {"trace_capacity": 2000000},
    {"theme": "blue"}, {"unknown": 1}, {"schema_version": 2},
])
def test_invalid_configuration(bad):
    with pytest.raises(SettingsError):
        validate(bad)

def test_failed_update_preserves_file(tmp_path):
    store = SettingsStore(tmp_path/"settings.json")
    store.update({"theme": "light"})
    with pytest.raises(SettingsError):
        store.update({"mode": "physical"})
    assert store.read()["theme"] == "light"

def test_no_implicit_file_creation(tmp_path):
    path = tmp_path/"settings.json"
    SettingsStore(path).read()
    assert not path.exists()
