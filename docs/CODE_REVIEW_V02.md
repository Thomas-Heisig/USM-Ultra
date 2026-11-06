# V0.2 code review and limitations

| Question | Actual implementation |
|---|---|
| USP entry point | `Matrix.transact(Transaction)` in `usm/core.py` |
| Memory windows | `Mapping(start,size,device,name,read,write,latency)` |
| Window generation | `WindowManager.replace(mappings,expected_generation)` |
| Error representation | `Response.error` is currently a string, **not** a typed error enum |
| Trace | `collections.deque(maxlen=4096)`, exposed by `GET /api/trace` |
| Web API | FastAPI, automatic OpenAPI at `/openapi.json` |
| Queue atomicity | `threading.Lock` protects claim; Python GIL alone is not relied upon |
| Lease time | Injectable `clock` callable, allowing deterministic fake clocks |
| Mini CPU opcodes | NOP, MOVEQ, MOVE.L Dn to absolute long, MOVE.L absolute long to Dn, STOP only |
| Mini CPU flags | No complete SR/CCR, exception model or addressing modes |

## Risks

- Window table swaps are lock-protected against other window commits but matrix transactions do not currently acquire the same lock: concurrent readers can observe the previous or next table, not a multi-stage transition, but the intended consistency contract must be formalized.
- The queue's claim lock gives unique ownership; its stated round-robin fairness is **not implemented as a strict arbiter**.
- A task that times out may be retried; exactly-once external side effects require additional deduplication.
- Typed error codes (TIMEOUT, DECODE, PERMISSION, TARGET_OFFLINE, ECC) are **not implemented**.
- SID is a 32-byte register stub, not an audio emulator.
- Browser API is local development only; no authentication.
- No verified timing budgets or native Musashi integration.

## Next acceptance items

1. Typed fault codes and structured fault traces.
2. Window staging and atomic commit contract.
3. Real Musashi C shim and ctypes binding.
4. CI passing on supported Python versions.
5. Separate timing model for T0/T1/T2, without claiming Python is cycle exact.
