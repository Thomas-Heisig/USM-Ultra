import pytest
from usm.machines.sbc6502 import SBC6502, demo_rom, UART, BusMemory, ROM_START

def test_rom_vectors():
    image = demo_rom()
    assert len(image) == 8192
    assert int.from_bytes(image[0x1FFC:0x1FFE], "little") == ROM_START

def test_rom_protected():
    machine = SBC6502()
    with pytest.raises(RuntimeError, match="permission"):
        machine.memory[0xE000] = 0xFF

def test_uart_byte_register():
    uart = UART()
    uart.write(0, 1, 65)
    assert uart.text() == "A"

def test_uart_rejects_word():
    with pytest.raises(ValueError):
        UART().write(0, 2, 0x4142)

def test_bus_memory_ram_roundtrip():
    machine = SBC6502()
    machine.memory[0x1234] = 0xAB
    assert machine.memory[0x1234] == 0xAB

def test_invalid_rom_length():
    with pytest.raises(ValueError):
        SBC6502(b"short")

def test_6502_boot_and_output():
    pytest.importorskip("py65")
    machine = SBC6502()
    assert machine.boot() == ROM_START
    result = machine.run()
    assert result.uart_text == "USM-6502 OK"
    assert result.pc == 0xE00F
    assert result.steps < 10000
