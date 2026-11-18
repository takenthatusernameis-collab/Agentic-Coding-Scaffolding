# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`.
3. Continue the correctness defect hunt (failing-test-first). The silently-ignored-parameter class is now fully swept across all candidate modules with no high-confidence defect found. Next class to investigate: **silently ignored parameters in the top-level non-`*_utils` modules** — `hello.py`, `calculator.py`, `shapes.py`, `stats.py`, `strings.py`, `utils.py`, `greeting_utils.py`. Audit each function's signature/docstring against its body, then fix one with a failing test.
4. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry.
5. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.

(End of file - total 7 lines)