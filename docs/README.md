# USM-Ultra — Dokumentationsindex

Stand: 2026-11-06. **Virtual-First** ist die verbindliche Architektur: vollständige Software-Nutzung soll unabhängig von Hardware möglich sein. Hybrid und Physical sind noch nicht verfügbar.

## Einstieg und Betrieb

- [Projektübersicht und Quickstart](../README.md)
- [Tatsächlicher Implementierungsstatus](../STATUS.md)
- [Priorisierte offene Aufgaben](../TODO.md)
- [Roadmap](../ROADMAP.md)
- [Entwicklung und Tests](DEVELOPMENT.md)
- [Sicherheit](../SECURITY.md) · [Lizenz](../LICENSE) · [Drittanbieterhinweise](../NOTICE.md)

## USM-6502 — erster virtueller Computer

- [Maschinenarchitektur und Boot-ROM](USM_6502.md)
- [Interaktiver Monitor, Breakpoints, BIN/PRG-Image-Loader](MONITOR_6502.md)
- [UART, Timer, GPIO und Speicherkarte](PERIPHERALS_6502.md)
- [BASIC-Konsole: Python-Fallback und native 6502-Portierung](BASIC_6502.md)
- [Getrennte Arbeitsbereiche und Snapshots](MACHINE_WORKSPACES.md)
- [MOS 6502: Geschichte, Technik, Referenzprojekte und historische Maschinen](MOS_6502_REFERENCE.md)
- [ROM- und Image-Datenschutz](ROM_POLICY.md)

## MasterVisor und APIs

- [Frontend, Modulnavigation und Bedienung](MASTER_VISOR.md)
- [Einstellungen und Konfiguration](SETTINGS.md)
- [Chip- und Modul-Katalog](CHIP_CATALOG.md)
- [OpenAPI-Schema zur Laufzeit](http://127.0.0.1:8000/openapi.json) — nur bei lokal laufendem Server

## Systemarchitektur und Forschung

- [Architektur](ARCHITECTURE.md)
- [USP-Spezifikation](USP_SPEC.md)
- [Virtual-First- und Hybrid-Vertrag](VIRTUAL_FIRST.md)
- [Betriebsmodi und Zeitklassen](MODES_AND_TIMING.md)
- [Musashi-Integrationsplan](MUSASHI_INTEGRATION.md)
- [V0.2-Code-Review](CODE_REVIEW_V02.md)
- [Wissenschaftliche V7-Studie: Kapitelübersicht](STUDIE_V7.md)

Die vollständige bebilderte V7-DOCX ist **noch nicht** Bestandteil des GitHub-Repositories. Die Markdown-Datei ist kein vollständiger Ersatz. Weder die Studie noch die Projektbeschreibungen sind ein Nachweis für physische FPGA-Funktion, elektrische Sicherheit oder Zyklusgenauigkeit.

## Revisionsregel

Jede Änderung an CPU-/Peripherie-Registern, Adressraum, Image-Format, Snapshots, Backend-Schnittstellen oder Zeitklassen muss in der zugehörigen Spezifikation und den Tests nachgezogen werden. Referenzierte externe Repositories sind nicht automatisch als Quellcode integriert.
