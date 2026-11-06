"""Local-only MasterVisor development interface; do not expose publicly."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import Lab
from .catalog import components, component, summary
from .settings import SettingsStore, SettingsError
from collections import deque
from threading import RLock
from .machines.workspace import MachineWorkspace, WorkspaceError
from .machines.sbc6502 import SBC6502
from .machines.monitor6502 import Monitor, parse_image

machine_lock = RLock()
machine_6502 = None
monitor_6502 = None
workspace_6502 = MachineWorkspace()

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
        {"title":"MOS 6502: Referenzen, Systeme und ROMs","path":"docs/MOS_6502_REFERENCE.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/MOS_6502_REFERENCE.md"},
        {"title":"6502 Monitor und Image Loader","path":"docs/MONITOR_6502.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/MONITOR_6502.md"},
        {"title":"6502 Peripherie","path":"docs/PERIPHERALS_6502.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/PERIPHERALS_6502.md"},
        {"title":"Projektstatus","path":"STATUS.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/STATUS.md"},
        {"title":"Einstellungen","path":"docs/SETTINGS.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/SETTINGS.md"},
        {"title":"Chipkatalog","path":"docs/CHIP_CATALOG.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/CHIP_CATALOG.md"},
        {"title":"Virtual-First Architektur","path":"docs/VIRTUAL_FIRST.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/VIRTUAL_FIRST.md"},
        {"title":"Zeitklassen und Modi","path":"docs/MODES_AND_TIMING.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/MODES_AND_TIMING.md"},
        {"title":"V7-Studie (Kapitelübersicht)","path":"docs/STUDIE_V7.md","url":"https://github.com/Thomas-Heisig/USM-Ultra/blob/main/docs/STUDIE_V7.md"},
    ]

class SnapshotRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)

class SoftwareRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    hex_data: str = Field(min_length=2, max_length=2097152)

@app.get("/api/machines/usm-6502/workspace")
def get_6502_workspace():
    with machine_lock:
        return {"machine": "usm-6502", "software": workspace_6502.software(), "snapshots": workspace_6502.snapshots(), "running": machine_6502 is not None, "status": machine_6502.status() if machine_6502 else None}

@app.post("/api/machines/usm-6502/software")
def upload_6502_software(request: SoftwareRequest):
    try:
        payload = bytes.fromhex(request.hex_data)
        return workspace_6502.add_software(request.name, payload)
    except (WorkspaceError, ValueError) as exc:
        raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/snapshots")
def save_6502_snapshot(request: SnapshotRequest):
    global machine_6502
    with machine_lock:
        try:
            if machine_6502 is None:
                machine_6502 = SBC6502()
                machine_6502.boot()
            return workspace_6502.save(machine_6502, request.name)
        except (RuntimeError, WorkspaceError) as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/snapshots/{name}/restore")
def restore_6502_snapshot(name: str):
    global machine_6502, monitor_6502
    with machine_lock:
        try:
            candidate = SBC6502()
            result = workspace_6502.restore(candidate, name)
            machine_6502 = candidate
            monitor_6502 = Monitor(candidate)
            return result
        except FileNotFoundError:
            raise HTTPException(404, "snapshot not found")
        except (RuntimeError, WorkspaceError, ValueError, KeyError, TypeError) as exc:
            raise HTTPException(422, str(exc))

@app.get("/api/6502/sources")
def sources_6502():
    from .machines.catalog6502 import SOURCES
    return SOURCES

@app.get("/api/6502/system-profiles")
def profiles_6502():
    from .machines.catalog6502 import SYSTEMS
    return SYSTEMS

class ImageLoad(BaseModel):
    name: str
    address: int | None = Field(default=None, ge=0, le=65535)
    start: bool = True

class BreakpointRequest(BaseModel):
    address: int = Field(ge=0, le=65535)
    enabled: bool = True

class MemoryEdit(BaseModel):
    address: int = Field(ge=0, le=65535)
    value: int = Field(ge=0, le=255)

def get_monitor():
    global monitor_6502
    machine = active_6502()
    if monitor_6502 is None or monitor_6502.machine is not machine:
        monitor_6502 = Monitor(machine)
    return monitor_6502

@app.get("/api/machines/usm-6502/monitor")
def monitor_status():
    with machine_lock:
        return get_monitor().state()

@app.post("/api/machines/usm-6502/monitor/reset")
def monitor_reset():
    with machine_lock:
        return get_monitor().reset()

@app.post("/api/machines/usm-6502/monitor/run")
def monitor_run(request: StepRequest):
    with machine_lock:
        try:
            return get_monitor().run(request.count)
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/monitor/step")
def monitor_step(request: StepRequest):
    with machine_lock:
        try:
            return get_monitor().step(request.count)
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/monitor/breakpoints")
def monitor_breakpoint(request: BreakpointRequest):
    with machine_lock:
        return get_monitor().breakpoint(request.address, request.enabled)

@app.get("/api/machines/usm-6502/monitor/memory")
def monitor_memory(address: int = 0, count: int = 64):
    with machine_lock:
        try:
            return get_monitor().inspect(address, count)
        except ValueError as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/monitor/memory")
def monitor_memory_write(request: MemoryEdit):
    with machine_lock:
        try:
            return get_monitor().poke(request.address, request.value)
        except ValueError as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/images/load")
def load_6502_image(request: ImageLoad):
    with machine_lock:
        try:
            import re
            if not re.fullmatch(r"[A-Za-z0-9_-]+\\.(bin|prg|rom|d64|dsk|img)", request.name, re.I):
                raise ValueError("invalid image filename")
            path = workspace_6502.path / "software" / request.name
            if path.is_symlink():
                raise ValueError("symlink not allowed")
            address, payload = parse_image(request.name, path.read_bytes(), request.address)
            result = active_6502().load_program(payload, address, request.start)
            return {"image": request.name, "format": request.name.rsplit(".", 1)[-1].lower(), **result}
        except FileNotFoundError:
            raise HTTPException(404, "image not found")
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(422, str(exc))

class ProgramLoad(BaseModel):
    name: str
    address: int = Field(default=0x0200, ge=0, lt=32768)
    start: bool = True

class StepRequest(BaseModel):
    count: int = Field(default=1, ge=1, le=100000)

class SerialInput(BaseModel):
    text: str = Field(max_length=4096)

class GPIOInput(BaseModel):
    value: int = Field(ge=0, le=255)

def active_6502():
    global machine_6502, monitor_6502
    if machine_6502 is None:
        machine_6502 = SBC6502()
        machine_6502.boot()
        monitor_6502 = Monitor(machine_6502)
    return machine_6502

@app.post("/api/machines/usm-6502/load")
def load_6502_program(request: ProgramLoad):
    with machine_lock:
        try:
            if not __import__("re").fullmatch(r"[A-Za-z0-9_-]+\\.(bin|prg|rom)", request.name):
                raise ValueError("invalid program filename")
            path = workspace_6502.path / "software" / request.name
            if path.is_symlink():
                raise ValueError("symlink not allowed")
            data = path.read_bytes()
            return active_6502().load_program(data, request.address, request.start)
        except FileNotFoundError:
            raise HTTPException(404, "program not found")
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/step")
def step_6502(request: StepRequest):
    with machine_lock:
        try:
            return active_6502().step(request.count)
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(422, str(exc))

@app.get("/api/machines/usm-6502/peripherals")
def peripherals_6502():
    with machine_lock:
        return active_6502().peripherals()

@app.post("/api/machines/usm-6502/serial/input")
def serial_input_6502(request: SerialInput):
    with machine_lock:
        try:
            machine = active_6502()
            machine.uart.receive(request.text.encode("ascii", errors="replace"))
            return machine.peripherals()["serial"]
        except ValueError as exc:
            raise HTTPException(422, str(exc))

@app.post("/api/machines/usm-6502/gpio/input")
def gpio_input_6502(request: GPIOInput):
    with machine_lock:
        machine = active_6502()
        machine.gpio.inputs = request.value
        return machine.peripherals()["gpio"]

@app.get("/api/machines")
def machines():
    return [{"id":"usm-6502","name":"USM-6502 SBC","backend":"py65","hardware":"not_probed","status":"experimental","description":"32 KiB RAM, 8 KiB ROM, synthetic UART; software-only"}]

@app.post("/api/machines/usm-6502/run")
def run_6502():
    global machine_6502
    try:
        with machine_lock:
            if machine_6502 is None:
                machine_6502=SBC6502()
            result=machine_6502.run()
            return {"result": vars(result), "status": machine_6502.status()}
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
