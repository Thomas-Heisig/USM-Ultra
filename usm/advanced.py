"""Semantic reference modules, not physical timing simulation."""
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
import hashlib, json, time
from .core import Matrix, Transaction

class WindowManager:
    def __init__(self, matrix):
        self.matrix, self.generation, self.lock = matrix, 0, Lock()
    def replace(self, mappings, expected_generation):
        with self.lock:
            if expected_generation != self.generation:
                raise ValueError("stale WIN_GENERATION")
            candidate = Matrix()
            for m in mappings:
                candidate.map(m)
            self.matrix.mappings = candidate.mappings
            self.generation += 1
            return self.generation

@dataclass
class Lease:
    task_id: int
    architecture: str
    owner: str
    expires_at: float
    state: str = "running"

class AtomicTaskQueue:
    """Claims linearize at the lock; no real-time fairness guarantee."""
    def __init__(self, clock=None):
        self.clock = clock or time.monotonic
        self.lock, self.pending, self.leases = Lock(), deque(), {}
        self.next_id = 1
    def submit(self, architecture):
        with self.lock:
            task_id = self.next_id
            self.next_id += 1
            self.pending.append((task_id, architecture))
            return task_id
    def _expire(self):
        for lease in list(self.leases.values()):
            if lease.state == "running" and lease.expires_at <= self.clock():
                lease.state = "expired"
                self.pending.append((lease.task_id, lease.architecture))
    def claim(self, worker, capabilities, ttl=30.0):
        with self.lock:
            self._expire()
            for item in list(self.pending):
                task_id, arch = item
                if arch == "any" or arch in capabilities:
                    self.pending.remove(item)
                    lease = Lease(task_id, arch, worker, self.clock() + ttl)
                    self.leases[task_id] = lease
                    return lease
            return None
    def complete(self, task_id, worker):
        with self.lock:
            lease = self.leases[task_id]
            if lease.owner != worker or lease.state != "running":
                raise PermissionError("not lease owner")
            lease.state = "done"

class RomLibrary:
    def __init__(self, root):
        self.root = Path(root)
    def inventory(self, manifest):
        root = self.root.resolve()
        result = []
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1048576), b""):
                    digest.update(block)
            result.append({"path": str(path.relative_to(root)), "bytes": path.stat().st_size, "sha256": digest.hexdigest()})
        dest = Path(manifest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

class MiniM68K:
    """Small opcode smoke-test interpreter; NOT a complete CPU emulator."""
    def __init__(self, matrix, pc=0):
        self.matrix, self.pc, self.d, self.stopped = matrix, pc, [0]*8, False
    def _access(self, address, width, write=False, value=0):
        if width > 1 and address % 2:
            raise ValueError("68000 address error")
        result = self.matrix.transact(Transaction("m68k-mini", address, width, write, value))
        if result.error:
            raise ValueError(result.error)
        return result.value
    def _fetch(self, width):
        value = self._access(self.pc, width)
        self.pc += width
        return value
    def step(self):
        if self.stopped:
            return
        op = self._fetch(2)
        if op == 0x4E71:
            return
        if op == 0x4E72:
            self._fetch(2)
            self.stopped = True
            return
        if op & 0xF100 == 0x7000:
            imm = op & 255
            self.d[(op >> 9) & 7] = (imm if imm < 128 else imm - 256) & 0xFFFFFFFF
            return
        if op & 0xFFF8 == 0x23C0:
            reg = op & 7
            self._access(self._fetch(4), 4, True, self.d[reg])
            return
        if op & 0xF1FF == 0x2039:
            reg = (op >> 9) & 7
            self.d[reg] = self._access(self._fetch(4), 4)
            return
        raise NotImplementedError(f"unsupported opcode {op:04x}")
    def run(self, max_steps=1000):
        for _ in range(max_steps):
            if self.stopped:
                break
            self.step()
        return {"pc": self.pc, "d": self.d.copy(), "stopped": self.stopped}
