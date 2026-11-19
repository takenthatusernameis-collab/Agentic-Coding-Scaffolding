# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Routine maintenance / regression monitoring —
   - `python -m unittest discover tests/` (or `pytest tests/`)
   - `python -m ruff check .`
   - `python -m mypy . --exclude build --exclude dist`
   - `python tools/refresh_scaffold.py --check`
   - `python tools/verify_state_delta.py --full --record-full-suite`
4. The persistent-state defect family (unusable cache/marker files trusted by the verification tooling) is now closed on all three consumers — `tools/verify_state_delta.read_marker`, `tools/refresh_scaffold.check_cache_hit`, and `tools/scan_untested.load_cache` — each shape-validates its persisted state and degrades to a safe fallback. If you open a new lead in that family, write a failing test first.
5. The library defect-hunt sweeps (bool-as-int, broad-except swallowing, silently ignored parameters, docstring-vs-implementation contracts via `tools/audit_contracts.py`, float/numeric edge cases, off-by-one boundaries) are complete with no open defect class; newly added modules get a first contract pass before the class is closed again. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`. Do not post duplicate/empty handoffs or commit no-op cycles.
