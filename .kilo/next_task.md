# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1, state is already verified; no redundant full re-run unless a source-relevant change occurred. If rc=2, run `python tools/verify_state_delta.py --full --record-full-suite`.
3. Prior session summary — state green at HEAD `c6cf3d34`; checkpoint advanced `6ae9affc` → `c6cf3d34` via full battery (genuine delta). Full battery green: tests 11973 passed / 4 skipped / 4438 subtests, lint clean, typecheck clean (574 files), scan_untested clean, refresh_scaffold in sync, audit_contracts 236 low-signal / 0 genuine defects.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed (this cycle reviewed semver_utils, interval_utils, ttl_cache_utils, ring_buffer_utils, circuit_breaker_utils — all clean). Prefer a genuine logic defect; write the failing test first. All classic defect classes previously swept; audit_contracts reports low-signal candidates only. `tests/test_doctests.py` already enforces every top-level doctest example.
5. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
6. Routine gates at coherent milestone.
7. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
8. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
9. Update handover files; post next task to main when a second participant exists.