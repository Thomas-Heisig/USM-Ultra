"""Declarative hardware/software catalog; planned does not imply implemented."""
from dataclasses import dataclass, asdict
from enum import Enum

class Implementation(str, Enum):
    EMULATED = "emulated"
    STUB = "stub"
    NOT_IMPLEMENTED = "not_implemented"

class Hardware(str, Enum):
    PRESENT = "present"
    NOT_PRESENT = "not_present"
    NOT_PROBED = "not_probed"

@dataclass(frozen=True)
class Component:
    id: str
    name: str
    family: str
    role: str
    implementation: Implementation = Implementation.NOT_IMPLEMENTED
    hardware: Hardware = Hardware.NOT_PROBED
    notes: str = ""
    dependencies: tuple[str, ...] = ()
    def payload(self):
        result = asdict(self)
        result["dependencies"] = list(self.dependencies)
        result["available_virtual"] = self.implementation == Implementation.EMULATED
        result["available_hardware"] = self.hardware == Hardware.PRESENT
        return result

# These are engineering placeholders, not a statement of hardware detection.
_COMPONENTS = (
    Component("m68000", "Motorola MC68000", "CPU", "16/32-bit CISC CPU", Implementation.STUB, notes="Bus master and tiny instruction smoke-test; Musashi not integrated"),
    Component("m68010", "Motorola MC68010", "CPU", "68k CPU"),
    Component("m68020", "Motorola MC68020", "CPU", "32-bit 68k CPU"),
    Component("m68030", "Motorola MC68030", "CPU", "MMU 68k CPU"),
    Component("m68040", "Motorola MC68040", "CPU", "68k CPU with FPU"),
    Component("m68060", "Motorola MC68060", "CPU", "68k CPU"),
    Component("i8086", "Intel 8086", "CPU", "16-bit x86 CPU"),
    Component("i8088", "Intel 8088", "CPU", "8-bit external x86 CPU"),
    Component("i80286", "Intel 80286", "CPU", "Protected-mode x86 CPU"),
    Component("z80", "Zilog Z80", "CPU", "8-bit CPU", Implementation.STUB, notes="Bus master stub only"),
    Component("mos6502", "MOS 6502", "CPU", "8-bit CPU", Implementation.EMULATED, notes="Optional py65 backend; USM-6502 SBC partial, not full historical machine"),
    Component("mos6510", "MOS 6510", "CPU", "C64 CPU"),
    Component("w65c02", "WDC 65C02", "CPU", "CMOS 6502"),
    Component("sid6581", "MOS SID 6581", "Audio", "C64 sound chip", Implementation.STUB, notes="32-byte register stub, no audio"),
    Component("sid8580", "MOS SID 8580", "Audio", "C64 sound chip"),
    Component("paula", "Amiga Paula", "Audio", "Audio, disk and I/O DMA", dependencies=("agnus",)),
    Component("agnus", "Amiga Agnus", "Video/DMA", "DMA, blitter and chip RAM control"),
    Component("denise", "Amiga Denise", "Video", "Display pipeline", dependencies=("agnus",)),
    Component("alice", "Amiga Alice", "Video/DMA", "AGA DMA controller"),
    Component("lisa", "Amiga Lisa", "Video", "AGA display chip", dependencies=("alice",)),
    Component("gary", "Amiga Gary", "System", "Bus control and decoding"),
    Component("cia8520a", "MOS 8520 CIA A", "I/O", "Amiga timers, ports, interrupts"),
    Component("cia8520b", "MOS 8520 CIA B", "I/O", "Amiga timers, ports, interrupts"),
    Component("vicii", "MOS VIC-II", "Video", "C64 video controller"),
    Component("cia6526a", "MOS 6526 CIA A", "I/O", "C64 I/O and timers"),
    Component("cia6526b", "MOS 6526 CIA B", "I/O", "C64 I/O and timers"),
    Component("ym2149", "Yamaha YM2149", "Audio", "Atari ST PSG"),
    Component("ay38910", "GI AY-3-8910", "Audio", "Programmable sound generator"),
    Component("shifter", "Atari ST Shifter", "Video", "Display controller"),
    Component("glue", "Atari ST GLUE", "System", "Timing and bus control"),
    Component("mmu_st", "Atari ST MMU", "Memory", "ST memory controller"),
    Component("wd1772", "WD1772", "Storage", "Floppy controller"),
    Component("mfp68901", "Motorola MC68901", "I/O", "Multi-function peripheral"),
    Component("acia6850", "Motorola MC6850", "I/O", "Serial interface"),
    Component("ram", "Virtual RAM", "Memory", "Byte-addressable RAM", Implementation.EMULATED, notes="Working RAM model"),
    Component("rom", "Virtual ROM", "Memory", "Read-only memory", Implementation.EMULATED, notes="Memory protection model; local ROM loader pending"),
    Component("usp", "USP Matrix", "Infrastructure", "Virtual bus and memory windows", Implementation.EMULATED),
    Component("task_queue", "Task Queue", "Infrastructure", "Lock-protected task claims", Implementation.EMULATED),
    Component("fpga_bridge", "FPGA Bus Bridge", "Hardware", "Future physical bridge"),
    Component("recovery_flux", "Flux Capture", "Recovery", "Read-data timestamp capture"),
    Component("recovery_analog", "Analog Capture AFE", "Recovery", "Raw head analog acquisition"),
    Component("ethernet_bridge", "Ethernet Bridge", "Hardware", "Future hardware transport"),
    Component("usb_bridge", "USB Bridge", "Hardware", "Future hardware transport"),
)

def components(family=None):
    items = _COMPONENTS
    if family:
        items = tuple(c for c in items if c.family.lower() == family.lower())
    return [c.payload() for c in items]

def component(component_id):
    return next((c.payload() for c in _COMPONENTS if c.id == component_id), None)

def summary():
    items = components()
    return {
        "total": len(items),
        "emulated": sum(c["implementation"] == "emulated" for c in items),
        "stub": sum(c["implementation"] == "stub" for c in items),
        "not_implemented": sum(c["implementation"] == "not_implemented" for c in items),
        "hardware_present": sum(c["hardware"] == "present" for c in items),
        "hardware_probe_available": False,
    }
