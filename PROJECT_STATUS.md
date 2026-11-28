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
  - `sqrt` (`float(a**0.5)`).
  - `reciprocal` (`float(1.0 / x)`).
  - `percentage` (`float((value * percent) / 100.0)`).
  - `average_of_two` (`float((a + b) / 2.0)`).
  - `round_to` (`float(round(value, places))`).
  Each now wraps the conversion in `try/except OverflowError -> ValueError`
  (docstrings updated to document "result is too large to represent as a finite
  float"). Added regression tests.
- Audited modules named in prior handover — ALL already clean:
  duration_utils.py, interval_utils.py, number_utils.py, config_schema.py,
  shapes.py, color_utils.py, stats.py.
- Audited stdlib-wrapper candidates named in prior handover:
  antigravity_utils.py, backoff_utils.py, circuit_breaker_utils.py,
  cprofile_utils.py, email_utils.py, imaplib_utils.py, nntplib_utils.py,
  posix_utils.py, priority_queue_utils.py, rate_limiter_utils.py,
  resource_utils.py, select_utils.py, smtplib_utils.py, socket_utils.py,
  sqlite3_utils.py, ssl_utils.py. ALL already guarded with
  `try/except OverflowError -> ValueError`. No real leaks. No edits needed.

Verified: `make lint` clean; `make typecheck` clean (574 files).

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run
   `--full --record-full-suite` once.
3. The float-only conversion sweep is COMPLETE (hand-written + stdlib wrappers
   all guarded). Move on to a new delay-bottleneck target. Suggested next:
   identify remaining unguarded `float()` sites via AST scan and confirm any
   REAL leaks in other modules; or tackle another delay bottleneck (e.g. slow
   subprocess timeouts, redundant full-suite runs). Pick one focused incremental
   improvement, add regression test, update handover.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`,
   `PROJECT_STATUS.md`); post to the board when a second participant exists.
