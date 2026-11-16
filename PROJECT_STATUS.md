# Project Status

## Latest Session (2026-11-16) — defect hunt/fix: `chunk_utils` bool size rejection

- `board_read`: empty (no task posted to main); executed durable handoff from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` rc=2 at session start/end (source-relevant edits pending coherent full verification checkpoint). No `--full --record-full-suite` run this session.
- **Optimize-delays survey:** no avoidable repository-managed delay; used state-delta probe, targeted pytest/unittest/ruff/mypy for touched files, fast `scan_untested` and `refresh_scaffold --check`. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defect fixed (failing-test-first):** `chunk_utils.chunk`, `ichunk`, and `chunk_count` accepted `bool` `size` values as ints, diverging from `chunk_pad`/`even_chunks` and module contracts. Added bool-rejection tests that failed before fix, then enforced `TypeError` for bool sizes.
- **Verification:** `python -m pytest tests/test_chunk_utils.py -q` (34 passed), `python -m unittest tests.test_public_api -q` (OK), `python -m ruff check chunk_utils.py tests/test_chunk_utils.py` (clean), `python -m mypy chunk_utils.py tests/test_chunk_utils.py` (clean), `python tools/scan_untested.py --all` (clean).
- **Scaffold/CHANGELOG:** added Unreleased changelog entry; `python tools/refresh_scaffold.py` + `--check` in sync.
- **Defect hunt batch:** reviewed `bz2_utils`, `cache_utils`, `calendar_utils`, `call_once_utils`, `case_utils`, `cgi_utils`, `cgitb_utils`, `chunk_utils`, `circuit_breaker_utils`; no other defects found.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 at current HEAD due to source-relevant edits (`chunk_utils` bool-size rejection fix + tests + changelog/handover docs) not yet recorded by a full verification checkpoint. Run `--full --record-full-suite` after validating this session's changes at a coherent milestone.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. No timestamp-only handovers/empty commits.
4. **Continue the correctness defect hunt (failing-test-first) on `*_utils.py` modules not yet defect-hunted.** This session fixed `chunk_utils.chunk`/`ichunk`/`chunk_count` bool-size rejection. Reviewed batch `bz2_utils`, `cache_utils`, `calendar_utils`, `call_once_utils`, `case_utils`, `cgi_utils`, `cgitb_utils`, `chunk_utils`, `circuit_breaker_utils` with no other defects found. Pick next unreviewed set (e.g. `cli_utils`, `cmath_utils`, `cmd_utils`, `code_utils`, `codecs_utils`, `codeop_utils`, `collections_abc_utils`, `collections_utils`, `color_utils`, `colorsys_utils`, `compileall_utils`), read implementations against wrapped stdlib/contracts, look for off-by-one/boundary/reset/aliasing/bool-as-int/type-contract defects, and add a test that fails before fix and passes after.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post next task to `main` via `board_post`.

## Previous Session (2026-11-16) — defect hunt/fix: `builtins_utils.iterator` sentinel contract
