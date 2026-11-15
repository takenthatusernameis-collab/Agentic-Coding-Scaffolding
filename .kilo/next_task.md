# Next Task (posted 2026-11-15T13:45Z)

**Source:** board empty on activation; executed the durable task in `.kilo/next_task.md`. The durable task is recorded here per handover protocol.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=1 on activation — working tree clean, no source-relevant file changed since the verified checkpoint `3c2f491`; verification battery skipped per the state-delta guard.
- **Fixed real defect:** `slugify_utils.slugify_many` rejected generators and sets despite an `Iterable[str]` signature. The docstring/type hint declare `texts: Iterable[str]`, but the implementation only accepted `list` and `tuple`, raising `TypeError("texts must be a list or tuple")` for any other iterable — a contract mismatch. The check now accepts any non-string/non-bytes iterable (`hasattr(texts, "__iter__")`), preserving per-item `str` validation and the empty-separator check; `str`/`bytes` are still rejected as iterables of characters.
- **Test rewrite:** `tests/test_slugify_utils.py` hard-imported `pytest` at module top, which is not installed in the CI runner, so `python -m unittest tests.test_slugify_utils` ran zero tests. Rewrote it as a unittest-native suite (`TestSlugify`, `TestIsSlug`, `TestDeslugify`, `TestTruncateSlug`, `TestSlugifyMany`) with coverage for list/tuple/generator/set acceptance, `str`/non-iterable/non-string-item rejection, empty-separator rejection, `is_slug` custom separator, `truncate_slug` bool-`max_length` rejection, zero-length truncation, and custom ellipsis.
- **Scaffold sync:** `python tools/refresh_scaffold.py` embedded the corrected `slugify_utils.py`, `tests/test_slugify_utils.py`, and `CHANGELOG.md`; `--check` reports all copies in sync.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta guard fast path active; no `.github/workflows/**` edits.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if board is empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0/1; rc=2 only if a new auto-commit lands ahead of the checkpoint).
3. Optimize-delays pass (`.kilo/command/optimize-delays.md`): no avoidable delay remains — record/confirm the survey; do not manufacture no-op changes.
4. Defect hunt: continue inspecting uninspected `*_utils.py` modules against their docstring/doctests. Look for literal-vs-real escape bugs, boundary/off-by-one errors, or contract mismatches. Only land a change you can demonstrate with a failing-then-passing test. If you edit a test module, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, and this durable next-task record; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.

(End of file - total 43 lines)