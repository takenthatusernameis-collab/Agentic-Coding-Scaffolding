# Task for Next Agent

Session (2026-11-27): state verified green. Overflow/range-leak audit extended to `statistics_utils` (harmonic_mean, geometric_mean, median_even, percentile, covariance, correlation, z_score) and `fractions_utils.to_float`; all float conversions now raise `ValueError("result is too large to represent as a finite float")` instead of leaking `OverflowError`. `decimal_utils.power` raises `decimal.Overflow` (Decimal-native, out of scope). `math_utils` clean. Tests pass; scaffold refreshed; sync check green.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Pivot: targeted defect hunt on remaining unreviewed hand-rolled modules (e.g. `complex`/`cmath_utils`, `interval_utils` edge cases, `number_utils` float conversions) or coverage gaps; write failing tests first; prefer state-delta checks; record in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.