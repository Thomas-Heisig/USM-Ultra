import pytest
from usm.machines.monitor6502 import Monitor, parse_image
from usm.machines.sbc6502 import SBC6502

def test_prg_load_address():
    addr, data = parse_image("demo.prg", bytes.fromhex("0002a941"))
    assert addr == 0x0200 and data == bytes.fromhex("a941")

def test_bin_requires_address():
    with pytest.raises(ValueError):
        parse_image("demo.bin", b"abc")

def test_disk_image_is_not_executable():
    with pytest.raises(ValueError):
        parse_image("disk.d64", b"abc", 0x200)

def test_rom_write_protected_by_loader():
    with pytest.raises(ValueError):
        parse_image("rom.bin", b"abc", 0xE000)

def test_monitor_memory_avoids_io_side_effects():
    m = Monitor(SBC6502())
    assert m.inspect(0x8000, 2)["bytes"] == [None, None]

def test_monitor_ram_edit():
    m = Monitor(SBC6502())
    m.poke(0x0200, 0xEA)
    assert m.inspect(0x0200, 1)["bytes"] == [0xEA]

def test_monitor_breakpoint_before_instruction():
    pytest.importorskip("py65")
    m = SBC6502()
    m.load_program(bytes.fromhex("a9418d0080"), 0x0200)
    monitor = Monitor(m)
    monitor.breakpoint(0x0202)
    result = monitor.run(100)
    assert result["reason"] == "breakpoint"
    assert m.cpu.pc == 0x0202
    assert m.uart.text() == ""

def test_monitor_step_after_breakpoint():
    pytest.importorskip("py65")
    m = SBC6502()
    m.load_program(bytes.fromhex("a9418d0080"), 0x0200)
    monitor = Monitor(m)
    monitor.step()
    assert m.cpu.a == 0x41
    assert m.cpu.pc == 0x0202
