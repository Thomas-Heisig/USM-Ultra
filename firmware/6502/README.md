# Original USM-6502 Boot-ROM

This repository contains an original 6502 assembly listing (`boot.asm`) and a dependency-free deterministic builder (`build_boot.py`). It does **not** bundle copyrighted Apple, Commodore or Microsoft BASIC ROM images.

## Build

```bash
python firmware/6502/build_boot.py
```

The generated `firmware/6502/usm6502-boot.bin` is exactly **8192 bytes**. The generator mirrors `usm.machines.sbc6502.demo_rom()` and creates a ROM which sends `USM-6502 OK` to the project's virtual serial TX register at `$8000`, then enters an idle loop.

```text
$E000  LDX #$00
$E002  LDA $E014,X
$E005  BEQ $E00F
$E007  STA $8000
$E00A  INX
$E00B  JMP $E002
$E00E  NOP
$E00F  JMP $E00F
$E012  NOP
$E013  NOP
$E014  "USM-6502 OK",0
$FFFA  $E000 (NMI)
$FFFC  $E000 (RESET)
$FFFE  $E000 (IRQ/BRK)
```

This is a **minimal self-test firmware**, not a full operating system or native BASIC interpreter. To test, install `pip install -e '.[6502,test]'` and run the project test suite. No external firmware is required.
