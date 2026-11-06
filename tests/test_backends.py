import pytest
from usm.backends import BackendKind, DeviceRegistry, MatrixBackend
from usm.core import Matrix, Mapping, RAM, Transaction, Response

def virtual_registry():
    matrix = Matrix()
    matrix.map(Mapping(0, 256, RAM(256), "RAM"))
    registry = DeviceRegistry()
    registry.register("cpu0", MatrixBackend(matrix, "m68000"))
    return registry

def test_virtual_backend_without_hardware():
    registry = virtual_registry()
    assert registry.transact("cpu0", Transaction("cpu0", 0, 1, True, 42)).error is None
    assert registry.transact("cpu0", Transaction("cpu0", 0)).value == 42

def test_default_backend_is_emulated():
    registry = virtual_registry()
    assert registry.devices["cpu0"]["active"].capabilities().backend == BackendKind.EMULATED

def test_no_live_swap_without_quiescence():
    registry = virtual_registry()
    with pytest.raises(RuntimeError, match="quiescence"):
        registry.select("cpu0", "virtual")

def test_virtual_fallback_after_quiescence():
    registry = virtual_registry()
    assert registry.fallback("cpu0", quiesced=True).backend == BackendKind.EMULATED

def test_reject_physical_fallback():
    class FakeHardware:
        def capabilities(self):
            from usm.backends import Capabilities
            return Capabilities("m68000", BackendKind.HARDWARE, physical=True)
    with pytest.raises(ValueError):
        DeviceRegistry().register("cpu0", FakeHardware())

def test_hardware_offline_does_not_silently_switch():
    class Offline:
        def health(self): return False
        def capabilities(self):
            from usm.backends import Capabilities
            return Capabilities("m68000", BackendKind.HARDWARE, physical=True)
        def transact(self, request): return Response(value=999)
    registry = virtual_registry()
    registry.add_optional("cpu0", "chip", Offline())
    with pytest.raises(RuntimeError, match="offline"):
        registry.select("cpu0", "chip", quiesced=True)
    assert registry.devices["cpu0"]["active"].capabilities().backend == BackendKind.EMULATED
