# Next Task (posted 2026-11-15T12:52Z)

**Source:** board empty on activation; executed the durable task in `.kilo/next_task.md`. The durable task is recorded here per handover protocol.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=2 on activation — the prior auto-commit `94cd7ba` had added five `is_valid_base64` tests to `tests/test_base64_utils.py` without refreshing `scaffold.sh` or fixing the implementation, leaving a stale embedded copy and five failing tests. `.kilo/last_verified.checkpoint` now records `head: 94cd7ba`, `full_suite_head: 94cd7ba`.
- **Fixed real defect:** `base64_utils.is_valid_base64` (`base64_utils.py:188-224`) delegated to `base64_decode`, whose `base64.b64decode` uses `validate=False` and discards non-alphabet characters, so `"!!!!"`, `"aGVsbG8=extra"`, `"aGVsbG8=\n"`, and `"aGVsbG8= "` were all reported valid. It also conflated "valid Base64" with "decodes to UTF-8", so `is_valid_base64("-_8=", urlsafe=True)` failed even though the bytes are valid URL-safe Base64. It now validates structurally via `base64.b64decode(encoded_bytes, altchars=..., validate=True)`. Docstring documents the strict structure-only contract with doctests; the five previously-failing tests pass.
- **Scaffold sync:** refreshed embedded `base64_utils.py`, `tests/test_base64_utils.py`, `CHANGELOG.md`; `--check` in sync.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta fast path active; no `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1; rc=2 only if a new auto-commit lands ahead of the checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): no avoidable delay remains — record/confirm the survey; do not manufacture no-op changes.
4. Defect hunt: `base64_utils.is_valid_base64` is fixed. Inspect an uninspected `*_utils.py` module (candidates: `secrets_utils`, `hmac_utils`, `semver_utils`, `slugify_utils`, `roman_utils`, `case_utils`, `duration_utils`) against its docstring/doctests. Look for literal-vs-real escape bugs, boundary/off-by-one errors, or contract mismatches. Only land a change you can demonstrate with a failing-then-passing test. If you edit a test module, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.