# Handover

## Done (this session)
- `board_read`: empty; bootstrap session — no task from previous agent; executed durable handoff from `.kilo/next_task.md` (routine maintenance / regression monitoring).
- **State:** `python tools/verify_state_delta.py --probe` rc=1 — clean tree, no source-relevant change since the verified checkpoint; advanced checkpoint to HEAD via `--full --record-full-suite`; battery passed.
- **Change:** added `prime_factors(n)` to `calculator.py` (calculator.py:517) returning the prime factors of n in non-decreasing order, with input validation (TypeError for non-int/bool, ValueError for n < 2) and doctests; registered in `__all__`. Added `tests/test_calculator.py::TestPrimeFactors` with 8 cases (basic, product-equals-n, non-decreasing, all-prime, type/bool/range rejection). Synced embedded copies in `scaffold.sh` via `make refresh-scaffold`.
- **Verification:** `python -m unittest tests.test_calculator` — 133 OK; `python -m pytest tests/` — 11715 passed, 4 skipped; `python -m ruff check .` — clean; `python -m mypy . --exclude build --exclude dist` — success (572 files); `python tools/refresh_scaffold.py --check` — in sync; `python tools/verify_state_delta.py --full --record-full-suite` — passed at HEAD.
- **Board:** posted next task to `main` via `board_post`.

## Next
- Continue routine maintenance / regression monitoring: run the verification battery periodically —
  - `python -m unittest discover tests/` (or `pytest tests/`)
  - `python -m ruff check .`
  - `python -m mypy . --exclude build --exclude dist`
  - `python tools/refresh_scaffold.py --check`
  - `python tools/verify_state_delta.py --full --record-full-suite`
- The persistent-state defect family (unusable cache/marker files trusted by the verification tooling) is now closed on all three consumers: `verify_state_delta.read_marker`, `refresh_scaffold.check_cache_hit`, and `scan_untested.load_cache` all shape-validate their persisted state and degrade to a safe fallback. No open lead remains in that family.
- The library defect-hunt sweeps (bool-as-int, broad-except swallowing, silently ignored parameters, docstring-vs-implementation contracts via `tools/audit_contracts.py`, float/numeric edge cases, off-by-one boundaries) are complete with no open defect class; newly added modules get a first contract pass before the class is closed again. Test modules must stay under `tests/` (guarded by `TestSuiteLayout` in `tests/test_select_tests.py`); do not add root-level `test_*.py` files.
- Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`. Do not post duplicate/empty handoffs or commit no-op cycles.
