from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class Transaction:
    source: str
    address: int
    width: int = 1
    write: bool = False
    value: int = 0

@dataclass
class Response:
    value: int = 0
    cycles: int = 0
    error: str | None = None

class RAM:
    def __init__(self, size=65536, readonly=False):
        self.data = bytearray(size)
        self.readonly = readonly
    def read(self, offset, width):
        if offset < 0 or offset + width > len(self.data):
            raise ValueError("out of bounds")
        return int.from_bytes(self.data[offset:offset+width], "big")
    def write(self, offset, width, value):
        if self.readonly:
            raise PermissionError("read-only ROM")
        if offset < 0 or offset + width > len(self.data):
            raise ValueError("out of bounds")
        self.data[offset:offset+width] = value.to_bytes(width, "big")

@dataclass
class Mapping:
    start: int
    size: int
    device: RAM
    name: str
    read: bool = True
    write: bool = True
    latency: int = 2
    @property
    def end(self):
        return self.start + self.size

class Matrix:
    def __init__(self):
        self.mappings = []
        self.tick = 0
        self.trace = deque(maxlen=4096)
    def map(self, mapping):
        if mapping.start < 0 or mapping.size <= 0 or mapping.end > 0x100000000:
            raise ValueError("invalid mapping")
        if any(mapping.start < m.end and m.start < mapping.end for m in self.mappings):
            raise ValueError("overlapping memory windows")
        self.mappings.append(mapping)
    def transact(self, tx):
        mapping = next((m for m in self.mappings if m.start <= tx.address and tx.address + tx.width <= m.end), None)
        value, error = 0, None
        try:
            if tx.width not in (1,2,4):
                raise ValueError("unsupported width")
            if mapping is None:
                raise ValueError("unmapped address")
            if tx.write and not mapping.write or not tx.write and not mapping.read:
                raise PermissionError("window permission denied")
            offset = tx.address - mapping.start
            if tx.write:
                mapping.device.write(offset, tx.width, tx.value)
            else:
                value = mapping.device.read(offset, tx.width)
        except (ValueError, PermissionError, OverflowError) as exc:
            error = str(exc)
        cycles = mapping.latency if mapping else 1
        self.tick += cycles
        self.trace.append({"tick": self.tick, "source": tx.source, "address": tx.address, "error": error})
        return Response(value, cycles, error)

class VirtualCPU:
    """Bus-master stub; not an ISA emulator."""
    def __init__(self, name, architecture, matrix):
        self.name, self.architecture, self.matrix = name, architecture, matrix
        self.operations = 0
    def access(self, address, width=1, write=False, value=0):
        if self.architecture == "m68000" and width > 1 and address % 2:
            return Response(error="68000 address error")
        result = self.matrix.transact(Transaction(self.name, address, width, write, value))
        self.operations += 1
        return result

class Lab:
    def __init__(self):
        from .advanced import AtomicTaskQueue
        self.matrix = Matrix()
        self.ram = RAM(65536)
        self.sid = RAM(32)
        self.matrix.map(Mapping(0,65536,self.ram,"RAM"))
        self.matrix.map(Mapping(0xD40000,32,self.sid,"SID-register-stub"))
        self.scheduler = AtomicTaskQueue()
        self.cpus = {"cpu0": VirtualCPU("cpu0","m68000",self.matrix),
                     "cpu1": VirtualCPU("cpu1","z80",self.matrix)}
    def status(self):
        return {"tick": self.matrix.tick,
                "windows": [{"name":m.name,"start":hex(m.start),"size":m.size} for m in self.matrix.mappings],
                "cpus":{name:{"architecture":cpu.architecture,"operations":cpu.operations} for name,cpu in self.cpus.items()}}
