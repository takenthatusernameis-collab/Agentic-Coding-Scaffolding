# Next Task

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe` before/after work as needed; interpret rc per tool semantics (0/1/2) and avoid redundant full runs when the checkpoint already matches. If rc=2, run the battery once (e.g. `--diff`) and proceed.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey.
4. Defect hunt: `pip install ruff mypy` (not installed by default in the CI runner, so `make lint` short-circuits and can mask real lint failures), then run `ruff check .` and `mypy . --exclude build --exclude dist`. `python tools/scan_untested.py` reported zero gaps (all exported callables tested). Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification. To find the next uninspected batch, list the repository `*_utils.py` modules, subtract the inspected set, and pick the next group.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.
