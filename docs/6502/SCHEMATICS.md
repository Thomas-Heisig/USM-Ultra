# USM-6502 — eigene logische Schaltbilder

Die folgenden Darstellungen sind **logische Entwürfe**, keine geprüften Fertigungsunterlagen, kein PCB-Layout und kein vollständiger elektrischer Original-6502-Schaltplan.

## Systemübersicht

```text
                       USM VIRTUAL MATRIX
     +----------------------------------------------------+
     | CPU: NMOS 6502 via py65                            |
     |   A0..A15 / D0..D7 / R-W / RESET / IRQ / NMI      |
     +-------------------------+--------------------------+
                               |
                    +----------v-----------+
                    | Adressdekodierung     |
                    +--+------+-----+-----+
                       |      |     |     |
            +----------+      |     |     +-------------+
            |                 |     |                   |
     +------v------+   +------v--+  |            +------v------+
     | 32 KiB RAM  |   | USM I/O |  |            | 8 KiB ROM   |
     | $0000-7FFF  |   | $8000+  |  |            | $E000-FFFF  |
     +-------------+   +----+----+  |            +-------------+
                            |       |
                 +----------+-------+-----------+
                 | Serial $8000-$8001           |
                 | Timer  $8010-$8013           |
                 | GPIO   $8020-$8021           |
                 +------------------------------+
```

## CPU-Anschlusskonzept für künftige Hardware

```text
CPU A[15:0] --------> Adressdekoder --------> CS_RAM / CS_ROM / CS_IO
CPU D[7:0]  <------> tri-state Datenbus <--> RAM / ROM / I/O
CPU R/W     --------> Schreib-/Lesesteuerung
PHI2        --------> Timing / gültige Busphase
RESET_N     <-------- Reset-Schaltung
IRQ_N       <-------- Interrupt-ODER (Open-Drain-konform)
NMI_N       <-------- NMI-Quellen
RDY         <-------- Wait-State / DMA-Steuerung
```

**Sicherheit und Grenzen:** Spannungspegel, Lastkapazitäten, Clock-Generator, Reset-Pulsdauer, Pull-ups, Pegelwandler, Bus-Contention, Stromversorgung und Pinbelegung hängen von der *konkreten* CPU-Variante und dem Datenblatt ab. **Kein direktes Verdrahten nach dieser ASCII-Grafik.** Original-NMOS-6502, W65C02 und 6510 sind elektrisch und funktional nicht austauschbar.

## Weitere Schaltbilder

- [Mikroarchitektur](MICROARCHITECTURE.md) (Register/ALU/Steuerung)
- [Firmware und Vektoren](../../firmware/6502/README.md)
- [Projektmatrix](../MOS_6502_REFERENCE.md)

Für ein tatsächlich fertigungstaugliches KiCad-Projekt fehlen Bauteilwahl, genaue Pinouts, Schaltungssimulation/ERC, Stromversorgungs- und Timingnachweis.
