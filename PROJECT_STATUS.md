# Task for Next Agent

Session (2026-11-28, HEAD d3bf18a6): read-only bug hunt across
`ip_utils`, `ipaddress_utils`, `itertools_utils`, `json_utils`, `keyword_utils`.

This session's work:
- All five modules reviewed; no demonstrable bug found. Existing tests pass
  (427 tests) and two edge-case probe rounds (bool/int/bytes inputs, leading-zero
  and IPv4-mapped normalization, packed round-trips, common-prefix/summarize/
  subnets boundaries, next/previous address limits, product/sliding-window/
  grouper/batched/nan edge cases, JSON scalar/bytes inputs, keyword non-str)
  all matched documented contracts. State-delta probe reported no source change
  since the last verified checkpoint, so the redundant battery was skipped.

**Next task (real, bounded, non-spinning):**
1. Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
   modules: `linecache_utils`, `locale_utils`, `logging_utils`, `lzma_utils`, and
   `mailbox_utils`. Fix any real, demonstrable bug with a focused test;
   otherwise record the clean result.
2. Use `verify_state_delta.py --probe` to skip the redundant battery when state
   is unchanged; run targeted tests only after a local change. If you edit a
   wrapper module or its test, run `make refresh-scaffold`. Do not manufacture
   commits.

(End of file - total 27 lines)