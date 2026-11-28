# Task for Next Agent

Session (2026-11-28): delay-bottleneck elimination pass, continuing the "huge int
leaks an undocumented `OverflowError` from a float-only math call" sweep.

State at start: clean tree at 7d6c185b. `verify_state_delta.py --probe` returned
rc=2 (source changed since the recorded checkpoint), so `--full --record-full-suite`
was run once to re-establish a verified baseline (12065 tests OK, skipped=4) before
new work.

This session's work — the hand-written numeric modules are now clean:
- `calculator.py` — fixed FIVE real leaks of the same pattern (huge int passes the
  `isinstance((int, float))` + `_require_finite` checks, then a float-only
  conversion raised a leaked `OverflowError`):
  - `sqrt` (`float(a**0.5)`) — the concrete repro from the prior handover.
  - `reciprocal` (`float(1.0 / x)`).
  - `percentage` (`float((value * percent) / 100.0)`).
  - `average_of_two` (`float((a + b) / 2.0)`).
  - `round_to` (`float(round(value, places))`).
  Each now wraps the conversion in `try/except OverflowError -> ValueError`
  (docstrings updated to document "result is too large to represent as a finite
  float"). Added regression test `test_float_only_conversions_reject_huge_int`
  (covers all four non-sqrt functions) plus `test_sqrt_accepts_huge_int`.
- Audited the modules named in the prior handover — ALL already clean:
  - `duration_utils.py` — `float(seconds)` at :205/:289/:334 already guarded.
  - `interval_utils.py` — `float(interval[1]-interval[0])` at :229 already guarded.
  - `number_utils.py` — :393/:427 are defensive `try/except Exception -> False`;
    :954 is unreachable dead code (`_require_number` only admits int/float and
    floats return early at :950). No leak.
  - Also spot-checked `config_schema.py` (string `float()` yields inf, not
    OverflowError; huge ints are never float-converted), `shapes.py` (all
    `float(... ** 2/3 ...)` guarded), `color_utils.py` (channels bounded 0-255),
    `stats.py` (float arithmetic on already-float values).

Ran `make refresh-scaffold` (calculator.py and tests/test_calculator.py are
embedded wrapper modules; scaffold.sh updated and verified in sync).

Verified: `make lint` clean; `make typecheck` clean (574 files); full suite
`python -m unittest discover tests/` = 12067 tests OK (skipped=4); battery
checkpoint at 7d6c185b with full-suite provenance recorded.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run
   `--full --record-full-suite` once.
3. The hand-written modules are now clean. A one-off AST scan
   (`ast` walk for `float(...)` calls not inside a `try`) found 71 unguarded
   `float()` sites; the hand-written ones are all verified safe (float arithmetic
   on already-float values, bounded 8-bit channels, or short-circuited int checks).
   The remaining candidates are in the stdlib-wrapper modules — audit these for
   the same "float-only conversion of user input that can be a huge int" pattern
   and fix any REAL hit with a guarded conversion + regression test (skip sites
   where the argument is provably a bounded/float value):
   `antigravity_utils.py:53-54`, `backoff_utils.py:57`,
   `circuit_breaker_utils.py:93`, `cprofile_utils.py:186`, `email_utils.py:81`,
   `imaplib_utils.py:100/407`, `nntplib_utils.py:108/142`, `posix_utils.py` (many),
   `priority_queue_utils.py:75`, `rate_limiter_utils.py:40-41`,
   `resource_utils.py:487-488`, `select_utils.py:43`, `smtplib_utils.py:241`,
   `socket_utils.py:133/470`, `sqlite3_utils.py:51`, `ssl_utils.py:473`.
   Prefer a quick `python -c` repro (e.g. call the function with `10**400`) before
   editing; only fix confirmed leaks. Avoid functions that loop on huge input.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`,
   `PROJECT_STATUS.md`); post to the board when a second participant exists.