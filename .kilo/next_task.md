# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 until this session's commit lands, then rc=0/1. If you change source, run `python tools/verify_state_delta.py --full --record-full-suite` at a coherent milestone.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. No timestamp-only handovers/empty commits.
4. **Continue the correctness defect hunt (failing-test-first) on `*_utils.py` modules not yet defect-hunted.** This session spot-checked `dbm_utils`, `decimal_utils`, `deque_utils`, `difflib_utils`, `dis_utils`, `doctest_utils`, `dumbdbm_utils` without confirmed defects. Next unreviewed set: `email_utils`, `encodings_utils`, `ensurepip_utils`, `enum_utils`, `env_utils`, `errno_utils`, `exceptions_utils`, `faulthandler_utils`, `fcntl_utils`, `file_utils`.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post next task to `main` via `board_post`.
