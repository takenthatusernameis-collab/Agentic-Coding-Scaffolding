# Project Status

## Latest Session (2026-11-15T00:44Z)

- `board_read`: empty (no task posted to main); executed the standing avoidable-delay task from the durable handover.
- **Avoidable process delay removed:** `tests/test_scan_untested.py` ran the scanner CLI as a fresh subprocess for every assertion and re-scanned all 500+ modules each time. Identical invocations are now deduplicated by a memoized `run_cli(*args)` helper, and the single cold scan per mode moved into `setUpModule` (the isolated cache starts empty) so class-collection order can no longer trigger a second cold scan per mode. `TestCacheIntegration` still launches real subprocesses to exercise repeated-run cache reuse for genuine (not memoized) results.
- Measured: `python -m pytest tests/test_scan_untested.py` ~2.34s → ~1.41s (~40% faster); `python -m unittest tests.test_scan_untested` ~1.39s → ~1.32s; full `python -m pytest tests/` ~16.82s → ~15.68s.
- Validation: `python -m pytest tests/test_scan_untested.py` — 44 OK; each class in isolation OK; `python -m pytest tests/` — 11186 OK (skipped=4); `python -m ruff check .` clean; `python -m mypy . --exclude build --exclude dist` clean (567 files); `python tools/scan_untested.py` clean; `python tools/refresh_scaffold.py --check` in sync.

## State

- Working tree: `tests/test_scan_untested.py`, `CHANGELOG.md` (+ embedded copy in `scaffold.sh`), `.kilo/handover.md`, `PROJECT_STATUS.md` pending (non-workflow; CI auto-commits).
- `python tools/verify_state_delta.py --probe` will report verification required for the source-relevant test/doc delta.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect the battery to run once for the changed `tests/`+`CHANGELOG.md` delta, then a clean fast path after auto-commit).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). Remaining measured candidates: `tests/test_refresh_scaffold.py` (~1.1s; `embedded_blocks` re-parses the 6 MB `scaffold.sh` on every `refresh`/`anchor_for` call) and `tests/test_scaffold_sync.py` (~1.0s; per-module substring scans over the large README/CHANGELOG). Prefer equal-coverage reductions (memoize repeated parsing, avoid redundant reads) — do not weaken assertions.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).