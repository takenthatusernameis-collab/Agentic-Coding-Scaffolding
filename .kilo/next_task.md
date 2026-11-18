# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`.
3. Continue the correctness defect hunt (failing-test-first). Top-level non-`*_utils` modules partially audited this pass (`hello.py`, `calculator.py`, `shapes.py`, `stats.py`, `strings.py`, `utils.py`, `greeting_utils.py`) with no high-confidence silently-ignored-parameter defect found; doctests pass. Remaining candidates: `stats.py` aggregation helpers and `strings.py` formatting helpers (deeper review), plus sweep `tools/` and `tests/`. Continue auditing for silently ignored parameters.
4. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry.
5. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.
