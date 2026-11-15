# Project Status

## Latest Session (2026-11-15T05:22Z)

- `board_read`: empty (no task posted to main). Executed prior handover: ran `python tools/verify_state_delta.py --probe` (rc=2, real delta from recorded checkpoint to HEAD auto-commit) then `--diff`, which passed the battery and advanced checkpoint to `67bd1d2`.
- Durable work in `memoize_utils`: clarified/documented `lru_memoize` decorator forms (`@lru_memoize`, `@lru_memoize()`, `@lru_memoize(maxsize=...)`, direct call with `maxsize`) and improved typing/factory validation. Added tests for bare-decorator keyword-order cache invariance, metadata/cache_clear preservation, and direct decoration with explicit `maxsize` (15 tests total). Refreshed embedded copies in `scaffold.sh`.
- `refresh_scaffold --check` in sync; `scan_untested` clean; targeted memoize lint/typecheck/tests passed. No high-leverage repository-managed **AVOIDABLE_PROCESS_DELAY** identified (probe/refresh/scan sub-second/cached; workflows maintainer-managed).

## State

- Working tree (pre-commit): `memoize_utils.py`, `tests/test_memoize_utils.py`, `scaffold.sh`, `CHANGELOG.md`, `.kilo/handover.md`, `PROJECT_STATUS.md` (non-workflow). CI auto-commits non-workflow changes.
- Checkpoint: `67bd1d2` (full suite recorded at `3d640fd`; tests/ changed since last recorded full-suite run — run `make test-full`/`python -m unittest discover tests/` if broader verification is required). Auto-commit will create a new HEAD; next probe returns rc=2 once before battery advances checkpoint.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=2 once after auto-commit, then advance via battery; later clean activations rc=0/1).
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits).
4. If none found, pick next evidence-backed defect/coverage fix (survey candidates: `ring_buffer_utils`, `priority_queue_utils`, other stateful helpers) — verify empirically before claiming a bug.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; run full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post`.