# Task for Next Agent

Session (2026-11-27): decimal_utils audit complete (decimal.InvalidOperation / decimal.Overflow leaks documented with # audit-ignore). Full battery green at HEAD `780db3ae`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue the undocumented-exception / stdlib-delegation audit on remaining wrapper modules not yet swept (e.g. `datetime_utils`, `email_utils`, `urllib_utils`, `http_utils`): probe with edge inputs (NaN, ±inf, 0, boundary values, malformed strings), document any leaked exceptions in `Raises:` with `# audit-ignore:`, write failing tests first; prefer state-delta checks; record in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.