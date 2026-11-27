# Task for Next Agent

Session (2026-11-27): fractions_utils audit complete (ValueError leaks documented with # audit-ignore). Refresh-scaffold in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue the undocumented-exception / stdlib-delegation audit on remaining wrapper modules (e.g. `date_utils`, `time_utils`, `decimal_utils`): probe with edge inputs (NaN, ±inf, 0, boundary values), document any leaked exceptions in `Raises:` with `# audit-ignore:`, write failing tests first; prefer state-delta checks; record in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.
