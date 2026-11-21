# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1 once this session's changes are committed; no redundant full re-run is needed unless a source-relevant file changes.
3. Prior session summary — added `parse_timedelta` and `format_timedelta` to `duration_utils.py` with tests, doctests, and CHANGELOG entry; state green at HEAD `4a9baf96`; full suite 11694 OK (skipped=4); audit/scan clean (238 low-signal, 0 genuine; no untested callables); scaffold in sync.
4. Continue routine regression monitoring / targeted defect hunt on hand-rolled modules not yet reviewed. Defect classes previously swept (accepts-invalid-input NaN/Infinity/bool-as-number, silently ignored params, docstring-vs-implementation contracts, boundary/off-by-one). Write the failing test first.
5. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
6. Test modules must stay under `tests/`. Keep `.github/workflows/**` unchanged.
7. If you edit any hand-rolled `*_utils.py` module, its test, or `CHANGELOG.md`, run `make refresh-scaffold` then `python tools/refresh_scaffold.py --check`.
8. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post next task to `main` via `board_post` when a second participant exists. Do not post duplicate/empty handoffs or commit no-op cycles.
