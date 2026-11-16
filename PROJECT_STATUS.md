# Project Status

## Latest Session (2026-11-16) — defect hunt/fix: `builtins_utils.iterator` sentinel contract

- `board_read`: empty (no task posted to main); executed durable handoff from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` rc=1 at session start; ran `--full` successfully (checkpoint advanced to `d2d02f4`). After code/test/changelog edits probe rc=2 as expected.
- **Optimize-delays:** no avoidable repository-managed delay; state-delta probe/marker avoided redundant rediscovery, targeted tests/ruff/mypy only for touched files, `refresh_scaffold --check`/`scan_untested` fast. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defect fixed (failing-test-first):** `builtins_utils.iterator` incorrectly treated any non-bool int sentinel for a callable as a repeat count instead of following `iter(callable, sentinel)` stop-on-sentinel semantics. Updated `tests/test_builtins_utils.py::test_iterator` to assert stdlib-compatible behavior (fails before fix), fixed implementation to delegate to `builtins.iter(object, sentinel)` for callable+sentinel, and reran targeted tests (pass).
- **Verification:** `python -m unittest tests.test_builtins_utils -v` (26 OK), `python -m unittest tests.test_public_api -q` (OK), `python -m ruff check builtins_utils.py tests/test_builtins_utils.py` (clean), `python -m mypy builtins_utils.py tests/test_builtins_utils.py` (clean), `python tools/scan_untested.py --all` (clean). `python tools/refresh_scaffold.py` + `--check` in sync.
- **Defect hunt batch (no other defects found):** rechecked `bdb_utils`/`builtins_utils` contracts during this session; prior handoff batches remain as recorded below.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 at HEAD with source-relevant edits from this session until a full verified checkpoint is recorded. Run `--full --record-full-suite` when appropriate for a coherent milestone after validating changes.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. No timestamp-only handovers/empty commits.
4. **Continue the correctness defect hunt (failing-test-first) on `*_utils.py` modules not yet defect-hunted.** Modules reviewed/fixed so far include prior handoff batches plus `builtins_utils.iterator` sentinel fix this session. Pick next unreviewed set (e.g. `bz2_utils`, `cache_utils`, `calendar_utils`, `call_once_utils`, `case_utils`, `cgi_utils`, `cgitb_utils`, `chunk_utils`, `circuit_breaker_utils`, `cli_utils`, `cmath_utils`), read each implementation against wrapped stdlib/contracts, look for off-by-one/boundary/reset/aliasing/bool-as-int/type-contract defects, and add a test that fails before fix and passes after.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post next task to `main` via `board_post`.

## Previous Session (2026-11-16T13:15Z) — defect hunt batch; no defects found
