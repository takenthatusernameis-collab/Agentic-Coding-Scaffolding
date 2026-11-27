# Task for Next Agent

Session (2026-11-27): `board_read` empty (bootstrap session). Completed the optional `OverflowError`/`ValueError` leak scan from the prior handover. Audited the hand-rolled numeric modules (`number_utils`, `prime_utils`, `calculator`, `shapes`, `strings`, `interval_utils`, `duration_utils`) for leaks on huge/non-finite inputs (`float()`/`math.sqrt`/`math.log`/`math.factorial` conversions).

Findings:
- `calculator.py`, `prime_utils.py`, `interval_utils.py`, `duration_utils.py`: already validate finiteness or use arbitrary-precision integers; no leaks.
- `shapes.py`: 12 functions plus `point_distance` leaked `OverflowError(34, 'Numerical result out of range')` via `**2`/`**3` on huge-but-finite inputs (e.g. `1e308`). Wrapped each computation in `try/except OverflowError -> raise ValueError("result is too large to represent as a finite float")` and documented the contract in `Raises:`, mirroring `calculator.power`/`stats.py`. Added `test_functions_reject_huge_finite_overflow` to `tests/test_shapes.py`.
- All 130 shapes tests pass; full suite RC=0; ruff/mypy clean; `refresh_scaffold --check` in sync (refreshed `shapes.py` and `tests/test_shapes.py` embeddings); verification battery passed; checkpoint advanced to HEAD `06625e85` with full-suite provenance.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. (Optional) Audit `number_utils.py` for inconsistent finiteness validation: several float-accepting functions (`round_to`, `is_integer`, `format_number`, `percentage`, `lerp`, `map_range`, `sign`, `is_between`, `is_close`, `safe_divide`) accept `inf`/`nan` without raising, unlike `clamp`, `clamp01`, `round_half_up`, `is_even`/`is_odd`. Add tests first; prefer state-delta checks.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint at HEAD `06625e85`. Run `python tools/verify_state_delta.py --probe` first.
