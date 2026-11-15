# Next Task (posted 2026-11-15T08:37Z)

**Source:** bootstrap session (board empty, executed task from previous `.kilo/next_task.md`, HEAD `222f2bf`). Board post to `main` was refused in this environment (`main` resolves to board root/self), so the durable task is recorded here per handover protocol (and posted to `main` where accepted).

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=1 at start (clean working tree, no source-relevant changes since last verified checkpoint; redundant verification battery correctly skipped).
- **Stateful-helper survey (evidence-backed, no defect found):**
  - `call_once_utils`: caches first result or exception and re-raises without re-invoking (including `BaseException` paths exercised); `reset()` clears cached state. Tests: 6 OK.
  - `cooldown_utils`: records last-call when interval elapsed even if the wrapped call raises (caller consumes the slot), which matches its rate-limiting contract; `ready/remaining/reset` consistent. Tests: 17 OK.
  - `retry_utils`: validates args (`max_attempts>=1`, non-negative delays/backoff, tuple exceptions) and retries only specified exceptions with configured backoff/jitter behavior. Tests: 39 OK.
  - `rate_limiter_utils`: `acquire` rejects negative tokens and requests above capacity; `acquire_blocking` raises for unsatisfiable requests; decorator acquires before call (token consumed on failure by design). Tests: 11 OK.
  - `memoize_utils`/`lru_memoize`: cache on success only; exceptions not cached and recomputed on next call (empirically confirmed). Tests: 13 OK.
- Tooling: `python tools/scan_untested.py` — no exported-but-untested callables. `python tools/refresh_scaffold.py --check` — in sync. Targeted suite for surveyed modules: 86 tests OK.
- **Optimize-delays pass:** no repository-managed AVOIDABLE_PROCESS_DELAY identified (state-delta probe already avoids redundant battery on clean activations; CI/workflow gates are maintainer-managed and unchanged). No `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1 on a clean, unchanged activation). Do not rerun the full battery or full test suite without a state delta or explicit need.
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): identify and remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). If none found, record the survey result (do not create no-op/timestamp-only changes).
4. If no avoidable delay remains, pick the next evidence-backed defect, edge-case hardening, or coverage gap: reproduce empirically first, prefer stateful/concurrency-sensitive helpers or tooling parity issues, and verify the fix with targeted tests plus `ruff`/`mypy` on touched files. Run `python -m unittest discover tests/` and `python tools/verify_state_delta.py --full --record-full-suite` when `tests/` or shared behavior changes.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (not for survey-only handoffs), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.
