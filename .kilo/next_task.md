# Task for Next Agent

Session (2026-11-28, HEAD d704e1c5): read-only bug hunt across `plistlib_utils`, `poplib_utils`, `posix_utils`, `posixpath_utils`, and `pprint_utils`.

State at start: board empty (bootstrap session); previous batch recorded in PROJECT_STATUS.md. `python tools/verify_state_delta.py --probe` returned rc=2 (HEAD ahead of the verified checkpoint); the verification battery ran and advanced the checkpoint to d704e1c5.

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across `plistlib_utils`, `poplib_utils`, `posix_utils`, `posixpath_utils`, and `pprint_utils`. Existing tests pass (147 tests) and edge-case probes matched documented contracts for all five modules.
- No demonstrable bug found in any of the five modules; recorded the clean result in PROJECT_STATUS.md.
- No wrapper module or test was edited, so `make refresh-scaffold` was not required; no source changes to commit from this session.

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused — record in `.kilo/next_task.md` instead).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules (subsequent to `plistlib_utils`, `poplib_utils`, `posix_utils`, `posixpath_utils`, `pprint_utils`): `profile_utils`, `pstats_utils`, `py_compile_utils`, `pyclbr_utils`, and `pyexpat_utils`. Fix any real, demonstrable bug with a focused test; otherwise record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is unchanged; run targeted tests only after a local change. If you edit a wrapper module or its test, run `make refresh-scaffold`. Do not manufacture commits.
