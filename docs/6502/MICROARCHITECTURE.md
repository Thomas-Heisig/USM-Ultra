# NMOS 6502 — Mikroarchitektur und Steuersignale

## Kein klassisches Mikrocode-ROM

Der NMOS 6502 ist überwiegend **hartverdrahtet** gesteuert. Ein ROM-Abbild mit „sämtlichem Mikrocode“ wäre irreführend. Die interne Steuerung verwendet Befehlsdekodierung, eine PLA, Taktphasen und Zustandslogik. Visual6502 untersucht diese Schaltungen auf Transistorebene; USM verwendet derzeit den funktionalen Interpreter von py65, **keine Transistorsimulation**.

## Register und Datenpfad

```text
                 +-----------------------+
A0..A15 <--------| PC / Adressgenerator  |
                 +-----------+-----------+
                             |
                 +-----------v-----------+
D0..D7 <-------->| Datenbus / Latches    |
                 +-----------+-----------+
                             |
       +-----------+---------+----------+
       |           |                    |
    +--v--+     +--v--+              +--v--+
    | A   |     | X,Y |              | SP  |
    +--+--+     +--+--+              +-----+
       |           |
       +-----+-----+
             |
         +---v---+         +-----------+
         | ALU   +-------->| P / Flags |
         +-------+         +-----------+
```

Die Grafik ist **ein abstrahiertes Funktionsdiagramm**, kein aus dem Silizium extrahierter vollständiger Schaltplan.

## Exemplarische Maschinenzyklen

- **LDA #imm:** Opcode holen, unmittelbaren Operanden lesen, A und N/Z aktualisieren.
- **STA abs:** Opcode holen, niederwertiges und höherwertiges Adressbyte holen, A an Zieladresse schreiben.
- **JMP abs:** Opcode und zwei Adressbytes holen, PC setzen.
- **BRK:** Interruptablauf mit Stackzugriffen und IRQ/BRK-Vektor; exakte B-Flag-Darstellung beachten.
- **Branch:** Zusätzliche Zyklen bei genommenem Sprung und Seitenwechsel.

Das sind **didaktische Ablaufbeschreibungen**, keine vollständigen pro-Takt-Signalwahrheitstabellen.

## Für zyklengenaue Emulation erforderlich

1. Vollständige NMOS-6502-Opcode-Matrix inklusive ungültiger/undokumentierter Opcodes und Varianten.
2. Adressierungsarten mit Dummy-Reads/-Writes und Seitenwechseln.
3. IRQ/NMI/RESET-Sequenzen und Prioritäten.
4. RDY, SYNC, R/W, PHI0/PHI1/PHI2 und externe Bus-Zeitbeziehungen.
5. Dezimalmodus-Verhalten, einschließlich NMOS-Eigenheiten.
6. Verifikation gegen unabhängige Test-ROMs mit dokumentierter Lizenz und Prüfsumme.

Referenzen: [Visual6502](https://www.visual6502.org/), [py65](https://github.com/mnaberez/py65), [6502.org](http://www.6502.org/).
