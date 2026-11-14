# Project Status

## Latest Session (2026-11-14T21:48Z)

- `board_read`: no pending task/messages. Probe: `verify_state_delta --probe` rc=1 (clean/no source-relevant change vs checkpoint) but `refresh_scaffold --check` reported stale `CHANGELOG.md` embed in `scaffold.sh` (integrity/drift), so probe later rc=2 after tree state considered.
- **Scaffold integrity repair:** ran `python tools/refresh_scaffold.py` to regenerate embedded copies (`scaffold.sh` updated, `CHANGELOG.md` embed resynced). `python tools/refresh_scaffold.py --check` is now in sync (idempotent). No `.github/workflows/**` changes; no library/source behavior changes.
- Validation: `python -m unittest tests.test_scaffold_sync tests.test_refresh_scaffold` (52 OK), `python -m unittest tests.test_verify_state_delta` (27 OK), `python tools/scan_untested.py` (clean). `ruff`/`mypy` clean on prior checkpoint context (no source edits this session beyond scaffold regeneration).

## State

- Working tree: `scaffold.sh`, `PROJECT_STATUS.md`, `.kilo/handover.md` pending (non-workflow; CI auto-commits).
- Last verified checkpoint context remains as recorded in `.kilo/verify_state.json` until advanced by `verify_state_delta` after commit/state change.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect clean fast path after auto-commit if unchanged).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). Profiling candidates from prior session: `TestStdlibModulefinder` (~5s total, opt-in), `test_verify_state_delta.py::TestCommandLine::test_the_check_mode_reports_a_synchronised_repository` (~1.0s), `test_doctests.py` (~0.76s), scaffold tests (~0.67–0.69s each), `scan_untested` cache/integration tests (~0.5s). Favor measured equal-coverage reductions (hermetic fixtures, caching/dedup of subprocess work, avoiding redundant checks) — do not weaken assertions.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).
