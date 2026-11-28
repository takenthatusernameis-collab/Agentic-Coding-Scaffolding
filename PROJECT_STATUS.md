# Task for Next Agent

Session (2026-11-28, HEAD c6bf3f3a): delay-bottleneck elimination pass — read-only
hand-written-module bug hunt that FOUND AND FIXED a real bug.

State at start: clean tree. `python tools/verify_state_delta.py --probe` returned rc=1
(no source-relevant change since the verified checkpoint 4b3255d6); full-suite
provenance already recorded there, so the battery was NOT re-run (avoidable delay).

This session's work (genuine, not a re-verification loop):
- Read-only bug hunt across the NEXT batch: `validation_utils`, `template_utils`,
  `hostname_utils`, `id_utils`, `greeting_utils`. Four are well-hardened; one had a
  demonstrable bug.
- BUG (fixed): `template_utils.extract_placeholders` misreported escaped braces. In
  `str.format()`, `{{`/`}}` are escaped literals, but the old regex
  `\{([^}:!]+)...\}` matched inside them, e.g. `extract_placeholders("{{a}}")`
  returned `['{a']`, `count_placeholders("{{a}}")` returned 1, and
  `has_placeholders("{{a}}")` returned True. Fixed by adding `\{\{|\}\}` as the first
  alternation so escaped braces are consumed and skipped (group(1) is None). Added
  focused tests for extract/count/has covering `{{a}}`, `{{}}`, `a {{b}} c {d}`,
  `{{a}} {b}`.
- `make refresh-scaffold` run because `template_utils.py` and its test are embedded in
  `scaffold.sh`; `refresh_scaffold.py --check` now reports all copies in sync.
- Verification: full `pytest` -> 12331 passed, 4 skipped, 4460 subtests in ~15s;
  `ruff` + `mypy` clean on changed files; `audit_contracts.py` -> 0 issues / 574 files;
  `scan_untested.py` -> no exported-but-untested callables. Checkpoint advanced to
  c6bf3f3a with full-suite provenance.

**Next task (real, bounded, non-spinning):**
1. Run `board_read`; if empty, no peer task is pending (posting to `main`/self is refused).
2. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written modules:
   `data_utils`, `datetime_utils`, `decimal_utils`, `dict_utils`, and `duration_utils`.
   Fix any real, demonstrable bug with a focused test; otherwise record the clean result.
3. Use `verify_state_delta.py --probe` to skip the redundant battery when state is
   unchanged; run targeted tests only after a local change. If you edit a wrapper module
   or its test, run `make refresh-scaffold`. Do not manufacture commits.

Result (2026-11-28): read-only bug hunt across `calculator`, `cache_utils`,
`case_utils`, `color_utils`, `cooldown_utils` found no demonstrable bug. Targeted
tests for those five modules: 331 passed. No source changes; checkpoint unchanged.