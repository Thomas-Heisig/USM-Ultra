"""Virtual 6502 peripherals. Registers are project-defined, not 6551/6522 compatible."""
from collections import deque

class SerialPort:
    # offset 0: DATA, offset 1: STATUS (bit0 RX ready, bit1 TX ready)
    def __init__(self):
        self.output = bytearray()
        self.input = deque()
    def read(self, offset, width):
        if width != 1:
            raise ValueError("serial registers are byte-wide")
        if offset == 0:
            return self.input.popleft() if self.input else 0
        if offset == 1:
            return (1 if self.input else 0) | 2
        raise ValueError("invalid serial register")
    def write(self, offset, width, value):
        if width != 1:
            raise ValueError("serial registers are byte-wide")
        if offset == 0:
            self.output.append(value & 255)
        elif offset != 1:
            raise ValueError("invalid serial register")
    def receive(self, payload):
        if len(self.input) + len(payload) > 4096:
            raise ValueError("serial RX queue full")
        self.input.extend(payload)
    def text(self):
        return self.output.decode("ascii", errors="replace")

class Timer:
    # offset 0/1: period low/high; 2: control bit0 enable; 3: pending bit0
    def __init__(self):
        self.period = 0
        self.counter = 0
        self.enabled = False
        self.pending = False
    def read(self, offset, width):
        if width != 1:
            raise ValueError("timer registers are byte-wide")
        if offset == 0: return self.period & 255
        if offset == 1: return self.period >> 8
        if offset == 2: return int(self.enabled)
        if offset == 3: return int(self.pending)
        raise ValueError("invalid timer register")
    def write(self, offset, width, value):
        if width != 1:
            raise ValueError("timer registers are byte-wide")
        if offset == 0: self.period = (self.period & 0xFF00) | (value & 255)
        elif offset == 1: self.period = (self.period & 255) | ((value & 255) << 8)
        elif offset == 2:
            self.enabled = bool(value & 1)
            self.counter = 0
        elif offset == 3:
            if value & 1: self.pending = False
        else: raise ValueError("invalid timer register")
    def advance(self, ticks):
        if self.enabled and self.period:
            self.counter += ticks
            if self.counter >= self.period:
                self.pending = True
                self.counter %= self.period

class GPIO:
    # offset 0: data; offset 1: direction (1=output)
    def __init__(self):
        self.data = 0
        self.direction = 0
        self.inputs = 0
    def read(self, offset, width):
        if width != 1: raise ValueError("GPIO registers are byte-wide")
        if offset == 0: return (self.data & self.direction) | (self.inputs & (~self.direction & 255))
        if offset == 1: return self.direction
        raise ValueError("invalid GPIO register")
    def write(self, offset, width, value):
        if width != 1: raise ValueError("GPIO registers are byte-wide")
        if offset == 0: self.data = value & 255
        elif offset == 1: self.direction = value & 255
        else: raise ValueError("invalid GPIO register")

class DeviceBackend:
    """Hardware replacement contract; no physical backend exists yet."""
    def read(self, offset: int, width: int) -> int: raise NotImplementedError
    def write(self, offset: int, width: int, value: int) -> None: raise NotImplementedError
    def snapshot(self) -> dict: raise NotImplementedError
    def restore(self, state: dict) -> None: raise NotImplementedError
