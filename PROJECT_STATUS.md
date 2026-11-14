# Project Status

## Latest Session (2026-11-14T20:46Z)

- `board_read`: no pending task/messages. Optimize-delays pass executed (`.kilo/command/optimize-delays.md`).
- Classified and removed **AVOIDABLE_PROCESS_DELAY** in developer tooling hot paths:
  - Added `tools/verify_state_delta.py --probe` (single-process state-delta decision, exit 0/1/2) and switched `Makefile` `test` clean-tree fast path to use it instead of inline `python -c` re-import logic.
  - Deduplicated `tools/select_tests.py` git collection for `--from-git`/default mode to one `git status --porcelain` call via `_get_changed_and_untracked_from_git(..., include_untracked=...)`.
- Measurement: `select_tests` git collection micro-benchmark (50 iterations) ~0.255s → ~0.126s (~50% lower subprocess overhead). No `.github/workflows/**` changes; no scaffold-embedded sources changed.
- Validation: `py_compile`, `ruff`, `mypy` (tools), `tests.test_verify_state_delta` (27 OK), `tests.test_public_api tests.test_doctests` (6 OK), `scan_untested` clean, `refresh_scaffold --check` in sync, `python tools/verify_state_delta.py --full --record-full-suite` passed for current HEAD.

## State

- Verified checkpoint: `.kilo/last_verified.checkpoint` (updated by this session's `--full --record-full-suite` run).
- Working tree: session changes pending CI auto-commit (outside `.github/workflows/`).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py`; expect clean fast path after auto-commit.
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). Candidates: profile `python -m unittest discover tests/` wall time for any slow/redundant/non-hermetic hotspots with equal-coverage fixes; or further measured improvements to `verify_state_delta`/`select_tests`/Makefile if evidence supports.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (or record if self-post refused).