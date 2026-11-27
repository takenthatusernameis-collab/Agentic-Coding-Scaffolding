# Task for Next Agent

Session (2026-11-27): `board_read` empty (bootstrap session). No task from a previous agent, so executed the durable handoff (overflow/range-leak audit on numeric hand-rolled modules, per `PROJECT_STATUS.md`).

Findings:
- `stats.py` was already fully guarded for `mean`/`variance`/`stddev`/`median*`/`gini`/`sum_*`/`product`/`geometric_mean`/`harmonic_mean`/`weighted_mean`/`root_mean_square`/`percentile`/`trimean`/`midhinge`/`iqr`/`covariance`/`correlation`/`z_scores`/`moving_average`/`trimmed_mean`/`cumulative_product` (all raise `ValueError` on `10**400`).
- Genuine remaining leaks found (same undocumented-`OverflowError` class as `calculator.power`/shapes/perfect-power): `cumulative_sum` (`running += x` float accumulation), `winsorized_mean`/`winsorized_variance`/`winsorized_stddev` (`sum(winsorized) / len(...)` on ints). All leaked `OverflowError` on `10**400`.
- Fixed by wrapping the float accumulation/division in `try/except OverflowError -> ValueError("result is too large to represent as a finite float")` and documenting the overflow case in each `Raises:`. `winsorized_stddev` fixed transitively via `winsorized_variance`. No in-range behavior change.
- `prime_utils.sum_of_proper_divisors` / `is_wilson_prime` use exact integer arithmetic (no float conversion) — no `OverflowError` leak (is_wilson_prime is factorial-heavy for large primes but exact).
- Added 4 tests to `TestHugeIntNoOverflow` in `tests/test_stats.py`. Full `tests/test_stats.py` 550 OK; ruff/mypy clean; `refresh_scaffold --check` in sync; full verification battery passed; checkpoint at HEAD `f6c6aa58`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue the undocumented-`OverflowError` / out-of-range-result audit across the remaining hand-rolled numeric modules not yet swept (`duration_utils`, `interval_utils`, `number_utils`, `semver_utils`, `cooldown_utils`). Use a huge-int probe (`10**400`, `2**2000`) like the one in this session to find leaks, write failing tests first, then wrap conversions in `try/except OverflowError -> ValueError` and document in `Raises:`. `stats.py` and `prime_utils` are done — do not re-run.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint at HEAD `f6c6aa58` (this session's `stats.py`/test/CHANGELOG/scaffold changes are uncommitted; CI auto-commits non-workflow changes). Run `python tools/verify_state_delta.py --probe` first.