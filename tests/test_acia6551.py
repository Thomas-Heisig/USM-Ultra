"""Register-level ACIA tests; do not assert cycle or IRQ compatibility."""
from usm.machines.acia6551 import ACIA6551
from usm.machines.sbc6502 import SBC6502

def test_acia_registers():
    acia = ACIA6551()
    assert acia.read(1, 1) & 0x10
    acia.receive(b"AB")
    assert acia.read(1, 1) & 0x08
    assert acia.read(0, 1) == ord("A")
    assert acia.read(0, 1) == ord("B")
    acia.write(2, 1, 0x0B)
    acia.write(3, 1, 0x1F)
    assert acia.read(2, 1) == 0x0B
    assert acia.read(3, 1) == 0x1F
    acia.write(0, 1, ord("X"))
    assert acia.text() == "X"

def test_acia_bus_mapping():
    machine = SBC6502()
    machine.acia.receive(b"Q")
    assert machine.memory[0x8031] & 0x08
    assert machine.memory[0x8030] == ord("Q")
    machine.memory[0x8030] = ord("Y")
    assert machine.acia.text() == "Y"
