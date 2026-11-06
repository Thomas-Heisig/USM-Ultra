# USM-Ultra – Wissenschaftliche Studie V7.0

**Dokumentationsindex zur wissenschaftlichen Ausarbeitung**  
Stand: 06.11.2026 · Quelle: `USM_Ultra_Wissenschaftliche_Studie_V7_System_Matrix_UI.docx` (39 Seiten, 31 Tabellen, 15 Abbildungen).

> Diese Datei ist ein strukturierter **Auszug und Kapitelwegweiser**, nicht die vollständige Word-Studie. Das Original ist noch nicht als Binärdatei im Repository abgelegt. Die Aussagen und Entwürfe sind nicht als gemessene Hardwareergebnisse zu verstehen.

## Forschungsziel und Abgrenzung

USM-Ultra untersucht eine modulare, heterogene Rechen- und Recovery-Architektur, die historische reale ICs, emulierte CPUs und künftige FPGA-Karten über klar abgegrenzte lokale Bus-Bridges integriert. Ziel ist ein fließender Übergang von rein virtueller Simulation zu Hardware-in-the-Loop und physischen Chipkarten.

Die Architektur unterscheidet drei Zeitklassen:

| Klasse | Bedeutung | Konsequenz |
|---|---|---|
| T0 | Cycle exact | Lokale FSM/FPGA-Hardware; nicht über asynchronen Host garantierbar |
| T1 | Wait tolerant | Variable, protokollkonforme Wait-States zulässig |
| T2 | Asynchronous | Entkoppelte Steuerung, Diagnose und Datenübertragung |

T2 darf ohne geeignete Pufferung nicht als T0 behandelt werden.

## Systemarchitektur

```text
               MasterVisor / Python / APIs
                        |
                 Virtuelle USP-Matrix
                   /      |       \
          CPU-Adapter   Speicher   Peripherie
          68000/Z80     RAM/ROM    SID/Paula
              |            |          |
       später reale     FPGA BRAM   später echte
       CPU-Karten       SRAM/DDR    ICs / Adapter
                        |
                  Recovery-Module
           Digital Capture / Flux / Analog AFE
```

Die physische Matrix ist als Stern-/Punkt-zu-Punkt-Topologie mit lokalen Bridges konzipiert, nicht als gemeinsamer ungeschützter 5-V-Bus. Das vorläufige 240-Kontakt-Budget ist keine freigegebene elektrische Pinbelegung.

## Kapitelübersicht des vollständigen Dokuments

**Teil I – Forschungsrahmen und Systemkonzept (Kap. 1–15)**

1. Forschungsfrage, Methode, Abgrenzung.
2. Systemarchitektur, elektrische Randbedingungen.
3. Motorola MC68000, Intel 8086/8088, Z80, MOS 6502, 68020/030/040.
4. SID, Paula, VIC-II, Agnus, Denise und Speicher.
5. USP-Transaktionsmodell.
6. Pinplanung, Spannungsdomänen und Backplane.
7. Speicher, MPU, Multiprozessorbetrieb.
8. Rekonfiguration, virtuelle Chips, Shadow-State.
9. Dezentrale KI und MasterVisor.
10. Datenrettung und digitale Forensik.
11. Wirtschaftliche Perspektive.
12. Validierung und Messgrößen.
13. Forschungsfragen und Antworten.
14. Implementierungs-Roadmap.
15. Schlussfolgerungen.

**Teil II – Vertiefte technische Spezifikation (Kap. 16–30)**

16. Funktionale und nichtfunktionale Anforderungen.
17. Topologie, Pegel, CDC, Schutz.
18. MC68000-Busadapter: Lese-/Schreibzyklus, Byte-Lanes, DTACK/BERR.
19. Intel 8086/8088 und 80286.
20. Z80, 6502, 68020/030/040.
21. SID 6581/8580 und analoge Grenzen.
22. Amiga-Custom-Chips und Videotiming.
23. USP 1.0: Handshake, Ordering, Latenzbudget.
24. Speicherfenster, Kohärenz und atomare Dienste.
25. Task-Scheduler und Architektur-Affinität.
26. DPR und dreistufiger Shadow-State.
27. KI-Orchestrierung und Sicherheitsarchitektur.
28. Recovery-Controller, Imaging, Rekonstruktion.
29. Wirtschaftlichkeit, Schutzrechte, Regulierung.
30. Reproduzierbare Versuchsplanung.

**Teil III – System- und Konstruktionsentwurf (Kap. 31–43)**

31. Gesamtsystem und Vertrauensgrenzen.
32. Mechanische und elektrische Matrix.
33. Chipkarten und MC68000-Zustandsautomat.
34. USP, Speicherhierarchie, atomare Queue.
35. FPGA-I/O-Banken und Pegelwandler.
36. Timing-Budgets.
37. Recovery-Hardware und Capture-Pfade.
38. MasterVisor-UI, Matrix-Editor und APIs.
39. Dezentrale KI.
40. Verifikationsmatrix V-001 bis V-010.
41. Technische Forschungsfragen.
42. Entwicklungsphasen und wirtschaftliche Ableitung.
43. Datenblatt- und Quellenprüfplan.

**Anhänge A–G:** Slot-Budget, Chip-Signalmatrix, Registermodell, FAQ, Quellen, Hardwareentscheidungen und Revisionen.

## Verbindliche Implementierungsgrenzen

- MC68000: A1–A23 plus UDS/LDS, 16-Bit-Datenbus; ungerade Wortzugriffe verursachen Address Error.
- Nicht-idempotente Schreibzyklen dürfen bei Retry nicht dupliziert werden.
- Window-Änderungen müssen atomar sein und WIN_GENERATION erhöhen.
- Concurrent TASK_DEQUEUE benötigt eindeutigen Linearization Point.
- Analoger Flux-Capture benötigt eine separat spezifizierte Eingangsstufe; digitale Read-Data-Signale und analoge Kopfspannungen sind nicht gleichzusetzen.
- 5-V-Signale dürfen nicht pauschal direkt an FPGA-I/Os angeschlossen werden.
- FPGA-interne Taktzeiten sind nicht mit kompletten CPU-Buszyklen gleichzusetzen.
- Python V0.2 validiert Semantik, **nicht** Worst-Case-Echtzeit-Timing.

## Noch zu korrigierende Stellen der Word-V7

- Kapitelnummerierung/Doppelung im Bereich Kapitel 16.
- Abb. 11: SID-Bridge statt SID.
- Window-Miss im TRANSLATE-Zustand muss explizit in FAULT übergehen.
- WIN_GENERATION im Registeranhang ergänzen.
- Timingwerte mit Datenblatt- und Messnachweisen ergänzen.
- Abgrenzung zu MiSTer sachlich und quellengeprüft ergänzen.

## Zuordnung zum Quellcode

| Studienbereich | Implementierung |
|---|---|
| USP / Speicherfenster | `usm/core.py` |
| Window-Generation | `usm/advanced.py` |
| Atomare Queue | `usm/advanced.py` |
| Mini-68000-Testkern | `usm/advanced.py` |
| MasterVisor | `usm/web.py` |
| CLI | `usm/cli.py` |
| Tests | `tests/` |

Die vollständige Studie mit ihren Originalabbildungen muss separat als DOCX/PDF in `docs/research/` abgelegt werden, sobald ein binärer Upload verfügbar ist.
