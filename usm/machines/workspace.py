"""Per-machine private workspace and versioned 6502 state snapshots."""
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from threading import RLock

ROOT = Path(os.environ.get("USM_MACHINE_HOME", Path.home() / ".usm-ultra" / "machines"))
IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")
SCHEMA = 1

class WorkspaceError(ValueError):
    pass

class MachineWorkspace:
    def __init__(self, machine_id="usm-6502", root=None):
        if not IDENTIFIER.fullmatch(machine_id):
            raise WorkspaceError("invalid machine ID")
        self.machine_id = machine_id
        self.root = Path(root) if root is not None else ROOT
        self.path = self.root / machine_id
        self.lock = RLock()

    def ensure(self):
        for name in ("software", "roms", "snapshots", "media"):
            (self.path / name).mkdir(parents=True, exist_ok=True)
        return self.path

    def software(self):
        self.ensure()
        return sorted({"name": p.name, "bytes": p.stat().st_size} for p in (self.path / "software").iterdir() if p.is_file() and not p.is_symlink())

    def add_software(self, name, content):
        if not IDENTIFIER.fullmatch(name.rsplit(".", 1)[0]) or not re.fullmatch(r"[a-zA-Z0-9_-]+\.(bin|prg|rom)", name):
            raise WorkspaceError("invalid software filename")
        if len(content) > 1048576:
            raise WorkspaceError("software exceeds 1 MiB")
        self.ensure()
        dest = self.path / "software" / name
        with self.lock:
            if dest.exists():
                raise WorkspaceError("software already exists")
            dest.write_bytes(content)
        return {"name": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}

    def save(self, machine, name):
        if not IDENTIFIER.fullmatch(name):
            raise WorkspaceError("invalid snapshot name")
        if machine.cpu is None:
            machine.boot()
        cpu = machine.cpu
        registers = {key: int(getattr(cpu, key)) for key in ("pc", "sp", "a", "x", "y", "p")}
        state = {
            "schema": SCHEMA, "machine": "usm-6502", "cpu_backend": "py65",
            "rom_sha256": hashlib.sha256(machine.rom.data).hexdigest(),
            "ram_sha256": hashlib.sha256(machine.ram.data).hexdigest(),
            "registers": registers,
            "ram": machine.ram.data.hex(),
            "uart": machine.uart.output.hex(),
            "matrix_tick": machine.matrix.tick,
        }
        self.ensure()
        target = self.path / "snapshots" / (name + ".json")
        payload = json.dumps(state, separators=(",", ":")).encode("utf-8")
        with self.lock:
            fd, tmp = tempfile.mkstemp(prefix=".snapshot-", dir=target.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(tmp, target)
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
        return {"name": name, "bytes": len(payload), "ram_sha256": state["ram_sha256"]}

    def snapshots(self):
        self.ensure()
        return sorted(p.stem for p in (self.path / "snapshots").glob("*.json") if p.is_file() and not p.is_symlink())

    def restore(self, machine, name):
        if not IDENTIFIER.fullmatch(name):
            raise WorkspaceError("invalid snapshot name")
        path = self.path / "snapshots" / (name + ".json")
        with self.lock:
            if path.is_symlink():
                raise WorkspaceError("snapshot symlink rejected")
            state = json.loads(path.read_text(encoding="utf-8"))
            if state.get("schema") != SCHEMA or state.get("machine") != "usm-6502":
                raise WorkspaceError("unsupported snapshot format")
            if state.get("cpu_backend") != "py65":
                raise WorkspaceError("incompatible CPU backend")
            if state.get("rom_sha256") != hashlib.sha256(machine.rom.data).hexdigest():
                raise WorkspaceError("ROM checksum mismatch")
            ram = bytes.fromhex(state["ram"])
            uart = bytes.fromhex(state["uart"])
            if len(ram) != len(machine.ram.data) or len(uart) > 1048576:
                raise WorkspaceError("invalid snapshot memory")
            if hashlib.sha256(ram).hexdigest() != state["ram_sha256"]:
                raise WorkspaceError("RAM checksum mismatch")
            regs = state["registers"]
            if set(regs) != {"pc", "sp", "a", "x", "y", "p"}:
                raise WorkspaceError("invalid CPU registers")
            for key, value in regs.items():
                if type(value) is not int or not 0 <= value <= (65535 if key == "pc" else 255):
                    raise WorkspaceError("invalid CPU register value")
            tick = state["matrix_tick"]
            if type(tick) is not int or tick < 0:
                raise WorkspaceError("invalid matrix tick")
            if machine.cpu is None:
                machine.boot()
            machine.ram.data[:] = ram
            machine.uart.output[:] = uart
            for key, value in regs.items():
                setattr(machine.cpu, key, value)
            machine.matrix.tick = tick
            return {"name": name, "pc": machine.cpu.pc, "uart_output": machine.uart.text()}
