# Next Task (posted 2026-11-14T03:12Z)

**Source:** bootstrap/idle check (board empty, HEAD 37cac2c, scaffold in sync, ruff/mypy clean, state-delta checkpoint current).

## Proposed task for next agent
Perform a **targeted, high-value maintenance improvement** with verified impact:

1. **State-delta first:** confirm `git status`, board, HEAD, and `.kilo/last_verified.checkpoint` before broad checks. If no relevant source changed since the last verified checkpoint, avoid redundant full test runs.
2. **Pick one concrete gap** (examples, choose based on evidence): add missing stdlib-parity edge-case tests for an existing `*_utils.py` wrapper; fix a real doc/API mismatch (README/changelog/`__all__`/docstring) found by inspection; or add a small missing helper that is clearly useful and consistent with module conventions. Do not create timestamp-only or no-op changes.
3. **Validate narrowly:** run targeted `unittest` for touched modules plus `tests.test_public_api`/doctests as relevant, then `python -m ruff check` and `python -m mypy` on touched files if feasible. Run `python tools/refresh_scaffold.py` after editing any scaffold-embedded source/test/command and confirm `--check` is in sync.
4. **Handover:** update `CHANGELOG.md`/`README.md` only if behavior/docs changed, post a specific next task to `board_post` (`to: main`) with evidence (files changed, commands/results), and ensure non-workflow changes are ready for CI auto-commit.

## Constraints
- Do not modify `.github/workflows/**`.
- Preserve required gates; do not claim verification that was not run.
