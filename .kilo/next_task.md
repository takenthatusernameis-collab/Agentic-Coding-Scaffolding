# Task for Next Agent

Session (2026-11-26): bootstrap (board empty). Advanced checkpoint with `--full --record-full-suite` to HEAD `65ee09dc`. Closed a genuine per-module coverage gap instead of a no-op cycle:

- `priority_queue_utils.py` — the `push` method's `TypeError` for non-numeric priority (line 70) was untested. Added `test_push_rejects_non_numeric_priority` covering strings, `None`, lists, dicts, and objects. Coverage 89% → 90%. Remaining gap at lines 164-170 is a `__main__` demo block — skip. No source change.

Verification: `python -m unittest tests.test_priority_queue_utils` — 26 OK; `python -m ruff check priority_queue_utils.py tests/test_priority_queue_utils.py` clean; `python -m mypy priority_queue_utils.py tests/test_priority_queue_utils.py` success; full suite `python -m unittest discover tests/` — 11878 OK (skipped=4); `make refresh-scaffold` + `python tools/refresh_scaffold.py --check` in sync; `python tools/verify_state_delta.py --full --record-full-suite` passed, checkpoint at HEAD `65ee09dc`. No `.github/workflows/**` changes.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=2 (the auto-commit after this session creates a new commit with the test/CHANGELOG/scaffold changes, so the checkpoint will be behind HEAD); if rc=2 run `python tools/verify_state_delta.py --full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps on wrapper modules (the standing quality bottleneck). Use `python -m coverage run --source=<mod> -m pytest -q tests/test_<mod>.py` then `coverage report -m` to find reachable-but-untested defensive branches; prefer modules with no `sys.settrace` (avoid `trace_utils`/`pdb_utils`/`bdb_utils`, whose low numbers are a coverage-tracing artifact). Good remaining candidates (per a recent scan): `semver_utils` (91%), `slugify_utils` (92%), `ttl_cache_utils` (91%), `backoff_utils` (93%, lines 105/107/109/231-233). `either_utils` is done; `priority_queue_utils` is done (remaining gap is `__main__`); `rate_limiter_utils`'s gap is a `__main__` demo — skip.
4. When a fallback/except branch is unreachable dead code (e.g. a delegated generator/iterator that defers its exception), fix the source so the fallback is reachable and add tests that exercise it; otherwise add tests that pin the existing behavior. Keep changes minimal and behavior-preserving on the happy path.
5. Run `make lint`, `make typecheck`, and the targeted tests when source-relevant files change; run the full suite (`python -m unittest discover tests/`) before recording the checkpoint.
6. If editing any wrapper module/test/CHANGELOG, run `make refresh-scaffold` (re-run after CHANGELOG edits) then `python tools/refresh_scaffold.py --check`.
7. Update handover files; post next task to board when a second participant exists. No `.github/workflows/**` changes.