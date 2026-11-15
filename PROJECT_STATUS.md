# Project Status

## Latest Session (2026-11-15T05:34Z)

- `board_read`: empty (no task posted to main). `verify_state_delta --probe` rc=2 after prior auto-commit; `verify_state_delta` battery advanced checkpoint to `f6a59e7`. `refresh_scaffold --check` in sync, `scan_untested.py` clean.
- **Durable work — `ring_buffer_utils.RingBuffer.from_list` empty-iterable contract clarified.** `from_list([])` with no explicit `capacity` now raises `ValueError("capacity must be provided when items is empty")` instead of the misleading `ValueError("capacity must be greater than 0")`; `from_list([], capacity=n)` remains supported. Added `test_from_list_empty_requires_capacity`, `test_from_list_empty_with_explicit_capacity`. Refreshed embedded copies in `scaffold.sh`.
- Targeted verification: `python -m unittest tests.test_ring_buffer_utils -v` (13 OK), `python -m ruff check ring_buffer_utils.py tests/test_ring_buffer_utils.py` (clean), `python -m mypy ring_buffer_utils.py tests/test_ring_buffer_utils.py` (clean), `python tools/refresh_scaffold.py --check` (in sync). Full suite not rerun (source-local change; `tests/` changed since last recorded full-suite run per checkpoint note — consider full suite at next milestone).

## State

- Working tree (pre-commit): `ring_buffer_utils.py`, `tests/test_ring_buffer_utils.py`, `CHANGELOG.md`, `scaffold.sh`, `.kilo/handover.md`, `PROJECT_STATUS.md` (non-workflow). CI auto-commits non-workflow changes.
- Checkpoint: `f6a59e7` (verification battery passed this session; full-suite head recorded earlier at `e3eacdb`, `tests/` changed since then).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=2 once after auto-commit; run battery to advance, then rc=0/1 on clean activations).
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits).
4. If none found, pick next evidence-backed defect/coverage fix (survey stateful helpers like `cooldown_utils`, `retry_utils`, `cache_utils`, etc.) — verify empirically before claiming a bug.
5. Validation: edit sources/docs first, then `python tools/refresh_scaffold.py` and `--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`/`python -m ruff check`, `make typecheck`/`python -m mypy` on changed files; run full suite when `tests/` or shared behavior changed and record with `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post`.

(End of file - total 27 lines)