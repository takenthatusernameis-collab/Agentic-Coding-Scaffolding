# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Continue routine regression monitoring and targeted defect hunt on hand-rolled (non-wrapper) modules not yet reviewed. Focus on accepts-invalid-input (esp. NaN/Infinity and bool-as-number), silently ignored parameters, docstring-vs-implementation contracts, and boundary/off-by-one bugs. Write the failing test first.
   - Concrete leads from the 2026-11-19 session: (a) `prompt_utils.truncate_prompt` documents `suffix` as "the suffix to append when truncated" but silently drops it when `max_length <= len(suffix)`; (b) `prompt_utils.wrap_prompt(width=0)` returns the raw text without the whitespace normalisation that every `width > 0` path applies (undocumented asymmetry); (c) `timing_utils.elapsed_time` accepts non-numeric `start_time` and relies on the subtraction `TypeError` with no `Raises:` clause.
   - Concrete leads from the 2026-11-20 session: (a) `shapes.py` hand-rolled geometry functions validated type but compared with `< 0`, letting `NaN` and `+inf` through — verified fixed; next focus modules: `stats.py`, `utils.py`, `greeting_utils.py`, `hello.py`, `calculator.py`.
4. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
5. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
6. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate/empty handoffs or commit no-op cycles. Keep `.github/workflows/**` unchanged.

(End of file - total 10 lines)