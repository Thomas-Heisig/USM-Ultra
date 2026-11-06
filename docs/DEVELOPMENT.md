# Entwicklungsumgebung

## Voraussetzungen

Python >=3.11, Git; für die Weboberfläche FastAPI und Uvicorn.

```bash
python -m venv .venv
python -m pip install -e ".[web,test]"
python -m pytest -q
python -m usm.cli status
python -m usm.cli demo
python -m usm.cli web
```

Web: http://127.0.0.1:8000 (nur localhost).

## Akzeptanzkriterien

- Tests unter Python 3.11/3.12/3.13 in CI
- Keine ROMs, Datenträgerimages oder lokalen Manifeste im Repository
- Neue CPU-Backends müssen dieselbe Matrix-Semantik verwenden
- C-Bindings dürfen keine Python-Callbacks aus fremden Threads ohne gesicherte Synchronisierung aufrufen
- Timingwerte werden als Simulation oder Messung gekennzeichnet

## Native Emulatoren

Musashi als C-Backend ist geplant, **nicht integriert**. Fremdquellen nicht unbesehen kopieren; Version und Lizenz dokumentieren. Hatari, WinUAE und MAME sind zunächst Referenzsysteme.
