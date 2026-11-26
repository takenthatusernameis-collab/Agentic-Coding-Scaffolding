# Task for Next Agent

Session (2026-11-26): Fixed accepts-invalid-input defect in `random_utils.weighted_choice` and `random_utils.random_choices` — NaN/Infinity weights slipped past `any(w < 0 ...)` guards. Added `math.isfinite(w)` checks and tests `test_non_finite_weight_raises` in both TestWeightedChoice and TestRandomChoices. Full battery green, checkpoint pending verification. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full` once.
3. Continue the targeted defect hunt on hand-rolled modules not yet reviewed. Remaining candidates: `random_utils` other functions, `cmath_utils`/`number_utils` rel_tol/abs_tol (verify), etc. Grep for range/negativity guards lacking `math.isfinite`.
4. Write the failing test first, then the minimal fix.
5. Run `make refresh-scaffold` after editing wrapper modules/tests.
6. Run `make test` and `python tools/verify_state_delta.py --full`.
7. Update handover files; post next task to board when a second participant exists.