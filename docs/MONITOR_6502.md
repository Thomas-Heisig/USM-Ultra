# USM-6502 interaktiver Monitor und Image-Loader

## Bedienung

Im MasterVisor unter **Maschinen**:

1. Programmdatei auswählen und über **Programm lokal ablegen** speichern.
2. Bei `.bin` die RAM-Ladeadresse eingeben, bei `.prg` wird die Adresse aus den ersten beiden Bytes gelesen.
3. **Ausgewähltes Image laden** lädt das Programm in den RAM und setzt den Programmzähler.
4. **Einzelschritt** oder **Bis Breakpoint / Limit ausführen** startet eine begrenzte Ausführung.
5. Breakpoints setzen/entfernen, RAM lesen oder einzelne RAM-Bytes ändern.
6. Speicherabbild sichern und später wiederherstellen.

Der Monitor führt Befehle synchron und mit festem Instruktionslimit aus; er ist kein dauerhaft laufender asynchroner Prozess. Das Stoppen erfolgt am Breakpoint oder nach Erreichen des Budgets. Kein Hintergrund-Run/Pause, keine Disassemblierung.

## Unterstützte Image-Formate

| Format | Funktion |
| --- | --- |
| BIN | Rohes 6502-Maschinenprogramm mit expliziter RAM-Ladeadresse |
| PRG | Commodore-typischer zweibyteiger Little-Endian-Ladeadressheader; Programmbytes werden in den USM-RAM geladen |
| ROM | Private Ablage möglich, aber kein automatischer ROM-Austausch oder Boot |
| D64/DSK/IMG | Noch kein Dateisystem, Diskettencontroller oder Image-Mount |

**Wichtig:** Ein PRG kann Commodore-KERNAL-/BASIC-/VIC-II-/CIA-Funktionen benötigen und ist dadurch nicht automatisch auf dem USM-6502 lauffähig. Ebenso sind Apple II, Atari 8-bit, NES, BBC Micro und C64 eigenständige vollständige Systeme mit zusätzlichen Chips, ROMs, Speicherplänen und Peripherie. Sie sind hier **nicht** vollständig emuliert.

## API

- `GET /api/machines/usm-6502/monitor`
- `POST /api/machines/usm-6502/monitor/reset`
- `POST /api/machines/usm-6502/monitor/run` — `{"count":1000}`
- `POST /api/machines/usm-6502/monitor/step` — `{"count":1}`
- `POST /api/machines/usm-6502/monitor/breakpoints` — `{"address":512,"enabled":true}`
- `GET /api/machines/usm-6502/monitor/memory?address=512&count=64`
- `POST /api/machines/usm-6502/monitor/memory` — `{"address":512,"value":234}`
- `POST /api/machines/usm-6502/images/load` — `{"name":"demo.prg","start":true}`

## Virtual-first und Hardware

Die CPU ist py65-basiert; der Bus und die Registerperipherie sind virtuell. Ein physischer 6502 oder reale ACIA/VIA/GPIO benötigt später ein eigenständiges Bridge-Backend mit Pegelanpassung, Timing, Synchronisierung und Tests. Der Monitor und die Dateiverwaltung sollen dann unabhängig vom Backend bleiben.

## Offene Punkte

Komplette 6502-Computerprofile, Disketten-Images, Datei-/Blockgeräte, IRQ/NMI, Audio/Video, Tastaturmatrix, Hardware-Backends, Disassembler, Quelltextassembler, präzise Taktsimulation und Snapshot-Transaktionssicherheit. Tests sind eingecheckt, aber noch nicht als CI-grün bestätigt.
