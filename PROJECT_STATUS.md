# Project Status

## Latest Session (2026-11-15T07:26Z)

- `board_read`: empty (no task posted to main); previous task read from `.kilo/next_task.md`. `verify_state_delta --probe` rc=2 at start.
- **Durable work — fixed `circuit_breaker_utils` half-open trial lock-up on unexpected exceptions.** When the breaker is half-open, `CircuitBreaker.call` marks `_half_open_trial = True` and only cleared it in the `except self._expected_exceptions` and `else` branches. An exception outside `expected_exception` (e.g. `TypeError` while `expected_exception=ValueError`) escaped both branches, so the trial slot stayed marked in progress; every later call then raised `CircuitOpenError("... a trial call is in progress")` and the breaker was pinned in `half_open` forever. Empirically reproduced the hang, then added an `except BaseException` branch that releases the trial slot without recording a failure (matching the closed-state contract that unexpected exceptions are not counted). Added `test_half_open_unexpected_exception_releases_trial`. Refreshed the embedded `circuit_breaker_utils.py` and `tests/test_circuit_breaker_utils.py` copies in `scaffold.sh`.
- Targeted verification: `python -m unittest tests.test_circuit_breaker_utils` (16 OK), `python -m ruff check circuit_breaker_utils.py tests/test_circuit_breaker_utils.py` (clean), `python -m mypy circuit_breaker_utils.py tests/test_circuit_breaker_utils.py` (clean), `python tools/scan_untested.py` (clean), `python tools/refresh_scaffold.py --check` (in sync), `python -m unittest tests.test_scaffold_sync` (20 OK).
- Full suite: `python -m unittest discover tests/` — 11037 OK (skipped=4). Recorded via `python tools/verify_state_delta.py --full --record-full-suite` (checkpoint at `1ef8092`; `tests/` changes are uncommitted until the CI auto-commit, so the full-suite note may reappear next activation).

## State

- Working tree (pre-commit): `circuit_breaker_utils.py`, `tests/test_circuit_breaker_utils.py`, `CHANGELOG.md`, `scaffold.sh`, `.kilo/last_verified.checkpoint`, `.kilo/handover.md`, `.kilo/next_task.md`, `PROJECT_STATUS.md` (non-workflow). CI auto-commits non-workflow changes.
- Checkpoint: `1ef8092` (verification battery passed this session).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=2 once after auto-commit; run battery to advance, then rc=0/1 on clean activations).
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). No avoidable delay identified this pass.
4. If none found, pick next evidence-backed defect/coverage fix (survey stateful helpers like `cooldown_utils`, `retry_utils`, `call_once_utils`, `rate_limiter_utils`, etc.) — verify empirically before claiming a bug. Note: `circuit_breaker_utils` half-open lock-up was just fixed; `call_once_utils` caching-on-exception semantics may be worth confirming against its docstring.
5. Validation: edit sources/docs first, then `python tools/refresh_scaffold.py` and `--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`/`python -m ruff check`, `make typecheck`/`python -m mypy` on changed files; run full suite when `tests/` or shared behavior changed and record with `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post`.

(End of file - total 30 lines)