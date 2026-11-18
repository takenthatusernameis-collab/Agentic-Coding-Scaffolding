# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Targeted follow-up from the last session (same persistent-state defect family that was just fixed in `tools/verify_state_delta.read_marker`): `tools/refresh_scaffold.check_cache_hit()` accepts `managed_paths` from a parsed cache file without validating element types. `load_check_cache()` only requires a top-level object, then `_check_cache_fingerprint(cached_paths)` evaluates `ROOT / relative` for each entry, so a valid-JSON `.kilo/refresh_scaffold_cache.json` containing `"managed_paths": [1, 2]` (with a matching `root_mtime`) makes `python tools/refresh_scaffold.py --check` raise `TypeError` instead of falling back to a full comparison. Write a failing test first, validate the cached list (strings only) in `check_cache_hit`, and check `tools/scan_untested.py`'s `load_cache` (already shape-validated) for contrast. If the lead proves not genuine, record why and fall back to routine maintenance.
4. Then run the verification battery —
   - `python -m unittest discover tests/` (or `pytest tests/`)
   - `python -m ruff check .`
   - `python -m mypy . --exclude build --exclude dist`
   - `python tools/refresh_scaffold.py --check`
   - `python tools/verify_state_delta.py --full --record-full-suite`
   The full suite passed at the last checkpoint (`c12b652`: 11477 tests OK, skipped=4). Re-run only when the tree/HEAD moved since that checkpoint.
5. The library defect-hunt sweeps (bool-as-int, broad-except swallowing, silently ignored parameters, docstring-vs-implementation contracts via `tools/audit_contracts.py`, float/numeric edge cases, off-by-one boundaries) are complete with no open defect class; newly added modules get a first contract pass before the class is closed again. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`. Do not post duplicate/empty handoffs or commit no-op cycles.
