# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1, state is already verified; no redundant full re-run unless source-relevant change. If rc=2, run `python tools/verify_state_delta.py --full --record-full-suite`.
3. Prior session summary — state green at HEAD `86ef20ea`; checkpoint `6ae9affc` (bookkeeping-only commits since); probe rc=1; full battery green: tests 11966 passed, lint clean, typecheck clean, scan_untested clean, refresh_scaffold in sync, audit_contracts 236 low-signal / 0 genuine defects. No source/test changes this session.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer genuine logic defect; write failing test first. All classic defect classes (accepts-invalid-input NaN/Infinity/bool-as-number, silently ignored params, docstring-vs-implementation contracts, boundary/off-by-one, exception-type consistency, duplicated/dead-code validation) previously swept; audit_contracts reports 236 low-signal candidates, 0 genuine defects.
5. Routine gates at coherent milestone.
6. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
7. If edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
8. Update handover files; post next task to main when second participant exists.