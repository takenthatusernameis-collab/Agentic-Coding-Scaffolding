# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Continue routine regression monitoring and targeted defect hunt on hand-rolled (non-wrapper) modules not yet reviewed (`utils.py`, `strings.py`, `stats.py`, `type_check_utils.py`, `uuid_utils.py`). Focus on accepts-invalid-input (esp. NaN/Infinity and bool-as-number), silently ignored parameters, docstring-vs-implementation contracts, and boundary/off-by-one bugs. Write the failing test first.
4. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
5. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
6. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate/empty handoffs or commit no-op cycles. Keep `.github/workflows/**` unchanged.
" filePath">
.kilo/next_task.md
## Latest Session (2026-11-19) — routine regression monitoring; verification battery green at HEAD c34af23

- `board_read`: empty (bootstrap session); executed durable handoff from `.kilo/next_task.md`.
- **State:** probe rc=1 (checkpoint behind HEAD); ran full verification, checkpoint advanced to HEAD `c34af23`.
- **Defect hunt:** audit_contracts — 249 low-signal stdlib-delegation candidates (unchanged), 0 genuine defects; scan_untested — no exported-but-untested callables. Target modules reviewed (utils.py, strings.py, stats.py, type_check_utils.py, uuid_utils.py) — no new defects.
- **Verification battery:** unittest discover — OK (skipped=4); ruff clean; mypy success (572 source files); refresh_scaffold in sync; verify_state_delta passed at HEAD `c34af23`.
- **Changes:** checkpoint advanced. No source/test changes. No `.github/workflows/**` changes.
