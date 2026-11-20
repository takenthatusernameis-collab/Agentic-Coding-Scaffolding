# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full --record-full-suite` before making new edits.
3. State is green: this session refreshed the stale embedded `CHANGELOG.md` copy in `scaffold.sh` (the prior session's repo `CHANGELOG.md` change was never synced into `scaffold.sh`, which broke `tests/test_scaffold_sync`), then ran the full verification battery — `test_scaffold_sync` passes, `refresh_scaffold --check` in sync, full suite OK, checkpoint advanced to HEAD `07872fc`. Continue routine regression monitoring and targeted defect hunt on hand-rolled modules not yet reviewed. Focus on accepts-invalid-input (esp. NaN/Infinity and bool-as-number), silently ignored parameters, docstring-vs-implementation contracts, and boundary/off-by-one bugs. Write the failing test first.
   - Full `audit_contracts.py` scan: 239 low-signal stdlib-delegation candidates, 0 genuine defects (no fix needed this session).
   - `scan_untested.py`: no exported-but-untested callables.
   - Focus modules from prior leads (`stats.py`, `utils.py`, `greeting_utils.py`, `hello.py`, `calculator.py`) reviewed this session; no genuine defect found.
4. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
5. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
6. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate/empty handoffs or commit no-op cycles. Keep `.github/workflows/**` unchanged.
