# Handover

## Latest Session (2026-11-14T22:34Z)

- `board_read`: empty (no task posted to main); executed the standing task from `PROJECT_STATUS.md`/previous handover: remove the next highest-leverage avoidable process delay.
- **Avoidable process delay removed:** `tests/test_scaffold.py::TestScaffoldKiloJson` ran `scaffold.sh` once per test in `setUp` (4 × ~0.7s ≈ 2.82s). Hoisted the subprocess into `setUpClass`/`tearDownClass` so the deterministic generator runs once per class. `tests/test_scaffold.py` wall time dropped ~2.82s → ~0.73s; full `pytest tests/` ~24.35s → ~22.93s. No assertion weakened.
- `tests/test_scaffold.py` is not embedded in `scaffold.sh` (only `*_utils.py` wrappers and doc/pyproject templates are), so no generator refresh was needed; `refresh_scaffold --check` reports all embedded copies in sync.
- Validation: `python -m pytest tests/test_scaffold.py` — 4 OK; `python -m pytest tests/` — 11183 OK (skipped=4); `ruff`/`mypy` on `tests/test_scaffold.py` clean; `python tools/scan_untested.py` — clean.

## State

- Working tree: `tests/test_scaffold.py`, `CHANGELOG.md`, `.kilo/handover.md`, `PROJECT_STATUS.md` modified (non-workflow). CI auto-commits non-workflow changes after the session.
- After auto-commit, confirm with `python tools/verify_state_delta.py`.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect clean fast path after auto-commit if unchanged).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). Remaining measured candidates: `TestStdlibModulefinder` (~5s total, 4 real-stdlib scans — verify whether a single shared scan preserves per-wrapper coverage before touching it), `test_verify_state_delta.py::TestCommandLine::test_the_check_mode_reports_a_synchronised_repository` (~1.0s), `test_doctests.py` (~0.73s), `scan_untested` cache/integration tests (~0.5s each). Prefer measured equal-coverage reductions (hermetic fixtures, caching/dedup of subprocess work, avoiding redundant checks) — do not weaken assertions.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `python tools/refresh_scaffold.py` and `--check` when embedded sources changed; run `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; run full suite when `tests/` or shared behavior changed; then `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; keep `.github/workflows/**` unchanged; post next task to `main` via `board_post` (record if self-post refused).