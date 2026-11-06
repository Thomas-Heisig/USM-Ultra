# USM-Ultra — Entwicklungsaufgaben

Stand: 2026-11-06. Statusangaben beruhen auf Repository-Inspektion; CI-Ergebnisse wurden in dieser Sitzung nicht bestätigt.

## P0 — Korrektheit und Verifikation

- [x] Software-Arbeitsbereich: Sortierung mehrerer Programmdateien korrigiert.
- [x] BASIC-Fallback: `/` als ganzzahlige Division unterstützt.
- [x] CI: optionale Web- und py65-Abhängigkeiten für Tests installiert.
- [ ] CI-Läufe auf Python 3.11–3.13 prüfen und Fehler beheben.
- [ ] E2E-Test: MasterVisor öffnen, 6502-Startprogramm ausführen, `USM 6502 READY` nachweisen.
- [ ] E2E-Test: BASIC-Fallback `10 PRINT 2+3`, `RUN` ergibt `5`.
- [ ] API-/UI-Konsistenz, Testisolierung und Statuscodes vollständig prüfen.
- [ ] Snapshot-Integrität, Größenlimits, vollständige Peripheriezustände und atomare Wiederherstellung absichern.

## P1 — Native BASIC-Integration

- [ ] Lizenz und reproduzierbaren Upstream-Commit von Tiny BASIC/EhBASIC prüfen.
- [ ] cc65 bzw. passenden Assembler in den Build integrieren.
- [ ] Zeichen-Ein-/Ausgabe an USM-6502 UART anpassen.
- [ ] BASIC als **6502-Maschinencode** ausführen, nicht als Python-Host-Fallback.
- [ ] Native BASIC-Integrationstest `10 PRINT 2+3` → `5` nachweisen.
- [ ] BASIC-Zustand mit CPU, RAM und Peripherie persistieren.

## P1 — Images und vollständiges erstes System

- [x] BIN/PRG-RAM-Lader und begrenzter Monitor mit Breakpoints.
- [x] Virtuelle serielle Schnittstelle, Timer und GPIO als vereinfachte USM-Geräte.
- [ ] Interaktive Terminal-Sitzung, asynchroner Lauf/Pause und Disassembler.
- [ ] ROM-Auswahl, private ROM-Identität und reproduzierbarer Boot.
- [ ] Disketten-/Tape-Images mit passenden Controllern und Copy-on-Write.
- [ ] IRQ/NMI, echte CPU-Zykluszählung und genauere Peripherie.
- [ ] Ein historisches Maschinenprofil (zuerst Apple I) vollständig und ROM-rechtlich sauber booten.

## P2 — Architektur und Hardware

- [ ] Hardware-Backend implementieren und elektrisch validieren.
- [ ] Virtuelles Backend muss ohne Hardware voll funktionsfähig bleiben.
- [ ] Musashi C-Shim/ctypes für m68k, später Z80 und weitere CPUs.
- [ ] Zeitklassen T0/T1/T2, typed USP faults, Trace-Export.
- [ ] Vollständige V7-Studie und grafische Anlagen ins Repo übernehmen; redaktionelle Korrekturen prüfen.

## Projektpflege

- [x] README und STATUS auf implementierte Funktionen und Grenzen abgeglichen.
- [x] Dokumentationsindex und neue TODO-Liste.
- [ ] Release-Tags, reproduzierbare Dependency-Locks, SBOM, Sicherheitsreview.
- [ ] Drittanbieter-Lizenzprüfung vor Vendor-Import, keine Original-ROMs im Git.
