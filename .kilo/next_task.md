# Next Task (posted 2026-11-15T11:58Z)

**Source:** board empty on activation; executed the durable task in `.kilo/next_task.md`. The durable task is recorded here per handover protocol.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=1 — working tree clean, no source-relevant change since checkpoint `4738ef2`; HEAD was `fa0e6cf`. `.kilo/last_verified.checkpoint` now records `head: fa0e6cf`, `full_suite_head: fa0e6cf`.
- **Fixed real defect:** `prompt_utils.has_lines` (`prompt_utils.py:1541-1542`) normalized/split on literal backslash escapes `"\\r\\n"`/`"\\n"`/`"\\r"` instead of real `"\r\n"`/`"\n"`/`"\r"`, diverging from siblings `count_lines`/`first_line`/`last_line`/`normalize_line_endings`. Behaviorally masked (`== bool(text)` for all inputs) so no failing test was possible beforehand; still a latent correctness trap. Now uses real escapes; added `test_line_endings` (CRLF, lone CR, lone newline).
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta fast path active; no `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1; rc=2 only if a new auto-commit lands ahead of the checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): no avoidable delay remains — record/confirm the survey; do not manufacture no-op changes.
4. Defect hunt: `prompt_utils.has_lines` is fixed. Inspect an uninspected `*_utils.py` module (candidates: `secrets_utils`, `hmac_utils`, `base64_utils`, `semver_utils`, `slugify_utils`, `roman_utils`, `case_utils`, `duration_utils`) against its docstring/doctests. Look for literal-vs-real escape bugs, boundary/off-by-one errors, or contract mismatches. Only land a change you can demonstrate with a failing-then-passing test.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.