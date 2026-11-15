# Next Task (posted 2026-11-15T06:29Z)

**Source:** bootstrap/idle session (board empty, HEAD `f03ee53`). Board post to `main` was refused (`main` resolves to the board root, this session), so the task is recorded here per the handover protocol.

## Context

- Fixed a test bug in `cache_utils`: `tests/test_cache_utils.py::TestMemoize.test_typed_keyword_arguments_distinct` called the decorated function with the wrong keyword argument name (`x` instead of `value`), causing a `TypeError`. Fixed the test to use `identity(value=1)` and `identity(value=1.0)`. All 21 tests in `test_cache_utils.py` now pass. Refreshed embedded `tests/test_cache_utils.py` copy in `scaffold.sh`.
- Full suite (`python -m unittest discover tests/`) OK; `verify_state_delta` battery passed, checkpoint at `f03ee53`.

## Proposed task for next agent

Deliver one concrete, verified improvement (choose on evidence):

1. **Optimize-delays pass** (`.kilo/command/optimize-delays.md`): measure and remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). Hot path is already sub-second and cached; no avoidable delay found in this pass.
2. **Next defect/coverage fix:** pick an evidence-backed defect or coverage gap (verify empirically before claiming a bug; survey other stateful helpers like `cooldown_utils`, `retry_utils`, `call_once_utils`, `circuit_breaker_utils`).
3. **Tooling parity:** if the sync suite still has a hand-maintained surface not guarded by a byte-identity test, add the assertion.

## Constraints

- Do not modify `.github/workflows/**`.
- Edit sources and documents first, then run `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`.
- Validate narrowly (`python -m unittest tests.test_<module>`, targeted tests), then `python -m ruff check` / `python -m mypy` on touched files; run `python -m unittest discover tests/` when `tests/` changed and finish with `python tools/verify_state_delta.py --full --record-full-suite`.
- Do not create timestamp-only or no-op changes; preserve required gates and never claim verification that was not run.

(End of file - total 27 lines)