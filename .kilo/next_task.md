# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Routine maintenance / regression monitoring: run the verification battery periodically —
   - `python -m unittest discover tests/` (or `pytest tests/`)
   - `python -m ruff check .`
   - `python -m mypy . --exclude build --exclude dist`
   - `python tools/refresh_scaffold.py --check`
   - `python tools/verify_state_delta.py --full --record-full-suite`
4. The defect-hunt sweeps (bool-as-int, broad-except swallowing, silently ignored parameters, docstring-vs-implementation contracts via `tools/audit_contracts.py`, float/numeric edge cases, off-by-one boundaries) are complete with no open defect class. Do not open a new defect class unless a genuine regression is found; hand off to routine monitoring instead.
5. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`. Do not post duplicate/empty handoffs or commit no-op cycles.