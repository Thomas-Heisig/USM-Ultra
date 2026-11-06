# First executable 6502 program and BASIC integration plan

## Available now

The MasterVisor Machines panel has a **6502-Startprogramm ausführen** action. It loads a self-authored, redistributable 6502 binary into USM-6502 RAM at $0200, runs a bounded number of CPU instructions through py65 and sends the message `USM 6502 READY` to the virtual serial TX register at $8000. Endpoint: `POST /api/machines/usm-6502/starter`.

This is an executable assembly program, **not BASIC**. Execution and CI have not yet been independently confirmed on a deployed machine.

## BASIC candidates (not integrated)

- [CorshamTech 6502 Tiny BASIC](https://github.com/CorshamTech/6502-Tiny-BASIC): GPLv3; its README documents 16-bit integer BASIC, RAM $0200–$13FF and xKIM dependency for optional SD functions. Integration requires adapting console input/output, build, memory map and licensing.
- [Klaus 6502 EhBASIC V2.22](https://github.com/Klaus2m5/6502_EhBASIC_V2.22): historical Enhanced BASIC source reference; verify license and build/link requirements before copying.
- [cc65](https://github.com/cc65/cc65): external assembler/compiler/linker; useful to build a USM-specific BASIC adaptation.

**Do not vendor all upstream repositories indiscriminately.** MiSTer HDL cores, CPU simulators and complete machine projects have different build targets and licensing obligations. The project should use pinned upstream revisions and explicit adapters. Proprietary Apple/Commodore ROM images remain private.

## BASIC acceptance criteria

1. Select a BASIC implementation with a compatible license and documented source provenance.
2. Build a reproducible 6502 binary in CI without proprietary ROMs.
3. Adapt getchar/putchar to USM serial DATA ($8000), STATUS ($8001).
4. Run a program entered through MasterVisor, e.g. `10 PRINT 2+3`, `RUN`, and verify the output `5`.
5. Save/restore BASIC interpreter state including RAM, CPU, UART RX/TX and relevant peripheral state.
6. Keep software emulation fully usable with no physical hardware.
7. Provide optional FPGA/real-CPU adapters only after separate electrical and timing validation.

## Known limits

A full Apple I/II, Commodore or NES computer is not provided by the USM-6502 SBC. Their firmware, memory mapping, video/audio, storage and peripheral controllers require independent machine-specific integration.
