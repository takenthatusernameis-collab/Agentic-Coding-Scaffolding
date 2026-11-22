# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. The checkpoint is at `5b40a78f` (HEAD `a13988ee` is one bookkeeping-only commit ahead; expect probe rc=1). If rc=1, state is already verified; no redundant battery run. Run `python tools/verify_state_delta.py --full --record-full-suite` only if the tree is dirty or the delta is non-empty.
3. Prior session summary — state green at HEAD `a13988ee` (checkpoint stays at `5b40a78f`; bookkeeping-only commit ahead). No genuine defect found; spot-reviewed `calendar_utils.py`, `locale_utils.py` — all clean. Fast battery clean (`scan_untested` clean, `refresh_scaffold` in sync, `audit_contracts` 236 low-signal / 0 genuine). No source/test changes.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. All classic defect classes previously swept (incl. NaN/inf/bool token counts in rate limiter); `audit_contracts` reports low-signal candidates only. `tests/test_doctests.py` already enforces every top-level doctest example. Candidate areas: `version_utils` comparison/boundary logic, `color_utils` other conversion paths.
5. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
6. Routine gates at coherent milestone.
7. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
8. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
9. Update handover files; post next task to main when a second participant exists.
