"""6502 ROM build, vectors and execution smoke tests."""
import importlib.util
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "firmware" / "6502" / "build_boot.py"
spec = importlib.util.spec_from_file_location("usm_boot_builder", BUILDER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_rom_layout_and_vectors():
    image = module.build()
    assert len(image) == 8192
    assert image[0x14:0x20] == b"USM-6502 OK\\x00".decode("unicode_escape").encode("latin1")
    assert all(image[x:x+2] == b"\\x00\\xe0".decode("unicode_escape").encode("latin1") for x in (0x1FFA, 0x1FFC, 0x1FFE))

def test_rom_matches_runtime():
    from usm.machines.sbc6502 import demo_rom
    assert module.build() == demo_rom()

def test_boot_execution():
    import pytest
    pytest.importorskip("py65")
    from usm.machines.sbc6502 import SBC6502
    machine = SBC6502(rom=module.build())
    result = machine.run()
    assert result.uart_text == "USM-6502 OK"
    assert result.pc == 0xE00F
    assert result.steps < 10000
