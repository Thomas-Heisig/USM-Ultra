"""Openly redistributable USM-6502 starter program and toolchain metadata.

The starter is real 6502 machine code, not a BASIC interpreter.
"""
from .monitor6502 import parse_image

def hello_program():
    # LDX #0 ; LDA $0210,X ; BEQ done ; STA $8000 ; INX ; JMP $0202
    # done: JMP done ; string at $0210
    code = bytes.fromhex("a200bd1102f0078d0080e84c02024c0e02")
    return code + b"USM 6502 READY\r\n\x00"

def install_hello(machine):
    program = hello_program()
    address, payload = parse_image("hello.bin", program, 0x0200)
    return machine.load_program(payload, address, True)

UPSTREAM = {
    "py65": "https://github.com/mnaberez/py65",
    "cc65": "https://github.com/cc65/cc65",
    "tiny_basic": "https://github.com/CorshamTech/6502-Tiny-BASIC",
    "ehbasic": "https://github.com/Klaus2m5/6502_EhBASIC_V2.22",
}
