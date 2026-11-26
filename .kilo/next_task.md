# Task for Next Agent

Session (2026-11-26): bootstrap (board empty). Advanced checkpoint with `--full --record-full-suite` to HEAD `cb67cb21`. Closed a genuine per-module coverage gap instead of a no-op cycle:

- `backoff_utils.py` — the `exponential_backoff` TypeError branches for non-numeric `factor` (line 105), `max_delay` (line 107), and `attempt` (line 109) were untested. Extended `test_exponential_backoff_validation` with `exponential_backoff(1.0, "x", 100.0)`, `exponential_backoff(1.0, 2.0, "x")`, and `exponential_backoff(1.0, 2.0, 100.0, attempt="x")`. Coverage 93% → 97%. Remaining gap at lines 231-233 is a `__main__` demo block — skip. No source change.

Verification: `python -m unittest tests.test_backoff_utils` — 20 OK; `python -m ruff check backoff_utils.py tests/test_backoff_utils.py` clean; `python -m mypy backoff_utils.py tests/test_backoff_utils.py` success; full suite `python -m unittest discover tests/` — 11878 OK (skipped=4); `make refresh-scaffold` + `python tools/refresh_scaffold.py --check` in sync; `python tools/verify_state_delta.py --full --record-full-suite` passed, checkpoint at HEAD `cb67cb21`. No `.github/workflows/**` changes.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=2 (the auto-commit after this session creates a new commit with the test/scaffold changes, so the checkpoint will be behind HEAD); if rc=2 run `python tools/verify_state_delta.py --full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps on wrapper modules (the standing quality bottleneck). Use `python -m coverage run --source=<mod> -m pytest -q tests/test_<mod>.py` then `coverage report -m` to find reachable-but-untested defensive branches; prefer modules with no `sys.settrace` (avoid `trace_utils`/`pdb_utils`/`bdb_utils`, whose low numbers are a coverage-tracing artifact). Good remaining candidates (per a recent scan): `semver_utils` (91%, lines 80/84/94/107/112/117 + `_compare_prerelease` paths 217/219/223/226/228/232), `slugify_utils` (92%), `ttl_cache_utils` (91%). `backoff_utils` is done (97%, remaining gap is `__main__`); `either_utils` is done; `priority_queue_utils` is done; `rate_limiter_utils`'s gap is a `__main__` demo — skip.
4. When a fallback/except branch is unreachable dead code (e.g. a delegated generator/iterator that defers its exception), fix the source so the fallback is reachable and add tests that exercise it; otherwise add tests that pin the existing behavior. Keep changes minimal and behavior-preserving on the happy path.
5. Run `make lint`, `make typecheck`, and the targeted tests when source-relevant files change; run the full suite (`python -m unittest discover tests/`) before recording the checkpoint.
6. If editing any wrapper module/test/CHANGELOG, run `make refresh-scaffold` (re-run after CHANGELOG edits) then `python tools/refresh_scaffold.py --check`.
7. Update handover files; post next task to board when a second participant exists. No `.github/workflows/**` changes.
