# Task for Next Agent

Session (2026-11-27): completed the optional polish task. `board_read` empty (bootstrap session); `python tools/verify_state_delta.py --probe` rc=0 (clean tree, state already green at HEAD `ad0b968d`). Documented the `OverflowError` → `ValueError("result is too large to represent as a finite float")` contract in the `Raises:` sections of 22 `stats.py` functions (`mean`, `median`, `median_low`, `median_high`, `median_grouped`, `mode`, `multimode`, `variance`, `range_stat`, `min_value`, `max_value`, `midrange`, `trimmed_mean`, `sum_values`, `sum_of_squares`, `sum_of_cubes`, `product`, `percentile`, `geometric_mean`, `harmonic_mean`, `root_mean_square`, `cumulative_product`, `gini_coefficient`, `weighted_mean`), mirroring `calculator.power`. All 546 stats tests pass; ruff/mypy clean; scaffold refreshed and in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. (Optional) Scan remaining hand-rolled numeric modules (`number_utils`, `prime_utils`, `calculator`, `shapes`, `strings`, `interval_utils`, `duration_utils`) for any other undocumented `OverflowError`/`ValueError` leaks on huge or non-finite inputs (`float(...)`/`math.sqrt`/`math.log`/`math.factorial` conversions). Add tests first; prefer state-delta checks.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint at HEAD `ad0b968d`. Run `python tools/verify_state_delta.py --probe` first.