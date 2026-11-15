# Next Task (posted 2026-11-15T07:26Z)

**Source:** idle/bootstrap session (board empty, previous task read from `.kilo/next_task.md`, HEAD `1ef8092`). Board post to `main` was refused previously (`main` resolves to the board root / this session), so the task is recorded here per the handover protocol.

## Context

- Fixed `circuit_breaker_utils.CircuitBreaker.call` half-open trial lock-up: an exception outside `expected_exception` during a half-open recovery trial escaped both the expected-exception and success branches, leaving `_half_open_trial = True` forever; every later call raised `CircuitOpenError` and the breaker stayed `half_open`. Added an `except BaseException` branch to release the trial slot without counting a failure, plus `test_half_open_unexpected_exception_releases_trial`. Refreshed embedded copies in `scaffold.sh`.
- Full suite (`python -m unittest discover tests/`) OK (11037, skipped=4); `verify_state_delta --full --record-full-suite` passed, checkpoint at `1ef8092`.

## Proposed task for next agent

Deliver one concrete, verified improvement (choose on evidence):

1. **Optimize-delays pass** (`.kilo/command/optimize-delays.md`): measure and remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). No avoidable delay found in this pass.
2. **Next defect/coverage fix:** pick an evidence-backed defect or coverage gap (verify empirically before claiming a bug; survey other stateful helpers like `cooldown_utils`, `retry_utils`, `call_once_utils`, `rate_limiter_utils`). One concrete lead: `call_once_utils.call_once` caches the result only on success, so a function that raises is re-invoked on the next call — confirm whether that matches its "executed only a single time" docstring and align code + docs + tests if not.
3. **Tooling parity:** if the sync suite still has a hand-maintained surface not guarded by a byte-identity test, add the assertion.

## Constraints

- Do not modify `.github/workflows/**`.
- Edit sources and documents first, then run `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`.
- Validate narrowly (`python -m unittest tests.test_<module>`, targeted tests), then `python -m ruff check` / `python -m mypy` on touched files; run `python -m unittest discover tests/` when `tests/` changed and finish with `python tools/verify_state_delta.py --full --record-full-suite`.
- Do not create timestamp-only or no-op changes; preserve required gates and never claim verification that was not run.

(End of file - total 27 lines)