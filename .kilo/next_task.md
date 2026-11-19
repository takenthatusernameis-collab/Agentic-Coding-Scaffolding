# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Continue the targeted defect hunt on hand-rolled (non-stdlib-passthrough) modules that earlier sweeps did not cover. Reviewed on 2026-11-19 without defects: `duration_utils`, `validation_utils`, `tree_utils`, `sort_utils`, `maybe_utils`, `either_utils`, `retry_utils`, `circuit_breaker_utils`. `statistics_utils` had a real defect and was fixed.
   - Untouched candidates: `slugify_utils`, `terminal_utils`, `shapes.py`, `config_schema.py`, `deprecation_utils`, `cooldown_utils`, `rate_limiter_utils`, `interval_utils` (already reviewed), `ring_buffer_utils` (already reviewed).
   - Focus on classes already established: accepts-invalid-input, silently ignored parameters, docstring-vs-implementation contracts, boundary/off-by-one. Write the failing test first.
4. Routine gates at a coherent milestone: `python -m pytest tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
5. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
6. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate/empty handoffs or commit no-op cycles.