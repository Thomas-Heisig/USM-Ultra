from usm.machines.basic_console import BasicConsole
from usm.machines.workspace import MachineWorkspace

def test_basic_slash_is_integer_division():
    console = BasicConsole()
    console.submit("10 PRINT 7/2")
    assert console.submit("RUN")["output"][-1] == "3"

def test_workspace_multiple_software_files_sorted(tmp_path):
    workspace = MachineWorkspace("usm-6502", tmp_path)
    workspace.add_software("zeta.bin", b"Z")
    workspace.add_software("alpha.bin", b"A")
    assert [item["name"] for item in workspace.software()] == ["alpha.bin", "zeta.bin"]
