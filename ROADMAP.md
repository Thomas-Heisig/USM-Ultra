# USM-Ultra roadmap

## V0.2 – functional baseline
- Python USP-style matrix, memory windows, generation counter, task claims, local ROM hashing
- Initial MasterVisor UI and small 68000 smoke-test interpreter

## V0.3 – full CPU foundation
- Pinned Musashi native backend with ctypes/CFFI
- Typed USP faults and deterministic queue/window contract tests
- Boot ROM mapping and CPU reset vector integration
- Native backend build verification on Windows/Linux

## V0.4 – complete virtual machine profiles
- Atari ST / TOS, Amiga and Z80 profile interfaces
- Video, audio, DMA, interrupt, storage and input subsystems
- Virtual hardware device tree and profile snapshots
- Boot acceptance tests using user-supplied local ROMs

## V0.5 – optional hardware-in-the-loop
- Device discovery and capability negotiation
- Per-slot backend selection and health monitoring
- Quiesce/snapshot/rebind/resume with safe rollback
- Automatic virtual fallback where state migration is technically supported

## V1.0 – standalone and hybrid operation
- Fully functional software-only system
- Hardware acceleration/real-chip coupling optional, not required
- Per-device virtual/native/hardware selection and traceable transitions
- Recovery workflows with write-blocking and provenance

Roadmap items are goals, not completed features or delivery promises.
