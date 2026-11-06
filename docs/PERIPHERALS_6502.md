# USM-6502: Loader und virtuelle Peripherie

## Implementierte Softwarebausteine

- **6502 CPU:** py65, Instruktionsausführung in RAM und ROM; keine physische Hardware.
- **Programmloader:** lokale Binärdateien aus dem Maschinen-Arbeitsbereich nach RAM laden, PC auf Ladeadresse setzen, begrenzte Anzahl Instruktionen ausführen.
- **Serielle Schnittstelle:** DATA und STATUS, virtuelle RX-Queue und TX-Ausgabe; keine vollständige 6551-ACIA-Emulation.
- **Timer:** 16-Bit-Periodenregister, Aktivierung und Pending-Flag; zählt emulierte Instruktionsschritte, nicht echte CPU-Zyklen. Noch keine IRQ-Leitung.
- **GPIO:** 8-Bit Daten, Richtung und virtuelle Eingänge.
- **Snapshots:** RAM, CPU-Register, serielle RX/TX-Daten, Timer und GPIO werden gespeichert.
- **MasterVisor:** Laden, CPU-Schritte, serielle Eingabe, GPIO-Eingänge, Peripheriestatus und Snapshots.

## Speicherkarte

| Adresse | Register |
| --- | --- |
| 0000–7FFF | 32 KiB RAM |
| 8000 | Serial DATA (lesen RX, schreiben TX) |
| 8001 | Serial STATUS (Bit 0 RX ready, Bit 1 TX ready) |
| 8010 | Timer period low |
| 8011 | Timer period high |
| 8012 | Timer control bit 0 enable |
| 8013 | Timer pending bit 0; write 1 to clear |
| 8020 | GPIO data |
| 8021 | GPIO direction |
| E000–FFFF | 8 KiB Boot-ROM |

All I/O register definitions are USM project-specific, **not** cycle-accurate representations of 6522 VIA, 6551 ACIA or another historic peripheral.

## Beispielprogramm

Upload as `hello.bin`, load at `0x0200`, then execute three steps:

```text
A9 41       LDA #$41
8D 00 80    STA $8000
4C 05 02    JMP $0205
```

Expected serial output: `A`.

## Physische Peripherie

A common `DeviceBackend` contract defines read, write, snapshot and restore. No physical driver is implemented. Do not connect 5V hardware directly to FPGA I/O. Future adapters need level shifting, bus arbitration, clock domain handling, safe disconnect, IRQ/NMI wiring and electrical validation.

## Not yet a complete historical machine

Outstanding: true serial device compatibility, accurate clock/cycle model, timer IRQ, GPIO edge interrupts, terminal monitor with command parser, assembler/disassembler, breakpoints, ROM selection and tests on physical chips. Uploaded software can be loaded and executed, but not all 6502 programs will run correctly on this minimal custom SBC. CI and browser E2E results remain to be confirmed.
