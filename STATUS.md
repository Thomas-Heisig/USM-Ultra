# USM-Ultra — Implementierungsstatus

**Stand:** 2026-11-06. **Status:** Experimenteller Virtual-First-Prototyp; nicht als vollständiger historischer Computer abgenommen.

| Modul | Tatsächlicher Stand | Fehlende Abnahme |
| --- | --- | --- |
| USP Matrix, RAM/ROM, Windows | Funktionaler Python-Prototyp | Timing, typisierte Fehler, HIL |
| Task Queue/Leases | Lock-basiert, FakeClock | Fairness-/Lastnachweis |
| 68000 | Minimaler Testkern | Musashi C-Shim und CPU-Tests |
| Z80 und weitere CPUs | Stubs/Katalog | Ausführbare Backends |
| USM-6502 CPU | Optional py65, RAM/ROM und Bus | CPU-/Interrupt-/Timing-Abdeckung |
| USM-6502 Peripherie | Virtuelle UART RX/TX, Timer, GPIO | IRQ, Gerätekompatibilität |
| 6502 Loader/Monitor | BIN/PRG, Reset, Step, Run-Limit, Breakpoints, Memory | E2E, Debugger/Disassembler |
| 6502 Startprogramm | Eigener 6502-Code mit UART-Ausgabe | CI-/E2E-Nachweis |
| BASIC-Konsole | Python-Host-Fallback mit Programmzeilen | **Natives 6502-BASIC fehlt** |
| Arbeitsbereiche/Snapshots | Lokale Softwareablage und CPU/RAM/Peripheriezustand | Vollständige atomare Sicherung |
| Apple I/II, C64, Atari, NES | Referenz-/Systemkatalog | Vollständige Emulation fehlt |
| MasterVisor | FastAPI + Browserseiten für Module, Monitor und BASIC | Browser-E2E und Sicherheit |
| Echte CPU/FPGA/Peripherie | Keine Treiber, keine geprüfte Erkennung | Hardware-Backend und Validierung |
| V7-Studie | Markdown-Übersicht im Repo | Vollständige illustrierte DOCX fehlt |

## In diesem Änderungsstand erledigt

- Mehrere Dateien im Software-Arbeitsbereich werden stabil nach Dateinamen sortiert.
- BASIC-Fallback unterstützt nun auch `/` als ganzzahlige Division.
- GitHub Actions installiert Web- und py65-Testabhängigkeiten; vorher konnten optionale CPU-Tests übersprungen werden.
- README, Dokumentationsindex und TODO-Liste mit tatsächlichem Implementierungsstand abgeglichen.

**Testhinweis:** Die CI-Konfiguration ist aktualisiert, aber die grünen Testläufe wurden hier noch nicht geprüft. Eine erfolgreiche End-to-End-Abnahme wird ausdrücklich nicht behauptet.

## Betriebsprinzip

Software-only ist Standard und muss dauerhaft funktionsfähig bleiben. Hybrid/Physical werden erst nach Implementierung, Erkennung, Sicherheits- und Äquivalenzprüfung freigeschaltet. ROMs und Original-Images bleiben lokal. Das Backend `py65` ist eine optionale Abhängigkeit, kein FPGA-/Hardware-Ersatz mit nachgewiesener Zyklusgenauigkeit.

Weiteres: [TODO](TODO.md), [BASIC](docs/BASIC_6502.md), [6502-Monitor](docs/MONITOR_6502.md), [V7-Studie](docs/STUDIE_V7.md).
