# MOS Technology 6502 — technische Referenz und Integrationsplan

Stand: 2026-11-06. Externe Projekte sind **Referenzen**, sofern nicht ausdrücklich als integriert markiert. Die Lizenz jeder konkreten Revision muss vor Übernahme geprüft werden.

## Historische und technische Grundlagen

Der MOS Technology 6502 wurde 1975 vorgestellt und war mit einem anfänglichen Angebotspreis von rund 25 USD ein wichtiger Treiber preisgünstiger Mikrocomputer. Er ist ein 8-Bit-Prozessor mit 16-Bit-Adressraum (64 KiB **Adressraum**, nicht zwangsläufig 64 KiB physischem RAM). Typische frühe Systeme arbeiteten im Bereich von etwa 1–2 MHz; Frequenz und Buszyklen hängen von der Variante und der konkreten Maschine ab. Vergleiche mit Intel 8080 oder Motorola 6800 sind workload- und systemabhängig, kein allgemeiner 1:4-Leistungsfaktor.

Programmiermodell: A, X, Y (8 Bit), P/Status (8 Bit), SP (8 Bit, Stack auf $0100–$01FF), PC (16 Bit). Die Zero Page $0000–$00FF erlaubt kompakte und häufig schnellere Adressierungsarten, ist aber kein Satz echter CPU-Register. Der NMOS-6502 besitzt IRQ, NMI und RESET; Dezimalmodus, undokumentierte Opcodes und Varianten wie 65C02, 6510 oder Ricoh 2A03 sind getrennt zu testen. Little-Endian-Datenformat für 16-Bit-Werte. Die CPU besitzt einen 16-Bit-Adressbus und einen 8-Bit-Datenbus.

## Referenz-Repositories

| Rolle | Projekt | Repository | Status in USM |
| --- | --- | --- | --- |
| Python CPU/Monitor | py65 | https://github.com/mnaberez/py65 | Als optionales Backend im USM-6502 benutzt |
| Verilog CPU | Arlet 6502 | https://github.com/anders-code/arlet-6502 | Referenz für zukünftigen FPGA-Core; nicht integriert |
| Apple II FPGA | MiSTer Apple II | https://github.com/MiSTer-devel/Apple-II_MiSTer | Referenz; nicht integriert |
| C64 FPGA | MiSTer C64 | https://github.com/MiSTer-devel/C64_MiSTer | Referenz; nicht integriert |
| C-Compiler/Assembler/Linker | cc65 | https://github.com/cc65/cc65 | Externes Tool, noch nicht in USM-Build integriert |
| Transistor-Simulation | Visual6502 | https://github.com/trebonian/visual6502 | Wissenschaftliche Referenz, kein Echtzeit-Backend |

Weitere Recherche: https://visual6502.org/ und https://www.cc65.org/ . Lizenz, Provenienz und unterstützte CPU-Varianten sind vor einem Vendor-Import zu prüfen. Keine unkontrollierte Kopie fremder Quellen oder Vermischung inkompatibler Lizenzen.

## Historische Maschinenprofile

| Maschine | CPU-Familie | Zusätzlich erforderliche Emulation | Status |
| --- | --- | --- | --- |
| Apple I | 6502 | PIA/Terminal, Monitor-ROM, Speicherkarte | Nicht implementiert |
| Apple II / IIe | 6502 / 65C02 je Modell | Video, Tastatur, Slots, Disk II, Monitor/BASIC-ROMs | Nicht implementiert |
| Commodore PET | 6502 | PIA/VIA, Video, Tastatur, BASIC/KERNAL | Nicht implementiert |
| Commodore VIC-20 | 6502 | VIC, VIA, BASIC/KERNAL, Sound | Nicht implementiert |
| Commodore 64 | 6510 | VIC-II, SID, CIA, PLA, BASIC/KERNAL/Character-ROM | Nicht implementiert |
| Atari 400/800 | 6502 | ANTIC, GTIA, POKEY, OS-ROM, SIO | Nicht implementiert |
| BBC Micro | 6502 | 6522 VIA, CRTC, Video, Keyboard, MOS/DFS | Nicht implementiert |
| Atari 2600 | 6507 | TIA, RIOT, Cartridge-Banking | Nicht implementiert |
| NES | Ricoh 2A03/2A07 | PPU, APU, Cartridge Mapper, Controller | Nicht implementiert |
| USM-6502 SBC | 6502 (py65) | USM UART, GPIO, Timer, RAM/ROM | Teilimplementiert; kein historischer Komplettcomputer |

**Wichtig:** Ein Apple II oder Apple I benötigt nicht nur CPU und Speicher. Die Peripherie, Firmware und die jeweils richtige Speicherkarte sind Voraussetzung für einen kompatiblen Start.

## Original-ROMs und Software-Images

Nützliche Rechercheorte:
- https://archive.org/ — historische Medien; Rechte und Herkunft je Eintrag prüfen
- https://www.tosecdev.org/ — Katalogisierung/Benennung historischer Software, **keine pauschale Nutzungslizenz**
- https://github.com/search?q=Apple+II+ROM&type=repositories — ROM-Quellen nur nach Provenienz- und Rechteprüfung auswählen
- Apple-I-BASIC, KIM-1-Monitor und OS-65D: historisch dokumentierte Software; keine automatische Freigabe zum Weiterverteilen

Original-ROMs, Diskettenabbilder und private ROM-Fingerprints werden **nicht** ins USM-GitHub-Repository eingecheckt. Private Dateien verbleiben in den jeweiligen Maschinen-Arbeitsbereichen. Das bloße öffentliche Auffinden eines ROMs bedeutet nicht, dass eine Weiterverteilung oder kommerzielle Nutzung erlaubt ist.

### Image-Formate und Systemzuordnung

- `.bin`: rohe Binärdaten, explizite Ladeadresse und CPU/Systemprofil nötig
- `.prg`: meist zweibyteige Ladeadresse, kann Commodore-Systemaufrufe benötigen
- `.rom`: Firmware/Cartridge; Mapping, Banking und Systemprofil nötig
- `.d64`: Commodore-Diskettenabbild, braucht Laufwerk-/IEC-/DOS-Emulation
- `.dsk`: mehrdeutig; Format und System müssen explizit erkannt werden
- `.woz`: Apple-II-Floppy-Abbild mit Flux-/Timinginformationen; benötigt passenden Disk-II-Controller

## Virtual-First / Hybrid

Virtual mode muss dauerhaft ohne Hardware funktionieren. Ein späterer physischer 6502 darf optional über ein separates Backend zugeschaltet werden. Die funktionale Äquivalenz wird durch dieselben Testprogramme, Register-/Speicherprüfungen, Bus-Trace-Vergleiche und definierte Zeitklassen T0/T1/T2 geprüft. Ein FPGA-Verilog-Core ist **nicht automatisch** ein 1:1-Ersatz für einen physikalischen NMOS-6502: Timing, undokumentierte Befehle und elektrische Signale können abweichen.

## Verifikationsplan

1. Funktionale Opcode-Tests einschließlich Flags, Interrupts, Zero Page, Page Crossings, Stack und Decimal Mode.
2. Referenzvergleich mit py65 und, wo geeignet, Visual6502.
3. Separate Profile für NMOS 6502, 65C02, 6510 und 2A03.
4. Laden echter System-ROMs ausschließlich aus lokal bereitgestellten, rechtmäßig verwendbaren Dateien.
5. Disk-/Tape-/Cartridge-Image-Adapter je Maschine mit schreibgeschütztem Original und Copy-on-Write-Differenzen.
6. Snapshot von CPU, RAM, ROM-Identität, Video, Audio, Interrupt-Controllern, Peripherie und Medienzustand.
7. Gleiche Monitor-/Frontend-Schnittstelle für Software-, FPGA- und physische Backends.
8. CI mit freien Testprogrammen und synthetischen ROMs; proprietäre Originaldateien nicht erforderlich.
