# Task for Next Agent

Session (2026-11-27): bootstrap session; board empty. `python tools/verify_state_delta.py --probe` rc=1 (clean tree, state already green at HEAD `f086164e`); no source changes. Ran `--full --record-full-suite` once — passed, checkpoint at HEAD `f086164e`. Overflow/range-leak audit on `stats.py` and `prime_utils.sum_of_proper_divisors` already complete from prior sessions; ruff/mypy clean; scaffold in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. (Polish) Document the `OverflowError` → `ValueError("result is too large to represent as a finite float")` contract in the `Raises:` sections of the modified `stats.py` functions, mirroring `calculator.power`. Add tests first where useful.
4. (Optional) Scan remaining hand-rolled numeric modules (`number_utils`, `prime_utils`, `calculator`, `shapes`, `strings`, `interval_utils`, `duration_utils`) for any other undocumented `OverflowError`/`ValueError` leaks on huge or non-finite inputs (`float(...)`/`math.sqrt`/`math.log`/`math.factorial` conversions). Add tests first; prefer state-delta checks.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint at HEAD `f086164e`. Run `python tools/verify_state_delta.py --probe` first.
