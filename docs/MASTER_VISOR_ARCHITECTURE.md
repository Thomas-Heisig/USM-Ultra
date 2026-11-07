# MasterVisor – gemeinsames Maschinen- und Komponentenmodell

Stand: 2026-11-07.

## Datenquellen

- `docs/components.json`: einheitlicher Chipkatalog (47 Einträge).
- `docs/machines.json`: Maschinenkatalog (29 Profile), CPU-Referenzen, Chip-IDs, Firmware-Anforderungen, Medienformate und Bild-/Dokument-Platzhalter.
- `docs/index.html`: gemeinsame Browseransicht und Matrix-Entwurf.
- `usm/catalog.py`: maßgeblicher Python-Komponentenkatalog für das lokale Backend.

**Wichtig:** Die JSON-Kataloge sind derzeit statische Snapshots, keine automatisch aus dem Python-Backend generierten Daten. Eine echte automatische Synchronisierung bei jeder Änderung ist noch zu implementieren.

## Benutzerablauf

1. **Dashboard:** kompakte Übersicht über Maschinen, CPUs, Komponenten und Backend-Status.
2. **Maschinen:** CPU/Hersteller/Status wählen, Suchtext kombinieren, Maschinenbeschreibung und Medienanforderungen öffnen.
3. **In Matrix übernehmen:** CPU und referenzierte Chips aus dem Maschinenprofil in den Entwurf übertragen.
4. **Matrix:** RAM, ROM, Takt und Peripherie verändern, formale Plausibilitätsprüfung, JSON exportieren/importieren.
5. **Speicher:** RAM-/ROM-Werte und CPU aus der Matrix anzeigen.
6. **Task-Queue:** Aufgaben im Browser vormerken, ohne Ausführung vorzutäuschen.
7. **Bus-Trace:** Matrixdiagnose exportieren; kein echter CPU-Trace.
8. **Hardware:** Katalogstatus der virtuellen/physikalischen Implementierungen.
9. **Recovery:** pro Maschine erwartete Dateiformate anzeigen; lokale Dateimetadaten erfassen.
10. **Settings:** Frontend-Darstellung ändern.
11. **Dokumentation:** technische Quellen und Integrationsstand.

## MOS 6502 – ausführbare Referenzmaschine

Das Python-Backend enthält eine teilweise funktionsfähige 6502-SBC mit `py65`, 32 KiB RAM, 8 KiB Boot-ROM, SerialPort, Timer, GPIO und experimentellem 6551-Registermodell.

Installation im Repository:

```bash
python -m pip install -e '.[6502,test]'
python -m pytest -q tests/test_6502_firmware.py tests/test_acia6551.py
python firmware/6502/build_boot.py
```

Ein minimaler Python-Smoke-Test:

```python
from usm.machines.sbc6502 import SBC6502
machine = SBC6502()
result = machine.run()
print(result.uart_text, hex(result.pc))
```

Erwartete Ausgabe: `USM-6502 OK`, PC `0xe00f`. **Erwartung, keine in diesem Dokument nachgewiesene Testausführung.**

Microsoft BASIC-M6502 ist als MIT-lizenzierter Assemblerquelltext in `third_party/microsoft-basic-m6502/` integriert. Ein natives, auf der emulierten CPU laufendes BASIC-ROM ist **noch nicht gebaut**. Die Online-BASIC-Konsole ist davon getrennt und kein echter 6502-Interpreter.

## Grenzen und nächste technische Aufgaben

- Ein einziges maschinenlesbares Backend-Schema statt paralleler Python-/JSON-Kataloge.
- CPU-Familien und tatsächliche Varianten sauber unterscheiden (6502/6507/8502/2A03).
- Busverbindungen, Register, Adressdekodierung, IRQ/DMA und Timing als Graphmodell.
- Maschinenprofile mit realen Firmware- und Medienbeständen (lizenzkonform), Prüfsummen und Verfügbarkeit.
- Systemabhängige Grafik, Sound und Massenspeicher implementieren.
- Echte Backend-Sessions, Boot-/Pause-/Step-/Reset, Snapshot und Trace.
- 6502 Microsoft-BASIC-Port: historische Assemblersyntax, I/O-Anpassung, Build, ROM-Test und serielle Konsole.
- Testpipeline mit Browser-E2E, Python-Tests und Deploy-Gates.

Die Kataloge beschreiben **historische Zielsysteme**, keine Behauptung, dass alle Maschinen schon emulierbar sind.
