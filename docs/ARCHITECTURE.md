# Virtual-first architecture

T0 cycle-exact, T1 wait-tolerant, T2 asynchronous. This Python implementation validates transaction semantics only, not actual T0 deadlines.

CPU core -> USP request -> memory-window mapping -> RAM / ROM / peripheral -> response.

WindowManager replaces the entire window table under a lock and increments WIN_GENERATION. A stale expected generation is rejected.

AtomicTaskQueue assigns a single owner at the lock-protected claim. Leases can expire and tasks can be requeued. Exactly-once *side effects* are not guaranteed: consumers must use idempotency keys or deduplication.

MiniM68K is a **deliberately incomplete** interpreter for smoke testing hand-authored machine code. It is not a substitute for Musashi.

Planned native bridge: Musashi (C) <-> ctypes/CFFI callbacks <-> USP matrix. Third-party code must be reviewed for licenses and validated against reference tests. No external emulator or copyrighted ROMs are vendored.
