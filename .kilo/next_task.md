# Task for Next Agent

Session (2026-11-27): `board_read` empty (bootstrap session). Completed the optional `number_utils.py` finiteness validation audit from the prior handover.

Findings:
- Added tests documenting current behavior for `is_integer`, `format_number`, `is_close` with `nan`/`inf` inputs (3 new tests in `tests/test_number_utils.py`).
- Current behavior: `is_integer` returns `False` for `nan`/`inf`; `format_number` returns `"nan"`/`"inf"`/`"-inf"` strings; `is_close` follows `math.isclose` semantics (returns `False` for `nan` comparisons, `True` for `inf==inf`).
- Inconsistency confirmed: `clamp`, `clamp01`, `round_half_up`, `is_even`/`is_odd` raise `ValueError` for non-finite inputs; the audited functions do not.
- Fixing this would be a breaking change; left for future decision.
- All 363 `number_utils` tests pass; full suite (11984 tests) passes; ruff/mypy clean; `refresh_scaffold --check` in sync (refreshed `tests/test_number_utils.py` embedding); verification battery passed; checkpoint advanced to HEAD `7d6cae5c`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. (Optional) Implement finiteness validation for audited `number_utils.py` functions to match `clamp`/`clamp01`/`round_half_up`/`is_even`/`is_odd` pattern: add `math.isfinite` checks and raise `ValueError` for `nan`/`inf`; update tests to expect `ValueError`.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint at HEAD `7d6cae5c`. Run `python tools/verify_state_delta.py --probe` first.