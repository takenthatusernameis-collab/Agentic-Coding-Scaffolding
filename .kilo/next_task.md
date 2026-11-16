# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=0/1 at session start (checkpoint matches HEAD). Run `--full --record-full-suite` once to advance the checkpoint only if the probe reports a source-relevant change. Avoid redundant full runs once the checkpoint matches source-relevant state.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey.
4. Defect hunt status: the `*_utils.py` defect hunt is complete across every wrapper module; no uninspected modules remain. `python -m ruff check .` and `python -m mypy . --exclude build --exclude dist` if source changed or confidence needed. `python tools/scan_untested.py` reports zero gaps. Run `make test-full` as a milestone and record full-suite provenance via `verify_state_delta.py --full --record-full-suite`. Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.
