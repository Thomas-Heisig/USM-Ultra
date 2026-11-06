# Planned CPU and chip catalog

Source of truth: [usm/catalog.py](../usm/catalog.py). The catalog includes Motorola 68k family, Intel 8086/8088/80286, Z80, MOS 6502/6510, Amiga custom chips, C64 SID/VIC-II/CIA, Atari ST GLUE/MMU/Shifter/PSG/MFP/ACIA, memory, bridge and recovery devices.

Each component exposes:

```json
{
  "id": "m68000",
  "name": "Motorola MC68000",
  "family": "CPU",
  "role": "16/32-bit CISC CPU",
  "implementation": "stub",
  "hardware": "not_probed",
  "available_virtual": false,
  "available_hardware": false,
  "dependencies": [],
  "notes": "Bus master and tiny instruction smoke-test; Musashi not integrated"
}
```

The backend catalog is **not** a claim that hardware was scanned. No physical probe transport exists yet. UI labels must distinguish `not_probed` from `not_present`.

## API

- `GET /api/components` – all components, optionally `?family=CPU`
- `GET /api/components/summary` – counts by implementation
- `GET /api/components/{component_id}` – one component or HTTP 404
- `GET /api/status` – live virtual matrix status

These are read-only inventory endpoints. Hardware configuration and switching will require authorization and validation before being exposed.

## Later capabilities

Every chip profile will eventually declare address map, bus width, endianness, voltage domain, timing class, IRQ/DMA, ROM dependencies, compatible backends, health, and test vectors. No arbitrary physical IO or untrusted firmware should be exposed through the unauthenticated development UI.
