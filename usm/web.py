"""Local-only MasterVisor development interface; do not expose publicly."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import Lab
from .catalog import components, component, summary
from .settings import SettingsStore, SettingsError
from collections import deque

app=FastAPI(title="USM MasterVisor",version="0.2.0")
lab=Lab()
settings_store=SettingsStore()
try:
    lab.matrix.trace = deque(lab.matrix.trace, maxlen=settings_store.read()['trace_capacity'])
except (OSError, ValueError):
    pass
class Access(BaseModel):
    cpu: str = "cpu0"
    address: int = Field(ge=0,le=0xFFFFFFFF)
    width: int = 1
    write: bool = False
    value: int = Field(default=0,ge=0,le=0xFFFFFFFF)

class SettingsUpdate(BaseModel):
    mode: str | None = None
    hardware_policy: str | None = None
    trace_capacity: int | None = Field(default=None, ge=256, le=1048576)
    theme: str | None = None
    locale: str | None = None
    default_cpu: str | None = None
    auto_fallback: bool | None = None

@app.get("/api/settings")
def get_settings():
    try:
        return settings_store.read()
    except (OSError, ValueError) as exc:
        raise HTTPException(500, f"settings read error: {exc}")

@app.put("/api/settings")
def put_settings(changes: SettingsUpdate):
    payload=changes.model_dump(exclude_none=True)
    try:
        updated=settings_store.update(payload)
    except (SettingsError, ValueError) as exc:
        raise HTTPException(422, str(exc))
    except OSError as exc:
        raise HTTPException(500, f"settings write error: {exc}")
    lab.matrix.trace=deque(lab.matrix.trace,maxlen=updated["trace_capacity"])
    return updated

@app.get("/api/capabilities")
def capabilities():
    return {
        "virtual_matrix": True,
        "component_catalog": True,
        "settings": True,
        "trace": True,
        "full_m68000": False,
        "musashi": False,
        "machine_boot": False,
        "hardware_discovery": False,
        "hybrid_mode": False,
        "physical_mode": False,
        "timing_t0": False,
    }

@app.get("/api/docs-index")
def docs_index():
    return [
        {"title":"Projektstatus","path":"STATUS.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/STATUS.md"},
        {"title":"Einstellungen","path":"docs/SETTINGS.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/SETTINGS.md"},
        {"title":"Chipkatalog","path":"docs/CHIP_CATALOG.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/CHIP_CATALOG.md"},
        {"title":"Virtual-First Architektur","path":"docs/VIRTUAL_FIRST.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/VIRTUAL_FIRST.md"},
        {"title":"Zeitklassen und Modi","path":"docs/MODES_AND_TIMING.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/MODES_AND_TIMING.md"},
        {"title":"V7-Studie (Kapitelübersicht)","path":"docs/STUDIE_V7.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/STUDIE_V7.md"},
    ]

@app.get("/api/machines")
def machines():
    return [{"id":"usm-6502","name":"USM-6502 SBC","backend":"py65","hardware":"not_probed","status":"experimental","description":"32 KiB RAM, 8 KiB ROM, synthetic UART; software-only"}]

@app.post("/api/machines/usm-6502/run")
def run_6502():
    from .machines.sbc6502 import SBC6502
    try:
        machine=SBC6502()
        result=machine.run()
        return {"result": vars(result), "status": machine.status()}
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))

@app.get("/api/components")
def list_components(family: str | None = None):
    return components(family)

@app.get("/api/components/summary")
def component_summary():
    return summary()

@app.get("/api/components/{component_id}")
def get_component(component_id: str):
    item = component(component_id)
    if item is None:
        raise HTTPException(404, "unknown component")
    return item

@app.get("/api/status")
def status():
    return lab.status()
@app.get("/api/trace")
def trace():
    return list(lab.matrix.trace)
@app.post("/api/access")
def access(request: Access):
    cpu=lab.cpus.get(request.cpu)
    if not cpu:
        raise HTTPException(404,"unknown CPU")
    return vars(cpu.access(request.address,request.width,request.write,request.value))
class TaskCreate(BaseModel):
    architecture: str = Field(min_length=1, max_length=64)

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    if task.architecture not in ("any", "m68000", "z80", "mos6502"):
        raise HTTPException(422, "unsupported architecture")
    task_id = lab.scheduler.submit(task.architecture)
    return {"id": task_id, "architecture": task.architecture, "state": "pending", "owner": None}

@app.get("/api/tasks")
def list_tasks():
    scheduler = lab.scheduler
    with scheduler.lock:
        pending = [{"id": task_id, "architecture": arch, "state": "pending", "owner": None} for task_id, arch in scheduler.pending]
        leased = [{"id": item.task_id, "architecture": item.architecture, "state": item.state, "owner": item.owner} for item in scheduler.leases.values()]
        return sorted(pending + leased, key=lambda x: x["id"])

@app.get("/api/memory")
def read_memory(address: int = 0, count: int = 64):
    if not 0 <= address <= 0xFFFFFFFF or not 1 <= count <= 256 or address + count > 0x100000000:
        raise HTTPException(422, "invalid memory range")
    lines = []
    errors = 0
    for start in range(address, address + count, 16):
        row = []
        for location in range(start, min(start + 16, address + count)):
            result = lab.cpus["cpu0"].access(location, 1)
            if result.error:
                errors += 1
                row.append("??")
            else:
                row.append(f"{result.value:02X}")
        lines.append(f"{start:08X}  " + " ".join(row))
    return {"address": address, "count": count, "errors": errors, "lines": lines}

@app.get("/")
def home():
    from fastapi.responses import HTMLResponse
    from pathlib import Path
    path = Path(__file__).parent / "frontend" / "index.html"
    return HTMLResponse(path.read_text(encoding="utf-8"))
