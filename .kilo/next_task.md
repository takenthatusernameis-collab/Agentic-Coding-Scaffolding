# Task for Next Agent

Session (2026-11-28, HEAD fe30136f): read-only bug hunt batch — no bug found.

State at start: `python tools/verify_state_delta.py --probe` returned rc=2 (source-relevant change since last checkpoint: mmap_utils.py, scaffold.sh, tests/test_mmap_utils.py); `--diff` ran the verification battery and advanced the checkpoint. Full-suite battery not re-run (avoidable delay).

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across the batch: `netrc_utils`, `networking_utils`, `nntplib_utils`, `ntpath_utils`, `nturl2path_utils`. Existing tests pass (130 tests); edge-case probes matched documented contracts for all five modules. No demonstrable bug found.
- No wrapper module or test was edited, so `make refresh-scaffold` was not required; no source changes to commit from this session.

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused — record in `.kilo/next_task.md` instead).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules (subsequent to `netrc_utils`, `networking_utils`, `nntplib_utils`, `ntpath_utils`, `nturl2path_utils`): `number_utils`, `numbers_utils`, `opcode_utils`, `operator_utils`, and `optparse_utils`. Fix any real, demonstrable bug with a focused test; otherwise record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is unchanged; run targeted tests only after a local change. If you edit a wrapper module or its test, run `make refresh-scaffold`. Do not manufacture commits.
