# Task for Next Agent

Session (2026-11-28, HEAD e81cbac8): read-only bug hunt batch — one real bug found and fixed.

State at start: clean tree. `python tools/verify_state_delta.py --probe` returned rc=1 (no source-relevant change since the verified checkpoint); full-suite battery NOT re-run (avoidable delay).

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across the batch: `memoize_utils`, `mimetypes_utils`, `mmap_utils`, `modulefinder_utils`, `multiprocessing_utils`. Existing tests pass (144 tests); edge-case probes matched documented contracts for all but one module.
- **BUG (fixed): `mmap_utils.create_file_mmap` leaked the underlying file descriptor** — the `fd` opened via `os.open` was never closed after the mmap was created, so it stayed open for the process lifetime. Fixed by closing `fd` in a `finally` block after the mmap is created (closing the fd after mmap creation is safe on POSIX; the mapping remains valid). Added focused test `test_create_file_mmap_closes_underlying_fd` asserting open-fd count returns to baseline after close.
- `make refresh-scaffold` run; `refresh_scaffold.py --check` reports all embedded copies in sync.
- Verification: targeted `tests.test_mmap_utils` -> 9 OK; `ruff check` clean; `mypy` clean on `mmap_utils.py`. `memoize_utils`, `mimetypes_utils`, `modulefinder_utils`, `multiprocessing_utils` had no demonstrable bug; existing tests pass (144 total across the batch).

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused — record in `.kilo/next_task.md` instead).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules (subsequent to `memoize_utils`, `mimetypes_utils`, `mmap_utils`, `modulefinder_utils`, `multiprocessing_utils`): `netrc_utils`, `networking_utils`, `nntplib_utils`, `ntpath_utils`, and `nturl2path_utils`. Fix any real, demonstrable bug with a focused test; otherwise record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is unchanged; run targeted tests only after a local change. If you edit a wrapper module or its test, run `make refresh-scaffold`. Do not manufacture commits.
