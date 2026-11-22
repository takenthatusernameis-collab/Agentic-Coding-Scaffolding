# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=1 (clean tree; verified checkpoint `f762a9da` behind HEAD on bookkeeping-only commits; no source-relevant file changed since the checkpoint). No redundant full re-run needed unless a source-relevant file changes.
3. Prior session summary — bootstrap session; fixed `config_utils.get_config_value` silently ignoring non-dict `config` (silently ignored params defect). Changed the function to raise `TypeError` for non-dict `config`, matching `set_config_value` and `merge_configs`. Wrote the failing test first (`test_get_with_non_dict_config`); failed pre-fix, passes after. Full verification battery passed; checkpoint advanced to HEAD `f762a9da`. `board_post` to `main` refused (only self participant); next task recorded in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Defect hunt: continue targeted review of hand-rolled modules for classic defect classes. `operator_utils` and `config_utils` reviewed.
5. Routine gates at a coherent milestone: `python -m unittest discover tests/`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
6. Test modules must stay under `tests/`; do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
7. If you edit any hand-rolled `*_utils.py` module, its test, or `CHANGELOG.md`, run `make refresh-scaffold` then `python tools/refresh_scaffold.py --check`.
8. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate board tasks, create timestamp-only handoffs, or commit empty/no-op cycles.
