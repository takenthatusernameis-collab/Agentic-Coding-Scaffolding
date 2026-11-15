# Project Status

## Latest Session (2026-11-15T08:37Z)

- `board_read`: empty (no task posted to main); executed task from `.kilo/next_task.md`. `python tools/verify_state_delta.py --probe` rc=1 at start (clean, no source-relevant delta; redundant verification battery skipped).
- **Survey (no code change required):** reviewed `call_once_utils`, `cooldown_utils`, `retry_utils`, `rate_limiter_utils`, `memoize_utils` against behavior/contracts and tests. No evidence-backed defect found. Targeted tests run: 86 OK. `scan_untested.py` clean; `refresh_scaffold.py --check` in sync.
- **Optimize-delays:** no repository-managed AVOIDABLE_PROCESS_DELAY identified this pass (state-delta fast path in place; workflow/CI maintainer-managed). No `.github/workflows/**` edits.

## State

- Working tree (pre-commit): `.kilo/handover.md`, `.kilo/next_task.md`, `PROJECT_STATUS.md` updated (durable handoff/survey only).
- Checkpoint: `222f2bf` (last verified HEAD recorded in `.kilo/last_verified.checkpoint`).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1 on clean activation).
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). If none found, avoid no-op changes.
4. If none found, pick next evidence-backed defect/coverage/tooling-parity fix — verify empirically before claiming a bug.
5. Validation: edit sources/docs first, then `python tools/refresh_scaffold.py` and `--check` when embedded sources changed; `scan_untested.py`, targeted tests, `ruff`/`mypy` on changed files; run full suite and `verify_state_delta.py --full --record-full-suite` when `tests/` or shared behavior changed.
6. Keep `.github/workflows/**` unchanged; update durable handoff docs and post next task to `main` via `board_post`.
