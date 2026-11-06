"""Interactive, bounded 6502 monitor and image parser.

This is a custom SBC monitor, not a Commodore/Apple/Atari machine emulator.
"""
from dataclasses import dataclass, field

@dataclass
class Monitor:
    machine: object
    breakpoints: set[int] = field(default_factory=set)
    halted: bool = True

    def reset(self):
        self.machine.boot()
        self.halted = True
        return self.state()

    def state(self):
        cpu = self.machine.cpu
        return {
            "halted": self.halted,
            "breakpoints": sorted(self.breakpoints),
            "registers": None if cpu is None else {
                key: int(getattr(cpu, key)) for key in ("pc", "sp", "a", "x", "y", "p")},
            "peripherals": self.machine.peripherals(),
            "ticks": self.machine.matrix.tick,
        }

    def breakpoint(self, address, enabled=True):
        if not 0 <= address <= 0xFFFF:
            raise ValueError("breakpoint outside 6502 address space")
        if enabled:
            self.breakpoints.add(address)
        else:
            self.breakpoints.discard(address)
        return self.state()

    def run(self, max_steps=10000, ignore_initial_breakpoint=False):
        if not 1 <= max_steps <= 100000:
            raise ValueError("step budget must be 1..100000")
        if self.machine.cpu is None:
            self.machine.boot()
        self.halted = False
        steps = 0
        reason = "budget"
        while steps < max_steps:
            pc = self.machine.cpu.pc
            if pc in self.breakpoints and not (ignore_initial_breakpoint and steps == 0):
                reason = "breakpoint"
                break
            self.machine.step(1)
            steps += 1
        self.halted = True
        return {"reason": reason, "steps": steps, **self.state()}

    def step(self, count=1):
        if not 1 <= count <= 10000:
            raise ValueError("step budget must be 1..10000")
        self.machine.step(count)
        self.halted = True
        return self.state()

    def inspect(self, address, count=64):
        if not 0 <= address <= 0xFFFF or not 1 <= count <= 256 or address + count > 0x10000:
            raise ValueError("invalid memory range")
        # RAM/ROM direct reads avoid destructive memory-mapped I/O reads.
        result = []
        for addr in range(address, address + count):
            if addr < 0x8000:
                result.append(self.machine.ram.data[addr])
            elif addr >= 0xE000:
                result.append(self.machine.rom.data[addr - 0xE000])
            else:
                result.append(None)
        return {"address": address, "bytes": result, "note": "I/O and unmapped addresses are not read"}

    def poke(self, address, value):
        if not 0 <= address < 0x8000 or not 0 <= value <= 255:
            raise ValueError("only RAM bytes can be modified")
        self.machine.ram.data[address] = value
        return {"address": address, "value": value}


def parse_image(filename, content, load_address=None):
    """Parse raw BIN or Commodore-style PRG; no ROM or disk auto-execution."""
    suffix = filename.lower().rsplit(".", 1)[-1]
    if suffix == "prg":
        if len(content) < 3:
            raise ValueError("PRG needs a two-byte load address and payload")
        address = int.from_bytes(content[:2], "little")
        payload = content[2:]
    elif suffix == "bin":
        if load_address is None:
            raise ValueError("raw BIN requires explicit load address")
        address, payload = load_address, content
    else:
        raise ValueError("image format not executable: supported .bin and .prg")
    if not payload or not 0 <= address < 0x8000 or address + len(payload) > 0x8000:
        raise ValueError("program must fit in 32 KiB RAM")
    return address, payload
