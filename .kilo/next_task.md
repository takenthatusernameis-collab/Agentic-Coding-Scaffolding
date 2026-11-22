# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1, run full. No redundant full re-run unless source-relevant change.
3. Prior session summary — state green at HEAD `9cd34fc4`; full battery green; full test suite OK (exit 0); ruff clean; mypy clean; scaffold copies in sync; no untested exports. Checkpoint advanced to HEAD with full-suite provenance.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer genuine logic defect; write failing test first.
5. Routine gates at coherent milestone.
6. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
7. If edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
8. Update handover files; post next task to main when second participant exists.
