"""USM-6502 single-board computer: RAM, memory-mapped UART, monitor ROM.

Requires optional py65 CPU dependency. Hardware adapters can replace the CPU
backend without changing the memory map or UART contract.
"""
from dataclasses import dataclass
from . import __doc__ as _machine_doc
from ..core import Matrix, Mapping, RAM, Transaction
from .peripherals import SerialPort, Timer, GPIO

RAM_START, RAM_SIZE = 0x0000, 0x8000
UART_ADDR = 0x8000
ROM_START, ROM_SIZE = 0xE000, 0x2000
RESET_VECTOR = 0xFFFC

class UART:
    """Simple transmit register. Not a real 6551 ACIA implementation."""
    def __init__(self):
        self.output = bytearray()
    def read(self, offset, width):
        if offset != 0 or width != 1:
            raise ValueError("UART only supports byte register at offset 0")
        return 0
    def write(self, offset, width, value):
        if offset != 0 or width != 1:
            raise ValueError("UART only supports byte register at offset 0")
        self.output.append(value & 0xFF)
    def text(self):
        return self.output.decode("ascii", errors="replace")

class BusMemory:
    """py65 byte-addressable memory adapter backed by the USM matrix."""
    def __init__(self, matrix):
        self.matrix = matrix
    def __len__(self):
        return 65536
    def __getitem__(self, address):
        if not isinstance(address, int):
            raise TypeError("byte address required")
        result = self.matrix.transact(Transaction("6502", address & 0xFFFF, 1))
        if result.error:
            raise RuntimeError(result.error)
        return result.value
    def __setitem__(self, address, value):
        if not isinstance(address, int):
            raise TypeError("byte address required")
        result = self.matrix.transact(Transaction("6502", address & 0xFFFF, 1, True, value & 0xFF))
        if result.error:
            raise RuntimeError(result.error)

def demo_rom():
    """Original, redistributable tiny boot program, not proprietary firmware.

    E000: LDX #$00
    E002: LDA $E014,X
    E005: BEQ E00F
    E007: STA $8000
    E00A: INX
    E00B: JMP E002
    E00E: NOP
    E00F: JMP E00F (idle)
    E012: padding
    E014: NUL-terminated text
    """
    rom = bytearray([0xEA] * ROM_SIZE)
    program = bytes([
        0xA2,0x00,             # LDX #0
        0xBD,0x14,0xE0,        # LDA $E014,X
        0xF0,0x08,             # BEQ E00F
        0x8D,0x00,0x80,        # STA $8000
        0xE8,                  # INX
        0x4C,0x02,0xE0,       # JMP E002
        0xEA,                  # NOP
        0x4C,0x0F,0xE0,       # JMP E00F
        0xEA,0xEA,             # padding
    ])
    rom[:len(program)] = program
    rom[0x14:0x14+11] = b"USM-6502 OK"
    rom[0x14+11] = 0
    rom[0x1FFC:0x1FFE] = (ROM_START).to_bytes(2, "little")
    rom[0x1FFA:0x1FFC] = (ROM_START).to_bytes(2, "little")
    rom[0x1FFE:0x2000] = (ROM_START).to_bytes(2, "little")
    return bytes(rom)

@dataclass
class RunResult:
    steps: int
    pc: int
    uart_text: str
    matrix_ticks: int

class SBC6502:
    def __init__(self, rom=None):
        self.matrix = Matrix()
        self.ram = RAM(RAM_SIZE)
        self.uart = SerialPort()
        self.timer = Timer()
        self.gpio = GPIO()
        self.rom = RAM(ROM_SIZE, readonly=True)
        image = demo_rom() if rom is None else bytes(rom)
        if len(image) != ROM_SIZE:
            raise ValueError("ROM must be exactly 8192 bytes")
        self.rom.data[:] = image
        self.matrix.map(Mapping(RAM_START, RAM_SIZE, self.ram, "6502 RAM"))
        self.matrix.map(Mapping(UART_ADDR, 2, self.uart, "Serial RX/TX"))
        self.matrix.map(Mapping(0x8010, 4, self.timer, "Timer"))
        self.matrix.map(Mapping(0x8020, 2, self.gpio, "GPIO"))
        self.matrix.map(Mapping(ROM_START, ROM_SIZE, self.rom, "6502 ROM", write=False))
        self.memory = BusMemory(self.matrix)
        self.cpu = None
    def boot(self):
        try:
            from py65.devices.mpu6502 import MPU
        except ImportError as exc:
            raise RuntimeError("Install optional CPU dependency: pip install -e '.[6502]'") from exc
        self.cpu = MPU(memory=self.memory)
        self.cpu.reset()
        return self.cpu.pc
    def load_program(self, payload, address=0x0200, start=True):
        if not isinstance(payload, (bytes, bytearray)) or not payload:
            raise ValueError("program must contain bytes")
        if not 0 <= address < RAM_SIZE or address + len(payload) > RAM_SIZE:
            raise ValueError("program does not fit RAM")
        self.ram.data[address:address+len(payload)] = payload
        if self.cpu is None:
            self.boot()
        if start:
            self.cpu.pc = address
        return {"address": address, "size": len(payload), "pc": self.cpu.pc}

    def step(self, count=1):
        if not 1 <= count <= 100000:
            raise ValueError("step count out of range")
        if self.cpu is None:
            self.boot()
        for _ in range(count):
            self.cpu.step()
            self.timer.advance(1)
        return self.status()

    def peripherals(self):
        return {"serial": {"rx_pending": len(self.uart.input), "tx": self.uart.text()},
                "timer": {"period": self.timer.period, "counter": self.timer.counter,
                          "enabled": self.timer.enabled, "pending": self.timer.pending},
                "gpio": {"data": self.gpio.data, "direction": self.gpio.direction, "inputs": self.gpio.inputs},
                "hardware": "not_available"}

    def run(self, max_steps=10000):
        if self.cpu is None:
            self.boot()
        steps = 0
        while steps < max_steps:
            if self.cpu.pc == 0xE00F:
                break
            self.cpu.step()
            self.timer.advance(1)
            steps += 1
        return RunResult(steps, self.cpu.pc, self.uart.text(), self.matrix.tick)
    def status(self):
        return {
            "machine": "usm-6502",
            "cpu": "MOS 6502 (py65 software)",
            "cpu_backend": "emulated",
            "hardware": "not_probed",
            "pc": self.cpu.pc if self.cpu else None,
            "uart_output": self.uart.text(),
            "matrix_ticks": self.matrix.tick,
            "memory_map": [
                {"start": "0x0000", "end": "0x7FFF", "name": "RAM"},
                {"start": "0x8000", "end": "0x8001", "name": "Serial RX/TX"},
                {"start": "0x8010", "end": "0x8013", "name": "Timer"},
                {"start": "0x8020", "end": "0x8021", "name": "GPIO"},
                {"start": "0xE000", "end": "0xFFFF", "name": "ROM"},
            ],
        }
