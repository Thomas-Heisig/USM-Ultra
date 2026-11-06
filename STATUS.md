# Implementation status

**Date:** 2026-11-06  
**Stage:** Experimental v0.2 / v0.3 preparation  
**Principle:** The final system must work without physical hardware. Optional hardware may be selected only when verified.

| Area | Current state | Next gate |
| --- | --- | --- |
| USP transaction matrix | Functional prototype | Typed errors, timing-class contract |
| RAM / ROM window model | Functional prototype | Staged commit, register map |
| WIN_GENERATION | Implemented in WindowManager | Concurrent transaction consistency |
| Task queue | Lock-based unique claim | Explicit fairness contract |
| Lease timeout | Injectable clock | Unified trace timestamp clock |
| Bus trace | In-memory ring, 4096 entries | Configurable 65536 and export |
| MC68000 | Minimal opcode smoke-test | Musashi C shim and ctypes |
| Z80 | Bus-master stub | Native/Python ISA backend |
| Other CPU families | Catalog placeholders | Backend implementation |
| SID | Register stub | Correct 6581/8580 audio model |
| Amiga custom chips | Catalog placeholders | Chip RAM/DMA/video/audio |
| Atari ST chipset | Catalog placeholders | TOS boot profile |
| Recovery hardware | Planned | Virtual imaging and capture interface |
| Physical FPGA / chips | Not connected | Hardware discovery and capability checks |
| MasterVisor | Local FastAPI dashboard | Catalog UI, config and diagnostics |
| V7 research | Chapter guide in Git | Full DOCX upload and editorial corrections |

## Meaning of availability

- **Emulated**: a software model is implemented for its stated scope, not necessarily a complete historical machine.
- **Stub**: limited contract/register/bus placeholder; not a functional chip emulator.
- **Not implemented**: planned and cataloged, but cannot execute.
- **Hardware not probed**: there is no implemented physical detection mechanism; it is **not** proof a device is physically absent.
- **Hardware not present**: only after an actual successful detection scan confirms absence.

## Non-goals of current version

Full Amiga/TOS boot, cycle-exact timing, FPGA execution, seamless migration of physical chip state, full ROM management, and remote unauthenticated access.

## MasterVisor-Einstellungen (neu)

- GET/PUT /api/settings: validierte lokale JSON-Konfiguration, atomar gespeichert
- GET /api/capabilities: Feature-Verfügbarkeit
- GET /api/docs-index: Dokumentationsverweise
- MasterVisor: Einstellungen und Dokumentation eingebunden
- Nur virtual ist aktivierbar; hybrid/physical bleiben bewusst gesperrt
- CI-Ergebnis der neuen Endpunkte noch zu bestätigen
