# MasterVisor – modular web frontend

MasterVisor is the **primary operator interface** for USM-Ultra. Python CLI remains a developer and automation interface, not a requirement for routine operation.

## Start

```bash
python -m pip install -e ".[6502,web,test]"
python -m usm.cli web
```

Open **http://127.0.0.1:8000**. The server must remain bound to localhost: there is currently no login, CSRF protection, user roles or secure remote deployment.

## Navigation and module pages

| Module | Frontend behavior | Backend |
| --- | --- | --- |
| Dashboard | Live matrix status and chip counts | `/api/status`, `/api/components/summary` |
| Machines | Run synthetic USM-6502 ROM and inspect output | `/api/machines`, `/api/machines/usm-6502/run` |
| Chip modules | Search, filter and inspect 38 catalog entries | `/api/components` |
| USP matrix | Execute read/write transactions, inspect windows | `/api/access`, `/api/status` |
| Memory | Inspect mapped RAM/ROM in a bounded hex dump | `/api/memory` |
| Task queue | Submit and list experimental tasks | `/api/tasks` |
| Bus trace | Inspect and download bounded JSON trace | `/api/trace` |
| Hardware | Shows unimplemented capability flags; no false device detection | `/api/capabilities` |
| Recovery | Planned modules and disabled actions | `/api/components` |
| Settings | Persistent local settings, theme selection | `/api/settings` |
| Documentation | Research and engineering links, OpenAPI access | `/api/docs-index`, `/docs` |

All pages are within a responsive single-page frontend with hash navigation. Unimplemented features are disabled or explicitly labeled; the existence of a UI panel does not imply a functioning emulator or hardware driver.

## Module interface contract

Each future module must declare:
- stable component ID, category and implementation status
- virtual and hardware backend capability independently
- operational endpoints with validated input and bounded output
- device-specific panel with start/stop/reset only when supported
- diagnostics and trace support
- safe backend transition and recovery semantics
- documentation and acceptance tests

## Known limitations

- No production authentication, user accounts, CSRF protection, websocket streaming or real-time debugger.
- 6502 demonstration executes a short ROM and returns output; it is not an interactive terminal.
- Trace is currently a snapshot of in-memory events, not a forensic capture service.
- Task submission/listing is implemented; worker orchestration is not yet exposed in the UI.
- Memory inspection is read-only and uses individual bus transactions.
- Hardware/recovery pages are preparation, not functioning devices.
- Full machine emulation, Musashi integration and hybrid mode remain future milestones.

## Release checks

Run `python -m pytest -q` and inspect the UI at desktop and mobile widths. CI results must be checked separately; committing files does not prove the application passes all tests.
