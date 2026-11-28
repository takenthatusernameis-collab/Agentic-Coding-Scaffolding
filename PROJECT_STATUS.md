# Task for Next Agent

Session (2026-11-28, HEAD 8f1d8458): delay-bottleneck elimination pass — read-only
bug hunt across `greeting_utils`, `hash_utils`, `heapq_utils`, `html_utils`,
`http_utils`.

This session's work:
- DOC BUG (fixed): `greeting_utils.format_names` summary line claimed a
  "comma-separated list" while the implementation, the detailed Returns
  contract, and the tests all use space separation. Corrected the summary to
  "space-separated". Refreshed scaffold.sh; `refresh_scaffold.py --check`
  reports in sync; targeted tests, ruff, and mypy pass.
- Other four modules reviewed: no demonstrable bug found. Edge-case probes
  (empty inputs, bool rejection, negative n, unknown algorithm, tag-like
  text) all matched documented contracts.

**Next task (real, bounded, non-spinning):**
1. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
   modules: `id_utils`, `imghdr_utils`, `importlib_utils`, `ini_utils`, and
   `inspect_utils`. Fix any real, demonstrable bug with a focused test;
   otherwise record the clean result.
2. Use `verify_state_delta.py --probe` to skip the redundant battery when state
   is unchanged; run targeted tests only after a local change. If you edit a
   wrapper module or its test, run `make refresh-scaffold`. Do not manufacture
   commits.

(End of file - total 26 lines)