# Project Status

## Latest Session (2026-11-16) — defect hunt/fix: `multiprocessing_utils` rejected valid `Lock`/`RLock`

- `board_read`: empty (bootstrap session); executed durable handoff from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` rc=2 at start (prior source-relevant edits pending checkpoint). Source changed, so ran `python tools/verify_state_delta.py --full` (battery passed, checkpoint `04bcf0e`), `python -m unittest discover tests/` (11266 tests, 1 pre-existing error, 4 skipped), then `--full --record-full-suite`.
- **Optimize-delays survey:** no avoidable repository-managed delay; used the state-delta probe and targeted tests for the touched module, then the battery/full suite at a coherent milestone. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defect fixed (failing-test-first):**
  - `multiprocessing_utils.create_condition`, `create_value`, and `create_array` validated their `lock` argument with `isinstance(lock, (mp.Lock, mp.RLock))`. `multiprocessing.Lock`/`RLock` are bound methods of the default context, not types, so `isinstance` raised `TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union` for every non-`None` lock. Passing a valid `Lock`/`RLock` therefore crashed instead of being accepted, contradicting the documented contracts ("lock must be a Lock, RLock, or None" / "lock must be bool or Lock/RLock"). The checks now use the real `multiprocessing.synchronize.Lock`/`RLock` types. Added `test_create_condition_accepts_lock`, `test_create_condition_accepts_rlock`, `test_create_value_accepts_lock`, `test_create_array_accepts_lock` (all fail before, pass after).
- **Verification:** `python -m unittest tests.test_multiprocessing_utils` — 34 OK; `python -m doctest multiprocessing_utils.py` — OK; `python -m py_compile` — OK; `python tools/scan_untested.py` — clean; `python tools/refresh_scaffold.py` + `--check` — in sync; `python -m unittest tests.test_scaffold_sync tests.test_public_api` — 24 OK.
- **Environment limitation:** `ruff`/`mypy`/`pytest` are not installed here. `unittest discover` shows one pre-existing error from `tests/test_quopri_utils.py` hard-importing `pytest`; unrelated to this session.
- **Scaffold/CHANGELOG:** added Unreleased changelog entry; refreshed embedded copies (`multiprocessing_utils.py`, `tests/test_multiprocessing_utils.py`, `CHANGELOG.md`).

## Latest Session (2026-11-16) — defect hunt/fix: `gc_utils.set_threshold` forwarding + `functools_utils.curry` builtins

- `board_read`: empty (bootstrap session); executed durable handoff from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` rc=1 at start (clean tree, checkpoint matched HEAD `2ccf470`); source changed, so ran the verification battery and `python -m unittest discover tests/`.
- **Optimize-delays survey:** no avoidable repository-managed delay; used the state-delta probe and targeted tests, then battery/full suite at a coherent milestone. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defects fixed (failing-test-first):**
  - `gc_utils.set_threshold` conflated an omitted threshold with an explicit `0` (default args `0, 0`), so `set_threshold(100, 0, 0)` became `gc.set_threshold(100)` and `set_threshold(500, 5)` reset generation 2 to 0. Defaults are now `None`; omitted arguments leave the threshold untouched while explicit `0` is forwarded. Added `test_two_arguments_preserve_threshold2`, `test_explicit_zero_generations`.
  - `functools_utils.curry` read `func.__code__.co_argcount` and crashed on builtins/callables without a code object (`curry(len)` → `AttributeError`). It now falls back to `inspect.signature`. Added `test_curry_builtin_function`.
- **Verification:** `python -m unittest tests.test_gc_utils tests.test_functools_utils` — 19 OK; `python -m doctest gc_utils.py functools_utils.py` — OK; `python -m py_compile` — OK; `python tools/scan_untested.py` — clean; `python tools/refresh_scaffold.py --check` — in sync; `python -m unittest tests.test_public_api tests.test_scaffold_sync tests.test_doctests` — 26 OK.
- **Environment limitation:** `ruff`/`mypy`/`pytest` are not installed here. `unittest discover` shows one pre-existing error from `tests/test_quopri_utils.py` hard-importing `pytest`; unrelated to this session.
- **Scaffold/CHANGELOG:** added Unreleased changelog entry; refreshed embedded copies.

## Latest Session (2026-11-16) — defect hunt/fix: `errno_utils` bool-as-int rejection

- `board_read`: empty (bootstrap session); executed durable handoff from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` rc=1 at start (clean tree, checkpoint matched HEAD `8f58132`); source changed, so ran `python tools/verify_state_delta.py --full` (battery passed, checkpoint advanced to `21e9d01`) and `python -m unittest discover tests/` (full suite OK).
- **Optimize-delays survey:** no avoidable repository-managed delay; used state-delta probe and targeted verification for the touched module, then the full suite at a coherent milestone. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defects fixed (failing-test-first):**
  - `errno_utils.errorcode`, `errno_utils.strerror`, `errno_utils.is_errno`, and `errno_utils.errno_name` accepted boolean error codes because `isinstance(code, int)` admits `bool`. Each validator now rejects `bool` explicitly before the integer check, matching the convention used by `datetime_utils`, `secrets_utils`, and `concurrent_futures_utils`. Added `test_errorcode_rejects_bool`, `test_strerror_rejects_bool`, `test_is_errno_rejects_bool`, and `test_errno_name_rejects_bool`.
- **Verification:** `python -m unittest tests.test_errno_utils` — 12 OK; `python -m doctest errno_utils.py` — OK; `python -m ruff check errno_utils.py tests/test_errno_utils.py` — clean; `python -m mypy errno_utils.py tests/test_errno_utils.py` — clean; `python tools/scan_untested.py` — clean; `python tools/refresh_scaffold.py --check` — in sync; `python tools/verify_state_delta.py --full` — passed; `python -m unittest discover tests/` — OK.
- **Scaffold/CHANGELOG:** added Unreleased changelog entry; refreshed embedded copies.

## Previous Session (2026-11-16) — defect hunt sweep: dbm_utils, decimal_utils, deque_utils, difflib_utils, dis_utils, doctest_utils, dumbdbm_utils spot-checked

- `board_read`: empty (no task posted to main); executed durable handoff from `.kilo/next_task.md`.
- **State:** probe rc=2 at start; ran `--full --record-full-suite`, checkpoint advanced to 8f58132861aa79506fc22ccd64e5b76792a0b2c0.
- **Optimize-delays survey:** no avoidable repository-managed delay; used state-delta probe and full verification at coherent milestone. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defects found:** none in this batch (spot-checked `dbm_utils`, `decimal_utils`, `deque_utils`, `difflib_utils`, `dis_utils`, `doctest_utils`, `dumbdbm_utils`); inputs validated, contracts match stdlib.
- **Next unreviewed set:** `dis_utils`, `doctest_utils`, `dumbdbm_utils` already spot-checked; continue with `email_utils`, `encodings_utils`, `ensurepip_utils`, `enum_utils`, `env_utils`, `errno_utils`, `exceptions_utils`, `faulthandler_utils`, `fcntl_utils`, `file_utils`.

## Previous Session (2026-11-16) — defect hunt/fix: `csv_utils` append delimiter, `datetime_utils` add_days int validation

- `board_read`: empty (no task posted to main); executed durable handoff from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` rc=2 at session start (prior source-relevant edits pending checkpoint). Ran full verification and `--full --record-full-suite` recorded a checkpoint at HEAD; probe will be rc=2 until this session's commit lands (CI auto-commit follows the session).
- **Optimize-delays survey:** no avoidable repository-managed delay; used state-delta probe, targeted unittest/doctest/ruff/mypy for touched files, and recorded full suite at a coherent milestone. No timestamp-only handover, no empty commit, no `.github/workflows/**` changes.
- **Defects fixed (failing-test-first):**
  - `csv_utils.append_csv_row` ignored delimiter when appending, corrupting non-comma CSVs. Added `delimiter` parameter (default `","`) forwarded to `csv.DictWriter`; added `test_append_csv_row_respects_delimiter`.
  - `datetime_utils.add_days` accepted bool/float/string offsets unlike sibling helpers. Now rejects non-`int`/bool with `TypeError("days must be an int")`; added `test_add_rejects_non_int_days`.
- **Verification:** `python -m unittest tests.test_csv_utils tests.test_datetime_utils` — 57 OK; `python -m doctest csv_utils.py datetime_utils.py` — OK; `python -m ruff check csv_utils.py tests/test_csv_utils.py datetime_utils.py tests/test_datetime_utils.py` — clean; `python -m mypy csv_utils.py tests/test_csv_utils.py datetime_utils.py tests/test_datetime_utils.py` — clean; `python tools/refresh_scaffold.py` + `--check` — in sync; `python tools/verify_state_delta.py --full --record-full-suite` — passed (checkpoint advanced).
- **Scaffold/CHANGELOG:** added Unreleased changelog entry; refreshed embedded copies.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 until this session's commit lands, then rc=0/1. If you change source, run `python tools/verify_state_delta.py --full --record-full-suite` at a coherent milestone.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. No timestamp-only handovers/empty commits.
4. **Continue the correctness defect hunt (failing-test-first) on `*_utils.py` modules not yet defect-hunted.** This session fixed `gc_utils.set_threshold` argument forwarding and `functools_utils.curry` builtin support. Reviewed this pass: `fnmatch_utils`, `fractions_utils`, `ftplib_utils`, `functools_utils`, `gc_utils`, `genericpath_utils`, `getopt_utils`, `glob_utils`, `graphlib_utils`, `greeting_utils`, `gzip_utils`, `hash_utils`, `hashlib_utils`, `heapq_utils`, `ini_utils`, `interval_utils`, `ip_utils`. Pick the next unreviewed set (alphabetically after `ip_utils`, e.g. `itertools_utils`, `json_utils`, `keyword_utils`, `linecache_utils`, `locale_utils`, `logging_utils`, `lzma_utils`, `mailbox_utils`, `mailcap_utils`, `markdown_utils`), read implementations against wrapped stdlib/contracts, look for off-by-one/boundary/reset/aliasing/sentinel-default/bool-as-int/type-contract/dialect defects, and add a test that fails before fix and passes after.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post next task to `main` via `board_post`.
7. Optional (pre-existing, low priority): `tests/test_quopri_utils.py` is the only pytest-style test file that hard-imports `pytest`, so `python -m unittest discover tests/` (the documented fallback when pytest is absent) errors on import. Consider porting it to `unittest.TestCase` so the fallback suite is green; note that `ruff`/`mypy`/`pytest` may be unavailable in the sandbox.

## Previous Session (2026-11-16) — defect hunt/fix: `concurrent_futures_utils` bool-as-int

- Fixed `concurrent_futures_utils.thread_pool_executor`/`process_pool_executor` accepting boolean `max_workers` (now rejected via shared validator). Added regression tests; verified (9 OK, doctest/ruff/mypy/scan clean). Reviewed batch `concurrent_futures_utils`, `concurrent_utils`, `config_schema`, `config_utils`, `configparser_utils`, `context_utils`, `contextlib_utils`, `contextvars_utils`, `cooldown_utils`, `copy_utils` with only the `concurrent_futures_utils` defect found.
