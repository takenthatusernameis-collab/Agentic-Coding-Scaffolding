# Task for Next Agent

Session (2026-11-28): delay-bottleneck elimination pass, continuing the "huge int
leaks an undocumented `OverflowError` from a float-only math call" sweep.

State at start: the previous session had already fixed `shapes.py`
(`rectangle_diagonal`, `point_distance`, `midpoint` now raise `ValueError` via a
guarded `math.hypot` / `/2.0` conversion) and added tests, committed as 8307088d,
but never advanced the checkpoint or handover. `verify_state_delta.py --probe`
returned rc=2 (source changed since the fa63f3ac checkpoint), so the battery and
full suite were re-run to re-establish a verified baseline before new work.

This session audited the remaining named modules:
- `stats.py` — clean; every float-returning helper already guards huge ints
  (`mean`, `geometric_mean`, `root_mean_square`, etc. all raise `ValueError`).
- `strings.py`, `prompt_utils.py` — no `math.`/`float()` applied to user input;
  clean.
- `utils.py` — found + fixed a real leak: `average([10**400])` raised
  `OverflowError` from `sum(lst)/len(lst)`. Wrapped in try/except -> `ValueError`
  (mirrors `stats.mean`). Added `test_average_accepts_huge_int`.
- `config_schema.py` — found + fixed a real leak: `float_validator(10**400)`
  raised `OverflowError` from `float(value)` (only `ValueError`/`TypeError` were
  caught). Added `OverflowError` to the except clause -> `ValueError`. Added
  `test_float_validator_rejects_huge_int`.

Ran `make refresh-scaffold` (config_schema.py, utils.py and their tests are
embedded wrapper modules; scaffold.sh updated).

Verified: `make lint` clean; `make typecheck` clean (574 files); full suite
`python -m unittest discover tests/` = 12065 tests OK (skipped=4); battery
checkpoint advanced to 8307088d with full-suite provenance recorded.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run
   `--full --record-full-suite` once.
3. Concrete repro already confirmed: `calculator.sqrt(10**400)` raises
   `OverflowError` from `float(a**0.5)` at calculator.py:240 — `sqrt` is the
   outlier; the sibling `power` (calculator.py:221-224) already guards the
   conversion. Fix `sqrt` with the same try/except -> `ValueError`, add a
   regression test (e.g. `test_sqrt_accepts_huge_int`), then run
   `make refresh-scaffold`. Then continue the sweep on the other hand-written
   numeric modules not yet audited — `duration_utils.py` (`float(seconds)` at
   :205/:289/:334), `interval_utils.py` (`float(interval[1]-interval[0])` at
   :229), and `number_utils.py` (`float(value)` at :393/:427/:954) — for the same
   "float-only conversion of an int that only passed an `isinstance((int,float))`
   check" pattern; fix any hit with a guarded conversion and a regression test.
   Avoid functions that loop on huge input (e.g. an iterative sqrt / prime check).
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`,
   `PROJECT_STATUS.md`); post to the board when a second participant exists.