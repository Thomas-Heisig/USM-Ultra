; USM-6502 original boot monitor (CC0 / project-authored)
; CPU: MOS 6502 (NMOS compatible)
; Origin: $E000, size: 8192 bytes. External assembler not required by
; build_boot.py; this file documents the intended assembly.
;
; Memory mapped USM serial TX: $8000. Not a MOS 6551 ACIA.
        .org $E000
reset:  ldx #$00
loop:   lda banner,x
        beq idle
        sta $8000
        inx
        jmp loop
        nop
idle:   jmp idle
        nop
        nop
banner: .byte "USM-6502 OK",0
; Remaining ROM bytes are NOP ($EA).
; Vectors: $FFFA=NMI, $FFFC=RESET, $FFFE=IRQ/BRK -> reset.
