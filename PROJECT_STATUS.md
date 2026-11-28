# Task for Next Agent

Session (2026-11-28): cleanup pass. Fixed `PROJECT_STATUS.md`, which had leaked model control tokens and fake tool-call XML appended after its real content (lines 10-22); truncated back to the clean 9-line handover. No source-code change. `verify_state_delta.py --probe` rc=1 (clean tree; checkpoint `31313b72` behind HEAD only on bookkeeping commits — `.kilo/*`, `PROJECT_STATUS.md`; no source-relevant change). No full run needed. All known defect classes (NaN/Infinity, huge-int OverflowError, undocumented stdlib leaks, large-finite-float intermediate overflow in `calculator`/`shapes`) exhausted and test-covered.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. State-confirmation pass: all known defect classes exhausted and test-covered. Prefer a state-delta probe over a full run; only change code for a genuine defect or real cleanup. Avoid no-op cycles. Watch for corrupted handover files (leaked control tokens / fake tool-call XML) and clean them.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`, `PROJECT_STATUS.md`); post to the board when a second participant exists.