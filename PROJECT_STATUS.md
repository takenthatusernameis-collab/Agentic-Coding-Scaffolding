# Project Status

## Latest Session (2026-11-15T10:47Z)

- `board_read`: empty (no task posted to main); executed the durable task in `.kilo/next_task.md`.
- **State delta:** probe rc=2 at start (HEAD `39bb706` was ahead of the `da4af7f` checkpoint after the previous session's `verify_state_delta` changes were committed). Battery passed; checkpoint advanced to `39bb706`. Baseline full suite: 11043 OK (skipped=4).
- **Fix (tooling parity + delay removal):** `tools/select_tests.py` mapped a changed `tests/test_*.py` file to `None`. Reproduced: `python tools/select_tests.py --changed-files tests/test_abc_utils.py` produced no output, so `make test` fell back to the smoke test and never ran the edited test locally. A test file now maps to its own test module (`tests/test_abc_utils.py` → `tests.test_abc_utils`); non-test helpers under `tests/` stay ignored. Added regression tests at the mapping, `select_tests(...)`, and `--changed-files` CLI levels.
- **Optimize-delays:** the removed avoidable delay is the test-only edit path that silently skipped the edited test until the next full-suite milestone; state-delta fast path already active; workflow/CI gates maintainer-managed. No `.github/workflows/**` edits.

## State

- Working tree (pre-commit): `tools/select_tests.py`, `tests/test_select_tests.py`, `CHANGELOG.md`, `scaffold.sh`, `.kilo/last_verified.checkpoint`, plus handoff docs.
- Checkpoint: `39bb706` (`head`/`full_suite_head`); re-verifies at the next committed HEAD.
- Validation: full suite 11047 OK (skipped=4); targeted `tests.test_select_tests tests.test_verify_state_delta tests.test_scaffold_sync tests.test_doctests` 115 OK; `scan_untested.py` clean; `refresh_scaffold.py --check` in sync. `ruff`/`mypy` unavailable in this environment.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=2 right after the auto-commit, then rc=0/1 once re-verified).
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits).
4. Otherwise pick the next evidence-backed defect/coverage/tooling-parity fix — reproduce empirically before claiming a bug.
5. If embedded sources changed: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update durable handoff docs and `CHANGELOG.md` (then refresh scaffold); post next task to `main` via `board_post`.