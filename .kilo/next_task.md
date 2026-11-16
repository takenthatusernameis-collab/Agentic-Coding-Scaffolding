# Next Task

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=0/1 (checkpoint `4a1e7f4`, HEAD `c4154b4`, no source-relevant delta). Avoid redundant full runs once the checkpoint matches source-relevant state.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey.
4. Defect hunt: `pip install ruff mypy` if absent, then `ruff check .` and `mypy . --exclude build --exclude dist`. `python tools/scan_untested.py` reports zero gaps. Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification. Next uninspected `*_utils.py` batch (alphabetical continuation after `stringprep`): `string`, `stringprep`, `sys`, `sysconfig`, `syslog`, `tabnanny`, `tarfile`, `telnetlib`, `temp`, `tempfile`. Optional: none outstanding.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.