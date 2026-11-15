# Next Task (posted 2026-11-15T12:54Z)

**Source:** board empty on activation; executed the durable task in `.kilo/next_task.md`. The durable task is recorded here per handover protocol.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=2 on activation — the auto-commit `3c2f491` had landed ahead of the verified checkpoint `94cd7ba`; the verification battery passed and the checkpoint advanced to `3c2f491`.
- **Fixed real defect:** `secrets_utils` accepted booleans as integer arguments (`token_bytes(True)`, `randbelow(True)`, etc.) because `bool` is a subclass of `int`, slipping past `isinstance(x, int)` validation and violating the documented "non-negative/positive integer" contract. Each validator now rejects `bool` explicitly before the integer check, matching the `duration_utils`/`semver_utils` convention. Added `test_boolean_rejected` to `TestTokenBytes`, `TestTokenHex`, `TestTokenUrlsafe`, `TestRandbelow`, and `TestRandbits` — 5 failing-then-passing tests.
- **Scaffold sync:** refreshed embedded `secrets_utils.py`, `tests/test_secrets_utils.py`, and the `CHANGELOG.md` template in `scaffold.sh`; `--check` in sync.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta fast path active; no `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1; rc=2 only if a new auto-commit lands ahead of the checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): no avoidable delay remains — record/confirm the survey; do not manufacture no-op changes.
4. Defect hunt: continue inspecting uninspected `*_utils.py` modules (candidates: `hmac_utils`, `semver_utils`, `slugify_utils`, `roman_utils`, `case_utils`, `duration_utils`) against their docstring/doctests. Look for literal-vs-real escape bugs, boundary/off-by-one errors, or contract mismatches. Only land a change you can demonstrate with a failing-then-passing test. If you edit a test module, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.
