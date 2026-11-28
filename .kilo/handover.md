# Task for Next Agent

Session (2026-11-28, HEAD 3551deba): delay-bottleneck elimination pass — read-only
hand-written-module bug hunt (no code change; no genuine bottleneck found).

State at start: clean tree. `python tools/verify_state_delta.py --probe` returned rc=1
(no source-relevant change since the verified checkpoint 4b3255d6); full-suite
provenance already recorded there, so the battery was NOT re-run (avoidable delay).

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across the NEXT batch: stats (1804 lines), shapes (905),
  strings (3409), config_schema (624), and prime_utils lines ~1990-2180
  (cuban/proth/cullen/woodall primes, primes_between). All are well-hardened
  (input validation, OverflowError->ValueError guards, exact integer roots,
  correct number-theoretic predicates); no demonstrable bug found.
- `python tools/audit_contracts.py` -> 0 issues across 574 files.
- `python tools/scan_untested.py` -> no exported-but-untested callables.
- Targeted battery: `pytest tests/test_stats.py tests/test_shapes.py
  tests/test_strings.py tests/test_config_schema.py tests/test_prime_utils.py`
  -> 1766 passed, 204 subtests passed in ~1s.
- No source edit made: per the delay-bottleneck policy, no no-op/manufactured commit.

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules:
   `validation_utils`, `template_utils`, `hostname_utils`, `id_utils`, and
   `greeting_utils`. Fix any real, demonstrable bug with a focused test; otherwise
   record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is
   unchanged; run targeted tests only after a local change. Do not manufacture commits.