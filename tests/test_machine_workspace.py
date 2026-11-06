import pytest
from usm.machines.workspace import MachineWorkspace, WorkspaceError
from usm.machines.sbc6502 import SBC6502

def test_separate_workspaces(tmp_path):
    a = MachineWorkspace("usm-6502", tmp_path)
    b = MachineWorkspace("another-cpu", tmp_path)
    a.add_software("test.bin", b"hello")
    assert len(a.software()) == 1
    assert b.software() == []

@pytest.mark.parametrize("name", ["../escape", "/tmp/x", "hello space", "a\\b"])
def test_invalid_machine_id(tmp_path, name):
    with pytest.raises(WorkspaceError):
        MachineWorkspace(name, tmp_path)

def test_invalid_software_name(tmp_path):
    ws = MachineWorkspace("usm-6502", tmp_path)
    with pytest.raises(WorkspaceError):
        ws.add_software("../bad.bin", b"x")

def test_duplicate_software_rejected(tmp_path):
    ws = MachineWorkspace("usm-6502", tmp_path)
    ws.add_software("demo.bin", b"x")
    with pytest.raises(WorkspaceError):
        ws.add_software("demo.bin", b"y")

def test_snapshot_roundtrip(tmp_path):
    pytest.importorskip("py65")
    ws = MachineWorkspace("usm-6502", tmp_path)
    machine = SBC6502()
    machine.boot()
    machine.ram.data[10] = 99
    machine.cpu.a = 77
    machine.cpu.pc = 0xE002
    ws.save(machine, "state1")
    machine.ram.data[10] = 0
    machine.cpu.a = 0
    ws.restore(machine, "state1")
    assert machine.ram.data[10] == 99
    assert machine.cpu.a == 77
    assert machine.cpu.pc == 0xE002

def test_snapshot_rejects_other_rom(tmp_path):
    pytest.importorskip("py65")
    ws = MachineWorkspace("usm-6502", tmp_path)
    ws.save(SBC6502(), "one")
    machine = SBC6502()
    machine.rom.data[0] ^= 1
    with pytest.raises(WorkspaceError, match="ROM checksum"):
        ws.restore(machine, "one")
