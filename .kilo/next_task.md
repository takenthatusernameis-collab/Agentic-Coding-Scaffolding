# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1 (checkpoint behind HEAD on bookkeeping commits), run `python tools/verify_state_delta.py --full --record-full-suite` to confirm and advance the checkpoint. No redundant full re-run is needed unless a source-relevant file changed.
3. Prior session summary — state green at HEAD `946e5a67`; targeted review of candidate hand-rolled modules found no genuine defect (all hardened). No source changes.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed: `seq_utils`, `string_utils`, `strings`, `number_utils`, `numbers_utils`, `stats`, `calculator`, `shapes`, `prompt_utils`, `type_utils`, `types_utils`, `typing_utils`, `enum_utils`, `dataclasses_utils`. Prefer a genuine logic defect over a documentation-only tweak; write the failing test first.
5. Routine gates at a coherent milestone: `python -m pytest tests/ -q`, `python -m ruff check .`, `python -m mypy . --exclude build --exclude dist`, `python tools/refresh_scaffold.py --check`, `python tools/verify_state_delta.py --full --record-full-suite`.
6. Test modules must stay under `tests/`; do not add root-level `test_*.py` files. Keep `.github/workflows/**` unchanged.
7. If you edit any hand-rolled `*_utils.py` module, its test, or `CHANGELOG.md`, run `make refresh-scaffold` then `python tools/refresh_scaffold.py --check`.
8. Update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post` when a second participant exists. Do not post duplicate board tasks, create timestamp-only handoffs, or commit empty/no-op cycles.
