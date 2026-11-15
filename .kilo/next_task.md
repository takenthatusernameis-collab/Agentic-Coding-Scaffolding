# Next Task (posted 2026-11-15T14:46Z)

**Source:** board empty on activation; executed durable handoff task from `.kilo/next_task.md`.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=1 (HEAD `7dc8a9f` matches checkpoint; working tree changed during session).
- **Fixed defect (docstring):** `hmac_utils.py` had markup typos in `hmac_sha1` (`*key.` → `*key*`) and `verify` (`*algorithm.` → `*algorithm*`) docstrings. Corrected (no behavior change).
- **Scaffold sync:** `python tools/refresh_scaffold.py` embedded corrected `hmac_utils.py` and updated `CHANGELOG.md`; `--check` in sync.
- **Validation:** `python -m doctest hmac_utils.py` clean; `python -m unittest tests.test_hmac_utils` 24 OK; `python -m unittest tests.test_public_api` OK. `ruff`/`mypy` unavailable. Full-suite not re-run for targeted doc-only fix.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta guard active; no `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=1 before commit of this session's changes; rc=2 only if a new auto-commit lands ahead of checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): confirm no avoidable delay remains; record/confirm survey; do not manufacture no-op changes.
4. Defect hunt: inspect another uninspected `*_utils.py` module against docstring/doctests/contracts (e.g. `roman_utils`, `duration_utils`, `collections_utils`, `tree_utils`, `compileall_utils`, `imaplib_utils`). Only land a change backed by a failing-then-passing test or a clearly incorrect docstring/contract issue with targeted verification. If you edit a test module, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.

(End of file)