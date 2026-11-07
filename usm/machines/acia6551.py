"""Experimental MOS 6551-like ACIA register model.

This is a behavioral peripheral for USM; it does not claim cycle-accurate
MOS 6551 emulation. Register layout: DATA, STATUS, COMMAND, CONTROL.
"""
from collections import deque

class ACIA6551:
    """Minimal 6551 register-facing serial adapter, without clock or IRQ timing."""
    def __init__(self):
        self.rx = deque()
        self.tx = bytearray()
        self.command = 0
        self.control = 0
        self.overrun = False

    def read(self, offset, width):
        if width != 1 or not 0 <= offset < 4:
            raise ValueError("6551 uses four byte-wide registers")
        if offset == 0:
            return self.rx.popleft() if self.rx else 0
        if offset == 1:
            # bit 3 RX full, bit 4 TX empty, bit 2 overrun
            return (8 if self.rx else 0) | 16 | (4 if self.overrun else 0)
        if offset == 2:
            return self.command
        return self.control

    def write(self, offset, width, value):
        if width != 1 or not 0 <= offset < 4:
            raise ValueError("6551 uses four byte-wide registers")
        value &= 255
        if offset == 0:
            self.tx.append(value)
        elif offset == 1:
            self.rx.clear()
            self.overrun = False
        elif offset == 2:
            self.command = value
        else:
            self.control = value

    def receive(self, payload):
        for value in payload:
            if len(self.rx) >= 4096:
                self.overrun = True
                break
            self.rx.append(value & 255)

    def text(self):
        return self.tx.decode("ascii", errors="replace")
