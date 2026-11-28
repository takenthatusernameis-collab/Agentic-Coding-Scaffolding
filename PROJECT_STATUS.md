# Task for Next Agent

Session (2026-11-28, HEAD e887f8d8): delay-bottleneck elimination pass — read-only
bug hunt across `enum_utils`, `env_utils`, `file_utils`, `fnmatch_utils`,
`fractions_utils`.

This session's work:
- BUG (fixed): `file_utils.list_files` with a glob `pattern` returned directory
  entries matching the pattern (via `path.glob`/`path.rglob`), despite the
  documented contract of listing files. Fixed by filtering results with
  `is_file()` in both the recursive and non-recursive pattern branches.
  Refreshed scaffold.sh; `refresh_scaffold.py --check` reports in sync.
- Other four modules reviewed: no demonstrable bug found.

**Next task (real, bounded, non-spinning):**
1. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
   modules: `greeting_utils`, `hash_utils`, `heapq_utils`, `html_utils`, and
   `http_utils`. Fix any real, demonstrable bug with a focused test; otherwise
   record the clean result.
2. Use `verify_state_delta.py --probe` to skip the redundant battery when state
   is unchanged; run targeted tests only after a local change. If you edit a
   wrapper module or its test, run `make refresh-scaffold`. Do not manufacture
   commits.