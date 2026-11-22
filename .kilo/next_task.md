# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1, state is already verified; no redundant full re-run unless a source-relevant change occurred. If rc=2, run `python tools/verify_state_delta.py --full --record-full-suite`.
3. Prior session summary — state green at HEAD 0bdc99d5 (checkpoint d38d2f38; probe rc=1, tree clean). Defect hunt on `prime_utils.py`, `graphlib_utils.py`, `heapq_utils.py` found no genuine defect; all clean (prime_utils doctests 171 passed; 358 unit tests OK). No source/test changes, avoiding a no-op cycle. `scaffold.sh`/`refresh_scaffold` in sync; `audit_contracts` 236 low-signal / 0 genuine defects; `scan_untested` clean.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. All classic defect classes previously swept (incl. NaN/inf/bool token counts in rate limiter); audit_contracts reports low-signal candidates only. `tests/test_doctests.py` already enforces every top-level doctest example.
5. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
6. Routine gates at coherent milestone.
7. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
8. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
9. Update handover files; post next task to main when a second participant exists.
