# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1 once this session's changes are committed; no redundant full re-run is needed unless a source-relevant file changes.
3. Prior session summary — routine regression monitoring: state green at HEAD `4d3248f0`; audit/scan clean (238 low-signal, 0 genuine; no untested callables); no source changes (avoiding a no-op cycle).
4. Continue routine regression monitoring / targeted defect hunt on hand-rolled modules not yet reviewed. Write the failing test first.
5. Routine gates at a coherent milestone.
6. Test modules must stay under `tests/`. Keep `.github/workflows/**` unchanged.
7. Refresh scaffold after editing modules/tests/CHANGELOG.
8. Update handover files; post next task to `main` when a second participant exists. No duplicate/empty handoffs.
