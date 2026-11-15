# Next Task (posted 2026-11-15T10:47Z)

**Source:** board empty on activation; executed the durable task in `.kilo/next_task.md`. The durable task is recorded here per handover protocol and posted to `main` where accepted.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=2 at start — HEAD `39bb706` was ahead of the `da4af7f` checkpoint (previous session's `tools/verify_state_delta.py` + `tests/test_verify_state_delta.py` were committed after the checkpoint). Battery passed; checkpoint advanced to `39bb706`. Baseline full suite 11043 OK (skipped=4).
- **Defect fixed (evidence-backed, tooling parity):** `tools/select_tests.py` mapped a changed `tests/test_*.py` file to `None`. Reproduced with `python tools/select_tests.py --changed-files tests/test_abc_utils.py` (no output). `map_source_to_test` handled only `tools/*.py` and root-level source modules, so a `tests/` path matched neither branch and `select_tests` emitted no targeted module; `make test` then ran only the smoke test, so a test-only edit was silently not exercised locally. A test file now maps to its own module (`tests.test_abc_utils`); non-test helpers under `tests/` are still ignored. Added regression tests at the mapping, `select_tests(...)`, and `--changed-files` CLI levels, and replaced the old assertion that a test file maps to `None`.
- Tooling: `scan_untested.py` clean; `refresh_scaffold.py --check` in sync (embedded `CHANGELOG.md` refreshed). `ruff`/`mypy` not installed here.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=2 on the first activation after the auto-commit, then rc=0/1 once re-verified at the new HEAD). Do not rerun the full battery/suite without a state delta or explicit need.
3. Continue the optimize-delays pass (`.kilo/command/optimize-delays.md`): identify and remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). If none, record the survey result (no no-op/timestamp-only changes).
4. If no avoidable delay remains, pick the next evidence-backed defect, edge-case hardening, or coverage gap: reproduce empirically first, prefer stateful/concurrency-sensitive helpers or tooling parity issues, verify with targeted tests plus `ruff`/`mypy` on touched files when available. Run `python -m unittest discover tests/` and `python tools/verify_state_delta.py --full --record-full-suite` when `tests/` or shared behavior changes.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.