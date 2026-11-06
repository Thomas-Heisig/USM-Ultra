# MasterVisor Online – Deployment

Die öffentliche statische MasterVisor-Demo liegt unter `docs/index.html`. GitHub Actions `.github/workflows/pages.yml` veröffentlicht bei Änderungen unter `docs/` automatisch über GitHub Pages.

## Einmalige Aktivierung durch Repository-Administrator

1. GitHub Repository → **Settings → Pages**.
2. Unter **Build and deployment** die Quelle **GitHub Actions** auswählen.
3. Unter **Actions** sicherstellen, dass GitHub Actions ausgeführt werden darf.
4. Workflow **Deploy MasterVisor Online (GitHub Pages)** unter **Actions** manuell starten, falls er nicht automatisch läuft.
5. Den grünen Deploy-Lauf und die angezeigte URL prüfen.

Erwartete Pages-Adresse nach erfolgreicher Aktivierung: https://thomas-heisig.github.io/USM-Ultra/ . Diese URL ist erst nach erfolgreicher Veröffentlichung tatsächlich erreichbar.

## Sicherheitsgrenze

Die GitHub-Pages-Demo ist statisch. Sie enthält eine unabhängige kleine JavaScript-BASIC-Demo, **nicht** den nativen 6502-Emulator. Sie stellt keine schreibenden API-Endpunkte, ROM-Uploads, Snapshots oder Hardwarezugriffe bereit.

Für ein echtes öffentliches MasterVisor mit py65/FastAPI ist ein separater, abgesicherter Backend-Host nötig: Benutzeranmeldung, Berechtigungen, CSRF-/CORS-Strategie, isolierte Arbeitsbereiche, Dateigrößenlimits, Ratenlimits, HTTPS, Logging und persistente Speichermedien. **Den aktuellen lokalen FastAPI-Entwicklungsserver nicht ungeschützt ins Internet stellen.**

## Virtual-First

Softwareemulation bleibt unabhängig von FPGA/physischer Hardware. Spätere reale Geräte werden nur als optionale Backends verwendet. Das Online-Frontend darf bei fehlender Hardware nicht ausfallen.
