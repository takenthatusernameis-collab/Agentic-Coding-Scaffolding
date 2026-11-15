# Project Status

## Latest Session (2026-11-15T02:39Z)

- `board_read`: empty (no task posted to main); executed the standing avoidable-delay task from the durable handover.
- Ran checkpoint gate from prior state: `python tools/verify_state_delta.py` (battery passed, checkpoint advanced to `cfe7056078c299a8d1b04a7cf8fca32f7a2d344f`). `refresh_scaffold --check` and `scan_untested.py` clean at start.
- **Optimization — `tools/verify_state_delta.py` clean-tree delta computed once.** Removed redundant delta recomputation on the clean-tree/HEAD-advanced skip path: `main` now uses a single `_changed_and_untracked_since(marker["head"])` call for both `--diff` listing and skip decision instead of `diff_since` + `untracked_source_files` (eliminates an extra `git diff` + `git status` pair per activation). Updated `tests/test_verify_state_delta.py::TestCleanDeltaFastPath` accordingly.
- Refreshed `scaffold.sh` embedded copies after doc/tool edits; `python tools/refresh_scaffold.py --check` in sync.
- Validation: `python -m pytest tests/test_verify_state_delta.py` — 30 OK; `python tools/scan_untested.py` clean; `python -m ruff check .` clean; `python -m mypy . --exclude build --exclude dist` clean (567 source files); `python tools/refresh_scaffold.py --check` in sync.

## State

- Working tree: `tools/verify_state_delta.py`, `tests/test_verify_state_delta.py`, `CHANGELOG.md`, `scaffold.sh`, `.kilo/handover.md`, `PROJECT_STATUS.md` modified (non-workflow). CI auto-commits non-workflow changes.
- `python tools/verify_state_delta.py --probe` => rc=2 for this delta before running the battery; run `python tools/verify_state_delta.py` once to verify/advance checkpoint.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect battery run for this delta, then clean/verified fast path after auto-commit).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). Measure candidates with evidence before changing.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).
