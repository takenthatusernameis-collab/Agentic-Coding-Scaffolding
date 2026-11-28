# Task for Next Agent

Session (2026-11-28, HEAD a5cf3d28): read-only bug hunt batch — one real bug found and fixed.

State at start: `python tools/verify_state_delta.py --probe` returned rc=1 (working tree clean; no source-relevant file changed since the last verified checkpoint at fe30136f).

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across the batch: `number_utils`, `numbers_utils`, `opcode_utils`, `operator_utils`, `optparse_utils`. Existing tests pass (674 tests) and edge-case probes matched documented contracts for all five modules.
- **`numbers_utils`**: Fixed a real, demonstrable bug in `is_perfect_power`: it used a float ``n ** (1.0 / b)`` estimate that raised ``OverflowError: int too large to convert to float`` for large perfect powers such as ``10**400`` (== ``(10**200)**2``) and ``2**2000``. Replaced with an exact integer Newton's-method nth-root helper (``_integer_nth_root``), matching the correct `number_utils.is_perfect_power`. Added a focused regression test (`test_large_perfect_power_does_not_overflow`) covering `10**400`, `2**2000`, and the near-miss `10**400 + 1`.
- `number_utils`, `opcode_utils`, `operator_utils`, `optparse_utils`: no demonstrable bug found; all edge-case probes matched documented contracts.
- Ran `make refresh-scaffold` to sync embedded copies in `scaffold.sh`; `refresh_scaffold.py --check` reports all embedded copies in sync.
- All 675 tests pass; ruff lint and mypy typecheck clean.

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused — record in `.kilo/next_task.md` instead).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules (subsequent to `number_utils`, `numbers_utils`, `opcode_utils`, `operator_utils`, `optparse_utils`): `os_utils`, `ossaudiodev_utils`, `path_utils`, `pathlib_utils`, and `pattern_utils`. Fix any real, demonstrable bug with a focused test; otherwise record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is unchanged; run targeted tests only after a local change. If you edit a wrapper module or its test, run `make refresh-scaffold`. Do not manufacture commits.
