# Musashi integration – native backend design

**Status:** interface specification and scaffold only; no Musashi source, compiled library or fully executing CPU is included.

## Source and licensing

Use a pinned upstream Musashi revision. Record commit SHA, license, compiler and build flags in a provenance manifest. Never import original ROMs into the repository. Musashi is C code; the existing `MiniM68K` interpreter is not Musashi.

## Callback boundary

Musashi normally expects global `m68k_read_memory_8/16/32` and `m68k_write_memory_8/16/32` functions. Implement these in the native shim; bridge them to the virtual USP matrix via registered C function pointers.

Python `ctypes.CFUNCTYPE` callback objects must remain strongly referenced for the lifetime of the native engine. Never allow exceptions to cross the C boundary. Capture error status in the wrapper and return a deterministic fallback value, then surface the fault to the caller after `execute`.

Start with **one CPU context per loaded native library**; multi-instance and concurrent execution require explicit upstream API verification. Musashi cycles are not physical T0 timing.

## Planned ABI

```c
typedef uint32_t (*usm_read_fn)(void *user, uint32_t address, uint32_t width);
typedef void (*usm_write_fn)(void *user, uint32_t address, uint32_t width, uint32_t value);

int usm_m68k_initialize(usm_read_fn read_cb, usm_write_fn write_cb, void *user);
int usm_m68k_reset(void);
int usm_m68k_execute(int cycles);
uint32_t usm_m68k_get_pc(void);
int usm_m68k_set_irq(unsigned level);
```

**Caveat:** This is a proposed API, not a compiled or verified Musashi wrapper. The real implementation must account for vector fetch during reset, 24-bit external address masking, CPU type, exception vectors, IRQ acknowledgment and callback error handling.

## Synthetic test vector

Assemble an original 68000 program that stores 0x1234 at 0x1000, reads it back to D0 and loops. Run the same memory and register assertions against the reference emulator and native Musashi. Do not treat agreement between two incomplete implementations as proof of ISA correctness.

## Acceptance gate

- Reproducible native build on Linux and Windows
- Pinned Musashi upstream revision and license
- Reset vector, instruction fetch and RAM writes through USP callbacks
- 8/16/32-bit big-endian access tests
- 68000 address-error behavior verified
- Fault propagation without C/Python exception leakage
- ASan/UBSan checks for the native shim
