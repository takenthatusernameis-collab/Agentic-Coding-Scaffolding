# Task for Next Agent

Session (2026-11-27): state verified green — checkpoint advanced to HEAD `541fdf22` via `python tools/verify_state_delta.py --full --record-full-suite` (battery passed). Overflow/range-leak audit extended to `duration_utils`, `interval_utils`, `number_utils`, `semver_utils`, `cooldown_utils` via `tools/_overflow_probe.py`: all float conversions already raise `ValueError("result is too large to represent as a finite float")` (no `OverflowError` leaks); no source changes. `audit_contracts.py --summary`: 0 issues.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Pivot: targeted defect hunt on `cmath_utils` / complex-number edge cases (NaN/Infinity propagation, validation of `bool` as complex, doctest coverage) or coverage gaps on remaining low-coverage wrappers; write failing tests first; prefer state-delta checks; record in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.
