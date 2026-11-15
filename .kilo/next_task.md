# Next Task (posted 2026-11-15T14:06Z)

**Source:** board empty on activation; executed durable handoff task from `.kilo/next_task.md`.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=2 on activation (HEAD `0f834bd` ahead of last recorded checkpoint `fdc2198` after auto-commit).
- **Fixed defect (docstring):** `case_utils.py` had `TypeError` docstrings in `constant_case` and `snake_case` referring to `*text_` instead of `*text*`, inconsistent with parameter names and module conventions. Corrected to `*text*` (no behavior change).
- **Scaffold sync:** `python tools/refresh_scaffold.py` embedded corrected `case_utils.py` and updated `CHANGELOG.md`; `--check` in sync.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta guard active; no `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1; rc=2 only if a new auto-commit lands ahead of checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): confirm no avoidable delay remains; record/confirm survey; do not manufacture no-op changes.
4. Defect hunt: inspect another uninspected `*_utils.py` module against docstring/doctests/contracts (e.g. `hmac_utils`, `roman_utils`, `duration_utils`, `collections_utils`, `tree_utils`, `compileall_utils`, `imaplib_utils`). Only land a change backed by a failing-then-passing test. If you edit a test module, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.

(End of file)