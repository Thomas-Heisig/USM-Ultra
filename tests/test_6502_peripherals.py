import pytest
from usm.machines.sbc6502 import SBC6502
from usm.machines.peripherals import SerialPort, Timer, GPIO

def test_serial_rx_tx():
    p=SerialPort()
    p.receive(b"A")
    assert p.read(1,1)&1
    assert p.read(0,1)==65
    p.write(0,1,66)
    assert p.text()=="B"

def test_timer_period_and_ack():
    t=Timer()
    t.write(0,1,3)
    t.write(2,1,1)
    t.advance(3)
    assert t.read(3,1)==1
    t.write(3,1,1)
    assert t.read(3,1)==0

def test_gpio_direction():
    g=GPIO()
    g.inputs=0xF0
    g.write(1,1,0x0F)
    g.write(0,1,0x05)
    assert g.read(0,1)==0xF5

def test_program_load_and_execution():
    pytest.importorskip("py65")
    m=SBC6502()
    # LDA #$41; STA $8000; JMP $0205
    m.load_program(bytes.fromhex("A9418D00804C0502"),0x0200)
    m.step(3)
    assert m.uart.text()=="A"
    assert m.cpu.pc==0x0205

def test_program_bounds():
    m=SBC6502()
    with pytest.raises(ValueError):
        m.load_program(b"X"*100,0x7FF0)

def test_peripheral_bus_mapping():
    m=SBC6502()
    m.memory[0x8021]=0xFF
    m.memory[0x8020]=0xA5
    assert m.memory[0x8020]==0xA5
