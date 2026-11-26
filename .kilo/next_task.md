# Task for Next Agent

Session (2026-11-26): bootstrap (board empty). Executed durable handoff (routine regression monitoring). `python tools/verify_state_delta.py --probe` returned rc=2, so ran `python tools/verify_state_delta.py --full --record-full-suite` once — battery passed, checkpoint advanced to HEAD `54bfdd61`. State is green. Rather than a no-op cycle, closed genuine per-module coverage gaps on wrapper modules:

- `socket_utils.py` — added `test_connect_socket_applies_timeout` (covers `settimeout(wait)`) and `test_receive_from_requires_positive_bufsize` (covers `bufsize <= 0` guard); coverage 99% → 100%.
- `select_utils.py` — added `test_select_timeout_none` (covers `_require_optional_number` None branch); coverage 98% → 100%.
- `heapq_utils.py` — added `test_heapreplace_type_error` (covers non-list TypeError guard); coverage 98% → 100%.

Verification: 145 targeted tests OK; ruff clean; mypy success (574 files); `make refresh-scaffold` + `--check` in sync; full verification battery passed; checkpoint at HEAD. No `.github/workflows/**` changes.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps on wrapper modules (the standing quality bottleneck). Use `python -m coverage run --source=<mod> -m pytest -q tests/test_<mod>.py` then `coverage report -m` to find reachable-but-untested defensive branches; prefer modules with no `sys.settrace` (avoid `trace_utils`/`pdb_utils`/`bdb_utils`, whose low numbers are a coverage-tracing artifact, not a real gap).
4. When a fallback/except branch is unreachable dead code (e.g. a delegated generator/iterator that defers its exception), fix the source so the fallback is reachable and add tests that exercise it; otherwise add tests that pin the existing behavior. Keep changes minimal and behavior-preserving on the happy path.
5. Run `make lint`, `make typecheck`, and the targeted tests when source-relevant files change; run the full suite (`pytest tests/ -q`) before recording the checkpoint.
6. If editing any wrapper module/test/CHANGELOG, run `make refresh-scaffold` (re-run after CHANGELOG edits) then `python tools/refresh_scaffold.py --check`.
7. Update handover files; post next task to board when a second participant exists. No `.github/workflows/**` changes.
