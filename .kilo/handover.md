# Handover

## Latest Session (2026-11-14T16:42Z)

- `board_read`: no pending task/messages (bootstrap/idle). Durable handover in `PROJECT_STATUS.md` requested Python 3.13+ portability for `aifc_utils`, `sunau_utils`, `uu_utils`, `xdrlib_utils`, `mailcap_utils`.
- State-delta: `python tools/verify_state_delta.py` at start showed stale/out-of-sync embedded copies for those modules/tests (7 stale) because repository copies had been updated but `scaffold.sh` was not refreshed; repaired as part of this session.
- Delivered (Python 3.13+ portability & availability truthfulness): `aifc_utils`, `sunau_utils`, `uu_utils`, `xdrlib_utils`, `mailcap_utils` now use guarded imports and truthful `is_available()` for stdlib modules removed in Python 3.13 (`aifc`, `sunau`, `uu`, `xdrlib`, `mailcap`). Module-backed operations raise `RuntimeError` when unavailable; exported `Error`/`ConversionError` remain valid exception classes. `xdrlib_utils` exposes compatible `Packer`/`Unpacker` callables that raise `RuntimeError` on instantiation when unavailable (and preserves subclass relationship between `ConversionError` and `Error`).
- Tests: expanded availability/round-trip coverage and added reload-based unavailable-branch tests for all five wrappers (`mock.patch.dict(sys.modules, ..., None)` + `importlib.reload`), so 3.13+ removal paths are verified on 3.12. `mailcap_utils.read_mailcap_file` coverage now asserts upstream `DeprecationWarning` to keep test output clean.
- Docs/scaffold sync: added Unreleased changelog entry before refresh; `python tools/refresh_scaffold.py` refreshed embedded copies; `--check` reports all in sync. `scan_untested.py` clean for default exported API.
- Validation: `python -m unittest tests.test_aifc_utils tests.test_sunau_utils tests.test_uu_utils tests.test_xdrlib_utils tests.test_mailcap_utils` (35 OK); `make lint` clean; `make typecheck` clean; `python -m unittest discover tests/` OK (10928 tests, 4 skipped); `python tools/verify_state_delta.py --full --record-full-suite` passed.
- `.github/workflows/**` unchanged.

## State

- HEAD at start: `9324ee2` (checkpoint advanced during session); verify with `python tools/verify_state_delta.py`.
- Verified checkpoint: `.kilo/last_verified.checkpoint` (updated by `--full --record-full-suite`).
- Working tree (pending auto-commit): `CHANGELOG.md`, `aifc_utils.py`, `mailcap_utils.py`, `scaffold.sh`, `sunau_utils.py`, `tests/test_aifc_utils.py`, `tests/test_mailcap_utils.py`, `tests/test_sunau_utils.py`, `tests/test_uu_utils.py`, `tests/test_xdrlib_utils.py`, `uu_utils.py`, `xdrlib_utils.py`, `.kilo/handover.md`, `PROJECT_STATUS.md` (auto-committed by CI per AGENTS.md; do not commit manually)

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py`; after the pending auto-commit lands expect the clean-tree fast path.
3. Deliver one concrete, verified improvement (choose on evidence):
   - `python tools/scan_untested.py --all`: add behavior coverage where a safe non-interactive seam exists; skip TypeVar/stdlib re-export/alias/constant/interactive-facade noise.
   - Continue Python 3.13+ portability audit: scan for other wrappers that import removed/renamed stdlib modules unconditionally without `is_available()`/fallback (e.g. search for `import imp`, `import distutils`, etc., or modules removed in 3.13) and apply guarded-import convention with reload-based tests.
   - Inspect wrappers for doc/API/edge-case mismatches (validation, return types, error semantics) and fix with targeted tests.
   Avoid timestamp-only or no-op changes.
4. Validation order to avoid drift: edit sources and **documents first**, then `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`. Run `python tools/scan_untested.py`, targeted tests, `make lint`, `make typecheck`, and `python -m unittest discover tests/` when `tests/` changed, finishing with `python tools/verify_state_delta.py --full --record-full-suite`.
5. Keep changes outside `.github/workflows/**`; update `CHANGELOG.md` (before refreshing), `.kilo/handover.md`, `PROJECT_STATUS.md`; post the next task via `board_post` to `main` (or record it here if posting to self is refused).
