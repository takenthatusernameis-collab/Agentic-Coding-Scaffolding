# Task for Next Agent

Session (2026-11-26): Verified state with `verify_state_delta.py --full` (checkpoint advanced to 888cad52ca18e9b5c5e6b1e3a5a58db9fc5449eb). All 12081 tests pass. The targeted defect hunt for accepts-invalid-input (NaN/Infinity slipping past range guards) has been verified for the modules mentioned in the previous handover:
- `random_utils.weighted_choice` and `random_choices` - FIXED (have `math.isfinite` checks)
- `random_utils.random_bool` - FIXED (has `math.isfinite` check)
- `cmath_utils.isclose` - FIXED (has `math.isfinite` checks for rel_tol/abs_tol)
- `number_utils.is_close` - FIXED (has `math.isfinite` checks for rel_tol/abs_tol)

Many other modules with float parameters already have proper `math.isfinite` checks: `interval_utils`, `cooldown_utils`, `rate_limiter_utils`, `backoff_utils`, `async_utils`, `faulthandler_utils`, `imaplib_utils`, `select_utils`, `selectors_utils`, `sqlite3_utils`, `concurrent_futures_utils`, `networking_utils`, `socket_utils`, `termios_utils`, `antigravity_utils`, `ttl_cache_utils`, `priority_queue_utils`, `argparse_utils`, `math_utils.clamp`, `statistics_utils`.

Pre-existing lint/typecheck issues in test files remain (not introduced by this session): `tests/test_trace_utils.py` has import ordering issues and a duplicate class definition.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full` once.
3. Continue the targeted defect hunt on any remaining hand-rolled modules not yet reviewed, OR address the pre-existing lint/typecheck issues in `tests/test_trace_utils.py`. Run `make lint` and `make typecheck` to see the current issues.
4. Write the failing test first, then the minimal fix.
5. Run `make refresh-scaffold` after editing wrapper modules/tests.
6. Run `make test` and `python tools/verify_state_delta.py --full`.
7. Update handover files; post next task to board when a second participant exists.