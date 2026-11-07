#!/usr/bin/env python3
"""Reproducible original USM-6502 boot ROM build; no external assembler.

Writes exactly 8192 bytes to the requested output path. This script is
project-authored and mirrors usm.machines.sbc6502.demo_rom.
"""
from pathlib import Path
import argparse
import hashlib

ROM_START = 0xE000
ROM_SIZE = 0x2000
PROGRAM = bytes([
    0xA2, 0x00,             # LDX #$00
    0xBD, 0x14, 0xE0,       # LDA $E014,X
    0xF0, 0x08,             # BEQ idle ($E00F)
    0x8D, 0x00, 0x80,       # STA $8000
    0xE8,                   # INX
    0x4C, 0x02, 0xE0,       # JMP loop
    0xEA,                   # NOP
    0x4C, 0x0F, 0xE0,       # JMP idle
    0xEA, 0xEA,             # padding
])
BANNER = b"USM-6502 OK\x00"

def build():
    image = bytearray([0xEA] * ROM_SIZE)
    assert len(PROGRAM) == 0x14
    image[:len(PROGRAM)] = PROGRAM
    image[0x14:0x14 + len(BANNER)] = BANNER
    vector = ROM_START.to_bytes(2, "little")
    for offset in (0x1FFA, 0x1FFC, 0x1FFE):
        image[offset:offset + 2] = vector
    return bytes(image)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="firmware/6502/usm6502-boot.bin")
    args = parser.parse_args()
    payload = build()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    print(f"{target}: {len(payload)} bytes SHA256 {hashlib.sha256(payload).hexdigest()}")

if __name__ == "__main__":
    main()
