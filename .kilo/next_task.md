# Next Task (posted 2026-11-15T08:26Z)

**Source:** bootstrap session (board empty, previous task read from `.kilo/next_task.md`, HEAD `0576ce4`). Board post to `main` was refused (`main` resolves to the board root / this session), so the task is recorded here per the handover protocol.

## Context

- **Fixed scaffold sync**: `make refresh-scaffold` updated embedded copies of `call_once_utils.py` and `tests/test_call_once_utils.py` in `scaffold.sh` (they were stale from a previous edit).
- **Full quality gate pass**:
  - `make test-full` — 11039 OK (skipped=4)
  - `make lint` — All checks passed
  - `make typecheck` — Success (only annotation-unchecked notes in test files)
  - `python tools/refresh_scaffold.py --check` — In sync
  - `python tools/verify_state_delta.py` — Checkpoint advanced to `0576ce4757a25abaf7efe2caa0b650288abcfdc8`
  - `python tools/scan_untested.py` — No exported-but-untested callables
- **Investigated next-task candidates from previous handover**:
  1. `call_once_utils` exception caching: **Already correct** — implementation caches exceptions on first failure and re-raises without re-invoking (test `test_exception_is_cached_not_re_invoked` passes; docstring lines 30-34 confirm this contract).
  2. Other stateful helpers (`cooldown_utils`, `retry_utils`, `rate_limiter_utils`): All 65 tests pass; no defects found.
  3. Tooling parity: All four hand-maintained surfaces (README.md, AGENTS.md, CHANGELOG.md, pyproject.toml) guarded by byte-identity checks in `test_scaffold_sync.py`.
  4. Optimize-delays pass: **No avoidable process delay found**. CI workflow is maintainer-managed; test selection via `verify_state_delta` already skips redundant work on clean activations.

## Proposed Task for Next Agent

Deliver one concrete, verified improvement (choose on evidence):

1. **Optimize-delays pass** (`.kilo/command/optimize-delays.md`): Measure and remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). If none found, document the survey.
2. **Next defect/coverage fix**: Pick an evidence-backed defect or coverage gap (verify empirically before claiming a bug; survey stateful helpers and any module with complex state).
3. **Tooling parity**: If the sync suite still has a hand-maintained surface not guarded by a byte-identity test, add the assertion.

## Constraints

- Do not modify `.github/workflows/**`.
- Edit sources and documents first, then run `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`.
- Validate narrowly (`python -m unittest tests.test_<module>`, targeted tests), then `python -m ruff check` / `python -m mypy` on touched files; run `python -m unittest discover tests/` when `tests/` changed and finish with `python tools/verify_state_delta.py --full --record-full-suite`.
- Do not create timestamp-only or no-op changes; preserve required gates and never claim verification that was not run.

(End of file - total 38 lines)