# Task for Next Agent

Session (2026-11-27): continued the overflow/range-leak audit on hand-rolled numeric modules. `stats.py` leaked an undocumented `OverflowError` on huge integer inputs across `mean`, `median`, `median_low/high`, `median_grouped`, `mode`, `multimode`, `variance`, `stddev`, `pvariance`, `pstdev`, `range_stat`, `min_value`, `max_value`, `midrange`, `trimmed_mean`, `sum_values`, `sum_of_squares`, `sum_of_cubes`, `product`, `percentile`, `geometric_mean`, `harmonic_mean`, `gini_coefficient`, `root_mean_square`, `cumulative_product`, `weighted_mean`, `skewness`, `kurtosis`, `z_scores`, `standard_error`, `covariance`, `correlation`, `trimean`, `midhinge`, `iqr`, `quantile`, `moving_average`, `median_absolute_deviation`, `mean_absolute_deviation`, and `coefficient_of_variation`. Replaced each overflowing float conversion/division with `try/except OverflowError` re-raising `ValueError("result is too large to represent as a finite float")`, matching the `calculator.power` precedent. Added 42 failing-first tests; full `tests.test_stats` suite (546 tests) green. `prime_utils.sum_of_proper_divisors` (`math.sqrt(abs(n))` → `math.isqrt(abs(n))`) also fixed; `tests.test_prime_utils` (334 tests) green. `is_wilson_prime`/`is_perfect_power`/`is_prime_power` already safe. ruff/mypy clean; `refresh_scaffold.py --check` in sync; `verify_state_delta.py --full --record-full-suite` passed, checkpoint advanced to HEAD `602b71c3`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. (Optional polish) Document the `OverflowError` → `ValueError("result is too large to represent as a finite float")` contract in the `Raises:` sections of the modified `stats.py` functions, mirroring `calculator.power`.
4. (Optional) Scan remaining hand-rolled numeric modules (`number_utils`, `prime_utils`, etc.) for any other undocumented `OverflowError`/`ValueError` leaks on huge or non-finite inputs (`float(...)`/`math.sqrt`/`math.log`/`math.factorial` conversions). Add tests first; prefer state-delta checks.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint advanced to HEAD `602b71c3`. Run `python tools/verify_state_delta.py --probe` first; if rc=2 run `--full --record-full-suite` once.
