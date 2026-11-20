# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full --record-full-suite` before making new edits.
3. State is green: this session added `utils.range_list` step=0 validation (raises ValueError with clear message) plus a regression test `test_range_list_rejects_zero_step`, refreshed embedded copies, checkpoint advanced. Continue routine regression monitoring and targeted defect hunt. Focus on accepts-invalid-input (NaN/Infinity, bool-as-number), silently ignored parameters, docstring-vs-implementation contracts, boundary/off-by-one bugs. Write the failing test first.
4. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
5. Test modules must stay under `tests/`; do not add root-level `test_*.py`. Keep `.github/workflows/**` unchanged.
6. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate/empty handoffs or commit no-op cycles. Keep `.github/workflows/**` unchanged.
