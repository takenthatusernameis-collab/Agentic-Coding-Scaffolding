# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=1 (clean tree; verified checkpoint at HEAD; no source-relevant file changed since the checkpoint). No redundant full re-run needed unless a source-relevant file changes.
3. Prior session summary — state green at HEAD `1f03d661`; checkpoint `5aadfdcd` behind HEAD on bookkeeping-only commits; fast battery (scan_untested, refresh_scaffold --check) clean; no genuine defect found; no source/test changes, avoiding a no-op cycle.
4. Defect hunt: continue targeted review of hand-rolled modules for classic defect classes. Many modules already reviewed; remaining candidates include `utils`, `stats`, `shapes`, `strings`, `calculator`, `prompt_utils`. All previously reviewed modules follow project validation conventions.
5. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
6. Test modules must stay under `tests/`; do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
7. If you edit any hand-rolled `*_utils.py` module, its test, or `CHANGELOG.md`, run `make refresh-scaffold` then `python tools/refresh_scaffold.py --check`.
8. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate board tasks, create timestamp-only handoffs, or commit empty/no-op cycles.
