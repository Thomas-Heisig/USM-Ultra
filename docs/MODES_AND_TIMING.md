# Execution modes and timing classes

## Operating modes

| Mode | Meaning | Availability now |
|---|---|---|
| virtual | All machine components use software implementations | Architectural target; only functional prototype exists |
| hybrid | Selected components use verified physical hardware; others remain virtual | Not implemented |
| physical | Required components of a machine profile are physical | Not implemented |

Physical-only operation is **optional** and cannot replace the software-only product requirement. A physical profile is valid only if all required physical devices and their dependent buses are present.

## Timing classes

| Class | Intended guarantee | V0.2/V0.3 current behavior |
|---|---|---|
| T0 | Cycle exact at a specified physical clock and pin-level boundary | Not modeled or verified |
| T1 | Wait-state-tolerant synchronous transfers | Functional synthetic latency count only |
| T2 | Asynchronous transactions with explicit ordering | Partial transaction/queue semantics |

The Python `Mapping.latency` count is an illustrative logical cost, **not** measured hardware wait-states. Do not claim 0–1 or 1–2 wait-states without clock-domain assumptions, board design and physical validation.

A future deterministic simulation backend must implement a virtual clock and a timing profile with per-transaction delay, arbitration and trace timestamps. A virtual-clock simulation is not a substitute for signal-level FPGA verification.

## Mode selection config (proposed; not yet parsed by runtime)

```json
{
  "schema_version": 1,
  "mode": "virtual",
  "hardware_policy": "manual",
  "devices": {
    "cpu0": {"component": "m68000", "backend": "emulated", "timing_class": "T1"},
    "sound0": {"component": "sid6581", "backend": "emulated", "timing_class": "T1"}
  }
}
```

The example is a **future configuration schema**, not a currently bootable machine. A SID emulator is not yet available.

## Verification plan

Compare reference instruction traces, bus read/write ordering, exception vectors, memory checksums, interrupt/DMA sequencing and device-level test ROM outputs between virtual and physical backends. Record tested frequency, FPGA revision, firmware and environment. For non-deterministic analog hardware, compare within defined measurement tolerances.
