# USM-6502 — Architektur, Quellen und Integrationsstand

**Status:** Virtual-First-Referenzmaschine, kein vollständiger Apple-II-/C64-Emulator. Das ausführbare CPU-Backend ist die optionale Python-Abhängigkeit **py65**. Historische Fremd-ROMs sind **nicht** Bestandteil dieses Repositories.

## Verifizierbare Grundlagen

- MOS Technology **MCS6500 Microcomputer Family Programming Manual** (1976), historische Dokumentation, u. a. über [6502.org](http://www.6502.org/documents/books/mcs6500_family_programming_manual.pdf).
- MOS Technology **MCS6500 Microcomputer Family Hardware Manual** (1976), historische Dokumentation; Verfügbarkeit und Scan-Lizenz beim jeweiligen Archiv prüfen.
- [Visual6502](https://www.visual6502.org/) — transistorbasierte Rekonstruktion und interaktive Untersuchung der NMOS-6502-Logik.
- [Visual6502/visual6502](https://github.com/trebonian/visual6502) — Referenz für Transistornetzliste und interne Signale; keine eingebaute Laufzeitabhängigkeit.
- [py65](https://github.com/mnaberez/py65) — **als optionale Dependency integriert**, CPU-Interpreter.
- [cc65](https://github.com/cc65/cc65) — Assembler/Compiler/Linker; **nicht als Dependency oder Build-Werkzeug integriert**.
- [Microsoft BASIC-M6502](https://github.com/microsoft/BASIC-M6502) — historischer BASIC-1.1-Quelltext **mit MIT-Lizenz im Ordner `third_party/microsoft-basic-m6502/` übernommen**; noch nicht für USM assembliert oder ausgeführt.
- [Arlet 6502](https://github.com/anders-code/arlet-6502) — Verilog-FPGA-Core; **nicht integriert**.
- [MiSTer Apple II](https://github.com/MiSTer-devel/Apple-II_MiSTer), [MiSTer C64](https://github.com/MiSTer-devel/C64_MiSTer) — Systemreferenzen, **nicht integriert**.

**Lizenz- und Quellenregel:** Keine ungeprüfte Übernahme fremder ROMs, Firmware, Schaltbild-Scans, Transistornetzlisten oder HDL-Quellen. Bei jeder künftigen Übernahme sind Repository, Revision, Lizenz, Copyright-Notices und Änderungen zu dokumentieren. Die nachstehenden Schaltbilder und Tabellen sind eigene technische Darstellungen.

## CPU-Eigenschaften (NMOS MOS 6502)

| Merkmal | Beschreibung |
|---|---|
| Datenbus | 8 Bit, bidirektional |
| Adressbus | 16 Bit, 64 KiB Adressraum |
| Register | A, X, Y (je 8 Bit); SP (8 Bit); PC (16 Bit); P (Status) |
| Stack | Seite $0100–$01FF |
| Zero Page | $0000–$00FF; verkürzte Adressierung |
| Resetvektor | $FFFC/$FFFD |
| NMI-Vektor | $FFFA/$FFFB |
| IRQ/BRK-Vektor | $FFFE/$FFFF |
| Endianness | Little Endian |
| Interrupts | RESET, NMI (flankengesteuert), IRQ (pegelgesteuert) |
| Statusbits | N V – B D I Z C; B ist kein gewöhnliches physisches Flipflop wie die anderen Statusflags |
| Befehle | Offizieller NMOS-6502-Befehlssatz; undokumentierte Opcodes separat betrachten |

Der 6502 besitzt **kein frei programmierbares Mikrocode-ROM** wie manche anderen CPU-Architekturen. Die Steuerung erfolgt durch festverdrahtete, getaktete Zustands- und Dekodierlogik (PLA und Random Logic). Daher gibt es keine originale, vom Hersteller auslesbare „Microcode.bin“, die seriös eingebunden werden könnte. Eine zyklengenaue Darstellung erfordert eine gesonderte Modellierung der internen Steuersignale, Speicherzyklen und Varianten. Siehe [Mikroarchitektur](MICROARCHITECTURE.md).

## USM-6502 Speicherplan (implementiert)

| Bereich | Größe | Funktion |
|---|---:|---|
| $0000–$7FFF | 32 KiB | RAM |
| $8000–$8001 | 2 Byte | USM SerialPort (kein 6551-ACIA) |
| $8010–$8013 | 4 Byte | USM Timer |
| $8020–$8021 | 2 Byte | USM GPIO |
| $8022–$802F | — | Nicht zugeordnet |
| $8030–$8033 | 4 Byte | Experimenteller 6551-ACIA-Registeradapter (ohne Timing/IRQ) |
| $8034–$DFFF | — | Nicht zugeordnet |
| $E000–$FFFF | 8 KiB | Schreibgeschütztes Monitor-ROM |

Der **Matrix-Konfigurator im Browser ist ein Entwurfswerkzeug**. Er ersetzt nicht die oben implementierte Zuordnung. Konfigurationen werden noch nicht in eine neue lauffähige SBC-Instanz kompiliert.

## Software und Firmware

- `usm/machines/sbc6502.py`: CPU-Adapter, Speicher, Bus und Start-ROM.
- `usm/machines/peripherals.py`: virtuelle serielle Schnittstelle, Timer und GPIO.
- `usm/machines/monitor6502.py`: Debugger/Monitor und Programmlader.
- `usm/machines/basic_console.py`: **Host-Python-BASIC**, kein 6502-BASIC-ROM.
- `firmware/6502/boot.asm`: dokumentierter Original-Quelltext des kleinen USM-Bootprogramms.
- `firmware/6502/build_boot.py`: deterministischer Build des ROM-Images ohne externe Assembler-Abhängigkeit.
- `firmware/6502/README.md`: Build- und ROM-Layout.

## Noch offen

Microsoft-BASIC-Quellportierung und ROM-Build, vollständig emulierte historische Chips (VIC-II, SID, 6522/6551 usw.), DMA, exakte Interrupt- und Taktverdrahtung, vollständige Opcode-/Zyklustests, originale Board-Layouts und reale FPGA-Anbindung. Nicht als abgeschlossen ausweisen, solange keine automatisierten Integrations- und Lizenztests vorliegen.
