"""Backend registry for virtual-first execution and optional hardware.

This is a policy scaffold, not a working hardware transport.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from .core import Response, Transaction

class BackendKind(str, Enum):
    EMULATED = "emulated"
    NATIVE = "native"
    HARDWARE = "hardware"

@dataclass(frozen=True)
class Capabilities:
    architecture: str
    backend: BackendKind
    snapshot: bool = False
    physical: bool = False

class Backend(Protocol):
    def capabilities(self) -> Capabilities: ...
    def transact(self, request: Transaction) -> Response: ...
    def health(self) -> bool: ...

class MatrixBackend:
    """Always-available software backend for virtual USP transactions."""
    def __init__(self, matrix, architecture="generic"):
        self.matrix = matrix
        self.architecture = architecture
    def capabilities(self):
        return Capabilities(self.architecture, BackendKind.EMULATED)
    def transact(self, request):
        return self.matrix.transact(request)
    def health(self):
        return True

class DeviceRegistry:
    """Select a healthy backend; virtual fallback is mandatory.

    Live migration is deliberately NOT provided. Callers must reset or
    establish state equivalence before switching a running CPU.
    """
    def __init__(self):
        self.devices = {}
    def register(self, device_id, virtual_backend):
        if virtual_backend.capabilities().physical:
            raise ValueError("software fallback must not be physical")
        self.devices[device_id] = {"virtual": virtual_backend, "active": virtual_backend, "optional": {}}
    def add_optional(self, device_id, name, backend):
        self.devices[device_id]["optional"][name] = backend
    def select(self, device_id, name="virtual", *, quiesced=False):
        entry = self.devices[device_id]
        candidate = entry["virtual"] if name == "virtual" else entry["optional"][name]
        if not quiesced:
            raise RuntimeError("backend switching requires quiescence or reset")
        if not candidate.health():
            raise RuntimeError("selected backend offline")
        entry["active"] = candidate
        return candidate.capabilities()
    def fallback(self, device_id, *, quiesced=False):
        return self.select(device_id, "virtual", quiesced=quiesced)
    def transact(self, device_id, request):
        entry = self.devices[device_id]
        if not entry["active"].health():
            return Response(error="TARGET_OFFLINE: reset or quiesce before fallback")
        return entry["active"].transact(request)
