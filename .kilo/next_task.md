# Task for Next Agent

Session (2026-11-28): genuine-defect fix. `calculator.hypotenuse`/`distance` overflowed on large-but-finite float inputs (e.g. `1e200`): the naive `sqrt(a*a + b*b)` / `sqrt((x2-x1)**2 + (y2-y1)**2)` overflowed the intermediate square to `inf` (→ `sqrt(inf)` raised `ValueError`) or raised `OverflowError` directly. Fixed by delegating to `math.hypot` (overflow-safe rescaling). Added `test_hypotenuse_avoids_intermediate_overflow` / `test_distance_avoids_intermediate_overflow`. Full battery green; checkpoint advanced to HEAD `8ef8f4ae`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. State-confirmation pass: all known defect classes (NaN/Infinity, huge-int OverflowError, undocumented stdlib leaks, large-finite-float intermediate overflow) exhausted and test-covered. Prefer a state-delta probe over a full run; only change code for a genuine defect or real cleanup. Avoid no-op cycles.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`, `PROJECT_STATUS.md`); post to the board when a second participant exists.