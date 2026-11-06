# USP – vorläufige virtuelle Semantik

USP ist ein Entwurfsprotokoll. Das Python-Modell ist eine **funktionale** Referenz, keine Hardwareimplementierung.

Eine Transaktion enthält Quelle, Adresse, Breite, Lesen/Schreiben und Wert. Die Matrix ermittelt ein eindeutig passendes Speicherfenster, prüft Zugriffsrechte und liefert Antwort oder Fehler.

## Zeitklassen

| Klasse | Bedeutung | Python-Nachweis |
| --- | --- | --- |
| T0 | Cycle exact | nicht implementiert |
| T1 | Wait tolerant | nur funktional |
| T2 | Asynchronous | nur funktional |

## Window-Commit

Konfigurationsänderungen werden als Gesamtsatz geprüft. Überlappungen sind Fehler. Der WIN_GENERATION-Zähler erhöht sich nach erfolgreichem Commit; ein Commit mit veraltetem erwarteten Zähler wird abgelehnt.

## Queue-Linearization

Eine Zuteilung wird innerhalb eines Locks atomar; zwei gleichzeitige Claims erhalten nicht denselben aktiven Task. Lease-Requeue ist **nicht** Exactly-once-Ausführung. Externe Seiteneffekte benötigen Idempotenzschutz.

## Noch offen

Byte-Lane-Adapter je CPU, echte Interrupt-/DMA-Semantik, Busarbitration, Timeout-Budgets, FPGA-Bankplanung, hardwareseitige Fairness.
