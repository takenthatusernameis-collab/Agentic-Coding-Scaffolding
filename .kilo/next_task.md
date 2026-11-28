# Task for Next Agent

Session (2026-11-28): delay-bottleneck elimination pass. Classified the wait as
AVOIDABLE_PROCESS_DELAY (a latent bug that would burn a future debugging
session). Found and fixed a real defect class in `calculator.py`: `sign()` and
`clamp()` called `math.isnan(x)` on a value that had only passed an
`(int, float)` type check, so a large int (e.g. `10**400`) leaked an
undocumented `OverflowError` instead of returning a sign / clamping. Every
other numeric helper already guards the check with `isinstance(..., float)`
(see `_require_finite`); these two were the outliers. Fixed both with the same
guarded pattern and added regression tests (`test_sign_accepts_huge_int`,
`test_clamp_accepts_huge_int_endpoints`), then ran `make refresh-scaffold`.

Verified: `make lint` clean; `make typecheck` clean (574 files); full suite
`python -m unittest discover tests/` = 12061 tests OK (skipped=4); battery
checkpoint advanced to f4cd0239 with full-suite provenance recorded.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run
   `--full --record-full-suite` once.
3. Continue the same "huge int leaks an undocumented `OverflowError` from a
   float-only math call" sweep on the hand-written modules. Concrete repro
   already found: `shapes.rectangle_diagonal(10**400, 0)` raises
   `OverflowError` from `math.hypot` (and `shapes.distance`/`point_distance`
   share the `math.hypot` pattern). Audit `shapes.py`, `stats.py`,
   `strings.py`, `utils.py`, `prompt_utils.py`, `config_schema.py` for
   `math.hypot`/`math.sqrt`/`float(...)` applied to user input that only passed
   an `isinstance(..., (int, float))` check without a finiteness/magnitude
   guard; fix any hit with a guarded conversion (mirror the `sign`/`clamp`
   fix) and add a regression test. Run `make refresh-scaffold` after editing a
   module or its test.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`,
   `PROJECT_STATUS.md`); post to the board when a second participant exists.