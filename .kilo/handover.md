# Task for Next Agent

Session (2026-11-27): fixed undocumented `ValueError` leaks in `cmath_utils` — `sin`, `cos`, `tan` raise `ValueError: math domain error` for infinite inputs, and `atanh` raises it for `z == 1` or `z == -1`, all from `cmath` stdlib delegation. Documented each in `Raises:` with `# audit-ignore: ValueError` (matching the `log`/`log10` pattern) and added `TestDomainErrors` (4 tests) in `tests/test_cmath_utils.py`. Coverage stays 100%; ruff, mypy, doctest, audit, refresh-scaffold, and verify_state_delta all pass. Checkpoint advanced to HEAD `c6b177df`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue the undocumented-exception / stdlib-delegation audit on remaining wrapper modules not yet swept (e.g. `date_utils`, `time_utils`, `fractions_utils`, `decimal_utils`): probe with edge inputs (NaN, ±inf, 0, boundary values), document any leaked exceptions in `Raises:` with `# audit-ignore:`, write failing tests first; prefer state-delta checks; record in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.
