"""Local configuration for MasterVisor. No secrets or ROM contents are stored."""
import json
import os
import tempfile
from pathlib import Path
from threading import RLock

DEFAULTS = {
    "schema_version": 1,
    "mode": "virtual",
    "hardware_policy": "manual",
    "trace_capacity": 65536,
    "theme": "dark",
    "locale": "de",
    "default_cpu": "cpu0",
    "auto_fallback": False,
}
_ALLOWED = {
    "mode": {"virtual", "hybrid", "physical"},
    "hardware_policy": {"manual", "prefer_verified"},
    "theme": {"dark", "light"},
    "locale": {"de", "en"},
    "default_cpu": {"cpu0", "cpu1"},
}
class SettingsError(ValueError):
    pass

def validate(payload):
    if not isinstance(payload, dict):
        raise SettingsError("settings must be an object")
    if set(payload) - set(DEFAULTS):
        raise SettingsError("unknown setting")
    candidate = {**DEFAULTS, **payload}
    for key, choices in _ALLOWED.items():
        if candidate[key] not in choices:
            raise SettingsError(f"invalid {key}")
    if type(candidate["trace_capacity"]) is not int or not 256 <= candidate["trace_capacity"] <= 1048576:
        raise SettingsError("trace_capacity must be 256..1048576")
    if type(candidate["auto_fallback"]) is not bool:
        raise SettingsError("auto_fallback must be boolean")
    if candidate["schema_version"] != 1:
        raise SettingsError("unsupported schema_version")
    if candidate["mode"] != "virtual":
        raise SettingsError("hybrid/physical modes are not implemented; select virtual")
    if candidate["hardware_policy"] != "manual" or candidate["auto_fallback"]:
        raise SettingsError("hardware discovery and automatic fallback are not implemented")
    return candidate

class SettingsStore:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else Path(os.environ.get("USM_SETTINGS_PATH", Path.home()/".usm-ultra"/"settings.json"))
        self.lock = RLock()
    def read(self):
        with self.lock:
            if not self.path.exists():
                return dict(DEFAULTS)
            return validate(json.loads(self.path.read_text(encoding="utf-8")))
    def update(self, changes):
        with self.lock:
            current = self.read()
            updated = validate({**current, **changes})
            self.path.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(prefix=".settings-", suffix=".json", dir=self.path.parent)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as out:
                    json.dump(updated, out, indent=2, ensure_ascii=False)
                    out.write("\n")
                    out.flush()
                    os.fsync(out.fileno())
                os.replace(tmp, self.path)
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
            return updated
