# USM-Ultra Dokumentation

## Wissenschaftliche Ausarbeitung

- [V7.0: wissenschaftliche Systemstudie – Leseausgabe](STUDIE_V7.md)
- Originaldatei: **USM_Ultra_Wissenschaftliche_Studie_V7_System_Matrix_UI.docx** (in der Projektarbeitsumgebung; noch nicht im GitHub-Repository). Die verlinkte Markdown-Datei ist ein Kapitelwegweiser und technischer Auszug, keine vollständige Transkription.
- Die V7-Studie ist eine Konzept- und Spezifikationsgrundlage, **kein Mess- oder Fertigungsnachweis**.

## Implementierung

- [Architektur und Sicherheitsgrenzen](ARCHITECTURE.md)
- [USP und Window-Semantik](USP_SPEC.md)
- [Entwicklungs- und Testablauf](DEVELOPMENT.md)
- [ROM- und Recovery-Datenschutz](ROM_POLICY.md)

## Revisionsregel

Bei Änderungen an Registeradressen, Busverhalten, Timing-Klassen oder Pinbelegungen muss der Bezug zur Studie überprüft und dokumentiert werden. Als TBD gekennzeichnete Werte dürfen nicht als verifiziert übernommen werden.

## Code-Review und V0.3

- [Tatsächlicher V0.2-Implementierungsstand und offene Fehler](CODE_REVIEW_V02.md)
- [Musashi-C-Shim und ctypes-Integrationsplan](MUSASHI_INTEGRATION.md)
- [Erweiterte V0.3-Vertragstests](../tests/test_v03_contracts.py)

## Virtual-first / Hybrid

- [Verbindliche Software-only- und Hybrid-Architektur](VIRTUAL_FIRST.md)
- [Roadmap und Meilensteine](../ROADMAP.md)
- [Backend-Registry-Implementierung](../usm/backends.py)
- [Backend-Fallback-Tests](../tests/test_backends.py)

## Chipkatalog und API

- [Chip- und Komponentenübersicht](CHIP_CATALOG.md)
- [Virtual / Hybrid / Physical und Zeitklassen](MODES_AND_TIMING.md)
- [Aktueller Implementierungsstatus](../STATUS.md)

## MasterVisor Full-Stack

- [Einstellungen, Persistenz und REST-API](SETTINGS.md)
- [MasterVisor Web API](../usm/web.py)
- [API-Einstellungen und Integrationstests](../tests/test_settings_api.py)

## Erste vollständige Zielmaschine in Entwicklung

- [USM-6502: virtueller Einplatinencomputer](USM_6502.md)
- [6502-Maschinenprofil und ROM](../usm/machines/sbc6502.py)
- [6502-Tests](../tests/test_sbc6502.py)

## Bedienoberfläche

- [MasterVisor: vollständige Modulnavigation, API und Bedienung](MASTER_VISOR.md)

- [Maschinen-Arbeitsbereiche, Programme und Speicherabbilder](MACHINE_WORKSPACES.md)

- [MOS Technology 6502: CPU, Quellen, Systeme, Originalsoftware und Lizenzhinweise](MOS_6502_REFERENCE.md)
