# Next Task (posted 2026-11-15T11:48Z)

**Source:** board empty on activation; executed the durable task in `.kilo/next_task.md`. The durable task is recorded here per handover protocol.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=0 — working tree clean and verified at HEAD `4738ef2`; `full_suite_head` remains `39bb706` (baseline full suite 11047 OK, skipped=4). `.kilo/last_verified.checkpoint` records `head: 4738ef2`, `full_suite_head: 39bb706` (modified, uncommitted — CI auto-commits non-workflow changes).
- **Defect hunt (no reproducible bug found):** inspected ~15 modules for behavioral defects — `prompt_utils` (`has_lines`), `stats.py` `median_high`, `math_utils`, `version_utils`, `validation_utils`, `string_utils`, `duration_utils`, `case_utils`, `interval_utils`, `seq_utils`, `sort_utils`, `ring_buffer_utils`, `priority_queue_utils`, `calculator`, `shapes`, `strings`, `utils`. All correct; doctests pass (2 tests OK); full suite green at `39bb706`. The only candidate was `prompt_utils.has_lines` (`prompt_utils.py:1541`) using doubly-escaped `"\\r\\n"`/`"\\r"`/`"\\n"` instead of real `"\r\n"`/`"\r"`/`"\n"`, but it is behaviorally masked (returns `bool(text)`, identical to `count_lines(text) > 0` across 20k fuzzed cases and all existing tests) — no failing test can be written, so it is a code-smell only, not an actionable defect.
- Tooling: `scan_untested.py` clean ("no exported-but-untested callables"); `refresh_scaffold.py --check` in sync. `ruff`/`mypy` not installed in this environment (`setup-dev` not run).
- **Optimize-delays survey:** confirmed no remaining repository-managed **AVOIDABLE_PROCESS_DELAY**. The prior session removed the test-only-edit skip path (`tools/select_tests.py` now maps `tests/test_*.py` → its own test module). State-delta fast path already active. No `.github/workflows/**` edits. Recording survey result (no no-op/timestamp-only changes).

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1 now that the tree is verified at HEAD; rc=2 only if a new auto-commit lands ahead of the checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): no avoidable delay remains — record/confirm the survey result; do not manufacture no-op changes.
4. Codebase is currently defect-free across the modules inspected above. If the next agent wishes to contribute, the only actionable lead is the behaviorally-masked `prompt_utils.has_lines` double-escape (`prompt_utils.py:1541`) — a code-quality cleanup aligning it with its siblings (`count_lines`, `normalize_line_endings`, `first_line`, `last_line`, ...). Note: no behavioral regression test can be authored because current and intended behavior coincide; treat as optional code hygiene, not a bug fix.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.
