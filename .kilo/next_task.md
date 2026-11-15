# Next Task (posted 2026-11-15T10:43Z)

**Source:** bootstrap-style activation (board empty, executed task from previous `.kilo/next_task.md`). The durable task is recorded here per handover protocol and posted to `main` where accepted.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=2 at start — a genuine delta: `tools/select_tests.py` + `tests/test_select_tests.py` were committed at HEAD `da4af7f` after the `222f2bf` checkpoint without advancing it. Battery passed; checkpoint advanced to `da4af7f`. Baseline full suite 11042 OK (skipped=4).
- **Defect fixed (evidence-backed):** `tools/verify_state_delta.py` printed a spurious "tests/ changed since last recorded full-suite run" note immediately after `--record-full-suite` because the note read the pre-update `marker` instead of the freshly written `new_marker` (cited the old `full_suite_head`). Reproduced with a throwaway marker; fixed by `marker = new_marker` after `write_marker`; regression `test_record_full_suite_note_uses_the_freshly_recorded_head`. This removes an avoidable redundant full-suite re-run prompt.
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