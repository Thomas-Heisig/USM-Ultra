# Microsoft BASIC M6502 – Quellintegration

**Upstream:** https://github.com/microsoft/BASIC-M6502  
**Dateien:** [m6502.asm](m6502.asm) und [LICENSE](LICENSE)  
**Lizenz:** MIT; Copyright Microsoft Corporation (1976–1978). Original-Lizenz beibehalten.  
**Quelle:** Microsofts öffentliches, seit September 2025 archiviertes Repository, Branch `main`; übernommener Datei-SHA: `51c07c918deb2c9ff2c13c6c472d1a5826be6a9e` (Git Blob SHA). Lizenz-Blob: `cfb1aba89130ba02027a6d1be0903d658c5592af`.

## Integrationsstatus

**Quellcode übernommen, nicht assembliert, nicht gelinkt, nicht gestartet.**

Das historische BASIC 1.1 ist ein vollständiger 6502-Assembler-Quelltext, aber **kein direkt ausführbares ROM**. Es verwendet zeitgenössische Makros und Direktiven (z. B. `SEARCH M6502`, `IFE`, `IFN`, `RADIX`, `^O`), die ein gewöhnlicher cc65-`ca65`-Assembler nicht unverändert akzeptiert.

Die bedingten Konfigurationen `REALIO=0..4` sind für historische Zielmaschinen (Simulator, KIM-1, OSI, PET, Apple) bestimmt, **nicht** für das USM-6502-SBC. Die USM-Schnittstellen liegen bei `$8000` (UART), `$8010` (Timer), `$8020` (GPIO), `$8030` (experimenteller ACIA-Adapter); diese Adressen müssen für Microsoft BASIC neu angepasst werden.

## Nächste Integrationsstufen

1. Einen reproduzierbaren Assembler-/Konvertierungs-Build mit gepinnter Toolchain herstellen; originale Syntax und bedingte Assemblerzweige prüfen.
2. USM-spezifische Ein-/Ausgabevektoren und RAM/ROM-Layout portieren.
3. Speicherbedarf und Konflikte mit dem Monitor-ROM ($E000–$FFFF) prüfen; bei Bedarf ein neues Bank-/ROM-Layout definieren.
4. Erst nach erfolgreichem Build und Tests ein BASIC-Binärabbild veröffentlichen.
5. Native BASIC-Befehle und I/O mit py65 testen; Host-Python-BASIC bis dahin eindeutig getrennt halten.

Keine nicht verifizierten ROMs oder angeblich lauffähigen BASIC-Binaries bereitstellen.
