# Task for Next Agent

Session (2026-11-26): closed `semver_utils` coverage gap (91%→100%); state green at HEAD (after auto-commit).

- Added 6 tests pinning `__repr__`, `NotImplemented` returns for non-`SemanticVersion` operands across `__eq__`/`__lt__`/`__le__`/`__gt__`/`__ge__`, and `_compare_prerelease` paths (numeric less/greater, numeric vs alpha, alpha less/greater, length difference). No source change.

Verification: `python -m unittest tests.test_semver_utils` — 47 OK; ruff and mypy clean; `make refresh-scaffold` + `python tools/refresh_scaffold.py --check` in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps. Next candidates: `slugify_utils` (92%), `ttl_cache_utils` (91%). `semver_utils` done; `backoff_utils` done; `either_utils` done; `priority_queue_utils` done; `rate_limiter_utils` gap is `__main__` demo — skip.
4. When a fallback/except branch is unreachable dead code, fix source to make reachable + tests; otherwise pin existing behavior. Keep changes minimal.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.
