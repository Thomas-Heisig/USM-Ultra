# MasterVisor settings

The settings API is **local-only and unauthenticated**. Do not bind the development server to a public address. The settings file is stored outside the repository at `~/.usm-ultra/settings.json`, or at the path specified by `USM_SETTINGS_PATH`.

## REST endpoints

- `GET /api/settings`: effective settings, with defaults if no file exists.
- `PUT /api/settings`: partial update, JSON object. Validated and saved using an atomic file replacement.
- `GET /api/capabilities`: feature flags; distinguish implemented functionality from planned functionality.
- `GET /api/docs-index`: documentation links.

## Supported settings

| Setting | Default | Notes |
| --- | --- | --- |
| `mode` | `virtual` | Hybrid/physical rejected until implemented |
| `hardware_policy` | `manual` | Auto-selection not yet supported |
| `trace_capacity` | 65536 | Bounded in-memory trace ring capacity, 256–1048576 |
| `theme` | `dark` | UI preference, stored for future UI support |
| `locale` | `de` | UI preference |
| `default_cpu` | `cpu0` | Existing CPU bus-master ID |
| `auto_fallback` | false | Cannot enable before hardware backend exists |
| `schema_version` | 1 | Configuration format version |

Settings are stored without credentials or ROM paths. Do not commit your local settings or manifest. For security, configuration changes must not activate unsupported physical features.

## Limitations

The trace capacity can be changed at runtime through the API; trace entries beyond the new capacity are discarded by the ring buffer. Configuration is persisted locally, but the development API has no authentication or multi-user authorization. It must not be exposed on a LAN or Internet.
