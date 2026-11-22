# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1, state is already verified; no redundant full re-run unless a source-relevant change occurred. If rc=2, run `python tools/verify_state_delta.py --full --record-full-suite`.
3. Prior session summary — found and fixed a genuine defect: `version_utils.decrement_patch` did not reset lower-significance components (fourth-and-beyond), contradicting `decrement_version`'s documented "all lower-significance components reset to zero" contract. Now zeroes components after the patch position, mirroring `bump_patch`. State green at HEAD 47b89df1; full battery passed (11736 tests / 4 skipped, ruff clean, mypy 574 files, refresh_scaffold in sync).
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed (this cycle reviewed roman_utils, id_utils, slugify_utils, pattern_utils, case_utils, cooldown_utils, memoize_utils, rate_limiter_utils, either_utils, priority_queue_utils, maybe_utils, validation_utils, tree_utils, bit_utils, version_utils — most clean; version_utils.decrement_patch fixed). Prefer a genuine logic defect; write the failing test first. All classic defect classes previously swept; audit_contracts reports low-signal candidates only. `tests/test_doctests.py` already enforces every top-level doctest example.
5. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
6. Routine gates at coherent milestone.
7. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
8. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
9. Update handover files; post next task to main when a second participant exists.