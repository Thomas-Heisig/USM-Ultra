# USM-Ultra Virtual Lab

Private Python reference platform for Universal Silicon Matrix. Initial version is a **functional** simulation, not cycle-accurate FPGA timing.

## Run

```bash
python -m venv .venv
pip install -e ".[test]"
pytest -q
```

`usm/core.py` models USP-style transactions, memory windows and RAM. `usm/advanced.py` adds atomic window generations, lease-based task claims, local ROM inventory and a tiny machine-code 68000 smoke-test interpreter. **The miniature interpreter is not Musashi and cannot boot TOS or Kickstart.**

## Roadmap

- Integrate reviewed Musashi C source through ctypes/CFFI and map memory callbacks to the virtual USP bus.
- Add the MasterVisor web UI, trace, peripheral and ROM management.
- Extend test coverage, Z80/8086 and hardware adapter interfaces.
- Separate functional semantics from timing models.

## ROM privacy

Store ROMs locally under `roms/`, never commit ROM images or generated manifests. Check ownership and licenses before reuse.

## External projects

Musashi, Hatari, WinUAE, MAME and Z80 emulators are potential reference/integration sources, **not bundled**. Respect their licenses and interfaces.
