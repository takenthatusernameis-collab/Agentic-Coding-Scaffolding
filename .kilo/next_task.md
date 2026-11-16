# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=0/1 once the tree is committed (checkpoint `9d3451b`, full-suite provenance recorded). Avoid redundant full runs once the checkpoint matches source-relevant state.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey.
4. Defect hunt: `python -m ruff check .` and `python -m mypy . --exclude build --exclude dist` if source changed or confidence needed. `python tools/scan_untested.py` reports zero gaps. Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification. Next uninspected `*_utils.py` batch (alphabetical continuation after `url`): `urllib`, `uu`, `uuid`, `validation`, `venv`, `version`, `warnings`, `wave`, `weakref`, `webbrowser`.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.

(End of file - total 8 lines)