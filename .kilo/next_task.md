# Task for Next Agent

Session (2026-11-28, HEAD fd4e5479): read-only bug hunt batch complete — CLEAN result.

State at start: clean tree. `python tools/verify_state_delta.py --probe` returned rc=1 (no source-relevant change since the verified checkpoint); full-suite provenance already recorded there, so the battery was NOT re-run (avoidable delay).

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across the batch: `calculator`, `cache_utils`, `case_utils`, `color_utils`, `cooldown_utils`. All five are well-hardened; no real, demonstrable bug was found.
- Targeted tests: `python -m unittest tests.test_calculator tests.test_cache_utils tests.test_case_utils tests.test_color_utils tests.test_cooldown_utils` — 331 OK.
- No code change, no empty commit (clean hunt per delay-bottleneck guidance).

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused — record in `.kilo/next_task.md` instead).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules (subsequent to `calculator`, `cache_utils`, `case_utils`, `color_utils`, `cooldown_utils`). Fix any real, demonstrable bug with a focused test; otherwise record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is unchanged; run targeted tests only after a local change. If you edit a wrapper module or its test, run `make refresh-scaffold`. Do not manufacture commits.
