# Machine workspaces and snapshots

Each machine profile gets a **separate local directory** under `~/.usm-ultra/machines/<machine-id>/`. Override the base path with `USM_MACHINE_HOME`. Files and snapshots are never automatically committed to GitHub.

```text
~/.usm-ultra/machines/
  usm-6502/
    software/     # .bin, .prg, .rom uploaded from MasterVisor
    roms/         # local ROM library (not uploaded)
    media/        # future disk and cassette images
    snapshots/    # state1.json, ...
  another-cpu/
    software/
    roms/
    media/
    snapshots/
```

## Current 6502 snapshot format

Version 1 stores CPU registers (PC, SP, A, X, Y, P), 32 KiB RAM, UART output, logical matrix tick, backend ID and ROM/RAM SHA-256. Saves use atomic replacement and restores reject a different ROM or malformed register ranges. Restore creates a fresh CPU machine in the web API before replacing the active session.

MasterVisor's Machines page can upload a program file to the private software directory, list it, save the active machine and restore a saved state. **Uploading a program does not execute it yet.** Loading arbitrary programs into the address space and stepping/debugging are separate milestones.

## API

- `GET /api/machines/usm-6502/workspace`
- `POST /api/machines/usm-6502/software` with `{"name":"demo.bin","hex_data":"a900"}`
- `POST /api/machines/usm-6502/snapshots` with `{"name":"checkpoint1"}`
- `POST /api/machines/usm-6502/snapshots/{name}/restore`

The initial 6502 emulator is optional: `pip install -e ".[6502,web,test]"`. This does not prove the package is installed on any user's computer.

## Hardware compatibility

Snapshots are **software-backend specific**. Physical-chip state cannot be restored until the bridge supports safe register capture/restore, memory coherence, peripheral quiescence and compatible timing. Do not assume py65 state can be loaded directly into a real 6502.

## Remaining work

- Per-instance machine IDs (multiple 6502 instances) and runtime lifecycle management
- Program load address, binary loader, debugger and breakpoints
- Complete peripheral state and IRQ/NMI, clocks, timers, serial input
- Snapshot schema migrations, integrity of entire snapshot, backup/retention and file-size quotas
- Consistent multi-CPU/multi-peripheral atomic snapshots
- Hardware-backed snapshot protocol and equivalence tests
- Authentication and safe remote access
