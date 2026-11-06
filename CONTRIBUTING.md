# Contributing

Use a feature branch and a pull request. Every change must have an issue or a concise rationale, test evidence, and updated documentation where interfaces change.

## Local checks

```bash
python -m pip install -e ".[web,test]"
python -m pytest -q
python -m compileall -q usm
```

Do not add copyrighted ROMs, BIOS images, recovered data, keys or vendor SDKs without verified redistribution rights. Prefer test ROMs assembled from original instructions and synthetic fixtures.

Distinguish implemented behavior from proposals and measured timing from estimates. Changes to USP and window semantics require regression tests and a specification update.
