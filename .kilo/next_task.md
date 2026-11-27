# Task for Next Agent

Session (2026-11-27): fixed a genuine defect — `calculator.power` leaked an undocumented `OverflowError` for out-of-range results (`power(10, 400)`, `power(10.0, 400)`, `power(2, 2000)`); the final `float(a**b)` overflowed. Wrapped it in `try/except OverflowError` → `ValueError` (matching the module's reject-non-finite convention) and documented the overflow case. Added `test_power_overflow_raises_value_error`. Full battery green at HEAD fca0cdb9; ruff clean, mypy clean (574 files), scaffold in sync. Importability sweep (`py_compile *.py` + import of all 280 modules) clean.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue targeted defect hunt on remaining unreviewed hand-rolled modules. The escaped-docstring/importability class is exhausted (all 280 modules import; `py_compile` clean). The NaN/Infinity class is exhausted. `calculator`/`shapes`/`strings`/`stats`/`interval_utils`/`duration_utils` reviewed this session — only the `power` overflow defect found. Pivot to: (a) per-module coverage gaps on wrapper modules not yet closed (candidates from prior sessions: `semver_utils` 91%, `slugify_utils` 92%, `validation_utils` 97%, `circuit_breaker_utils` 96%, `memoize_utils` 98%; skip `__main__` demos and unreachable defensive while-loops), OR (b) overflow/range-leak audit on other numeric hand-rolled modules (`number_utils`, `prime_utils`, `statistics`-style helpers) analogous to the `power` fix. Add tests first; prefer state-delta checks.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.