# Virtual-first architecture – normative design decision

## Fundamental invariant

**USM-Ultra must remain usable without any physical USM hardware.** Physical chips, FPGA bridges, external data buses and recovery frontends are optional backends. Absence, unplugging, malfunction or deliberate deactivation of a hardware adapter must not prevent launching the software-only platform.

This is a product requirement and an architectural constraint, **not** a claim that every historical machine already boots in the current prototype.

## Component lifecycle

Each component has a stable logical identity, a capability descriptor and one selected backend:

- `emulated`: software-only implementation (default and required baseline)
- `native`: optional optimized C/C++/Rust/assembly software implementation
- `hardware`: optional real FPGA/IC/peripheral adapter
- `unavailable`: component cannot currently run; must be explained to the operator

The first two are both software-only. `native` is not physical hardware.

## Selection policy

1. Start in emulation by default; do not require physical detection to boot.
2. Discover hardware asynchronously and validate identity, firmware, voltage, protocol, timing class, health and user policy.
3. Offer per-device manual selection and optional opt-in automatic preference for verified hardware.
4. Switch only after quiescence and consistency checks. Physical analog state or DMA activity may make seamless transfer impossible.
5. If migration cannot be proven safe, require a controlled reset/restart, not a fictitious live swap.
6. On hardware failure, return to emulation where a consistent state exists; otherwise preserve evidence and offer safe restart.

## Stable logical contracts

```text
 MasterVisor / virtual machine profiles / user ROM library
                         |
              Logical device registry
                         |
               USP transaction layer
                         |
          Backend capability and policy
              /          |          \
        Python       native C       hardware
       emulator      emulator      FPGA/IC bridge
              \          |          /
              trace / faults / snapshots
```

No high-level machine profile should depend directly on USB, PCIe, Ethernet, FPGA GPIO or a particular emulator implementation. All such dependencies belong behind adapters.

## Backend interface (design)

```python
class DeviceBackend(Protocol):
    def capabilities(self) -> CapabilitySet: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def transact(self, request: Transaction) -> Response: ...
    def snapshot(self) -> bytes | None: ...
    def restore(self, snapshot: bytes) -> None: ...
    def health(self) -> HealthReport: ...
```

Snapshots are optional capabilities. They must never be assumed for original chips. Backend implementations must define endianness, address width, bus lanes, ordering, timeout behavior and interrupt/DMA semantics.

## Compatibility goals

- Software-only Atari ST/TOS and Amiga profiles require substantially more than CPU emulation: memory maps, custom chips, video, audio, input, storage, interrupts and DMA.
- Original ROMs are loaded only from user-controlled local storage and checked for correct mapping/format.
- Musashi is an initial CPU candidate; Hatari/WinUAE are reference applications, not plug-and-play library modules.
- Hardware-specific cycle exactness must be measured and validated separately.

## Acceptance tests

- Startup with no hardware attached.
- Start/stop a virtual CPU and perform deterministic memory transactions.
- Select a native software backend without changing machine profile semantics.
- Simulate absent, incompatible, offline and failing hardware.
- Verify policy-controlled fallback and explicitly fail when state migration is unsafe.
- Verify no ROM or manifest is sent to the server, repository or telemetry.
