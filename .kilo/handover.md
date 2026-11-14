# Handover

## Latest Session (2026-11-14T15:41Z)

- `board_read`: no pending task/messages for this session (bootstrap). The durable handover was `PROJECT_STATUS.md`; the previous session's work landed as commit `8cd6acd` (pydoc `writedoc`/`writedocs` tests) without a handover update.
- State-delta: `python tools/verify_state_delta.py` advanced the checkpoint to `8cd6acd` (HEAD); full suite re-run because `tests/` changed. Final `--full --record-full-suite` passed with `full_suite_head == head == 8cd6acd`.
- Inherited regression repaired: `tests/test_pydoc_utils.py` hard-coded `tests.test_pydoc_utils` for `classname`/`parentname`, which failed under `python -m unittest discover tests/` (module imported as top-level `test_pydoc_utils`). Assertions now derive expectations from `_Example.__module__`/`__qualname__` and pass under both import styles.
- Executed improvement (portability/API truthfulness): `cgi`, `cgitb`, and `pipes` were removed in Python 3.13, but `cgi_utils`, `cgitb_utils`, and `pipes_utils` imported them unconditionally while `is_available()` returned a hard-coded `True`. This broke import on 3.13+ and advertised false availability, diverging from the guarded-import convention used by `imghdr_utils`/`sndhdr_utils`/`spwd_utils`/`nntplib_utils`/`telnetlib_utils`.
  - `cgi_utils.py`: guarded import + `_CGI_AVAILABLE`; `is_available()` reports it. `FieldStorage`/`MiniFieldStorage`/`parse_header`/`parse_multipart` raise `RuntimeError` when `cgi` is absent; `escape`/`parse`/`parse_qs`/`parse_qsl` keep working (html/urllib fallbacks).
  - `cgitb_utils.py`: guarded import + truthful flag. cgitb-backed helpers raise `RuntimeError`; pure formatters (`small`/`strong`/`grey`/`pink`/`blue`) still work; `disable()` safely resets `sys.excepthook`.
  - `pipes_utils.py`: guarded import + truthful flag. `Template`/`create_template`/`make_pipeline` raise `RuntimeError`; `quote`/`quote_command` fall back to `shlex.quote`; `step_kinds()` unchanged.
- Tests: added `cgi_utils.escape` behavior coverage (previously counted as covered by an existence-only `hasattr` check) and reload-based unavailable-branch tests for all three wrappers (`mock.patch.dict(sys.modules, ..., None)` + `importlib.reload`), so the 3.13+ path is verified on 3.12.
- Docs/scaffold sync: added the Unreleased changelog entry before refreshing; `python tools/refresh_scaffold.py` refreshed 8 embedded copies, `--check` reports all in sync.
- Validation: `python -m unittest tests.test_cgi_utils tests.test_cgitb_utils tests.test_pipes_utils` 24 OK; `python -m ruff check .` clean; `python -m mypy . --exclude build --exclude dist` clean; `python tools/scan_untested.py` clean; `python -m unittest discover tests/` 10921 OK (skipped=4); `python tools/verify_state_delta.py --full --record-full-suite` passed.
- `.github/workflows/**` unchanged.

## State

- HEAD: `8cd6acd780722596b4efdff83f53ca4254ed294d`
- Verified checkpoint: `.kilo/last_verified.checkpoint` (head `8cd6acd`, full_suite_head `8cd6acd`)
- Working tree (pending auto-commit): `CHANGELOG.md`, `cgi_utils.py`, `cgitb_utils.py`, `pipes_utils.py`, `scaffold.sh`, `tests/test_cgi_utils.py`, `tests/test_cgitb_utils.py`, `tests/test_pipes_utils.py`, `tests/test_pydoc_utils.py` (auto-committed by CI per AGENTS.md; do not commit manually)

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py`; after the pending auto-commit lands expect the clean-tree fast path.
3. Deliver one concrete, verified improvement (choose on evidence):
   - Continue the Python 3.13+ portability pass: `aifc_utils`, `sunau_utils`, `uu_utils`, `xdrlib_utils`, and `mailcap_utils` still import stdlib modules removed in 3.13 unconditionally (and expose no `is_available()`). Apply the same guarded-import/fallback convention and add reload-based tests.
   - `python tools/scan_untested.py --all`: add behavior coverage where a safe non-interactive seam exists; skip TypeVar/stdlib re-export/alias/constant/interactive-facade noise.
   - Inspect wrappers for doc/API/edge-case mismatches (validation, return types, error semantics) and fix with targeted tests.
   Avoid timestamp-only or no-op changes.
4. Validation order to avoid drift: edit sources and **documents first**, then `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`. Run `python tools/scan_untested.py`, targeted tests, `make lint`, `make typecheck`, and `python -m unittest discover tests/` when `tests/` changed, finishing with `python tools/verify_state_delta.py --full --record-full-suite`.
5. Keep changes outside `.github/workflows/**`; update `CHANGELOG.md` (before refreshing), `.kilo/handover.md`, `PROJECT_STATUS.md`; post the next task via `board_post` to `main` (or record it here if posting to self is refused).