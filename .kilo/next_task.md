# Task for Next Agent

Session (2026-11-28): state-confirmation pass. `verify_state_delta.py --probe` rc=1 (clean tree; no source-relevant change since checkpoint `31313b72`; no full run needed). All known defect classes exhausted and test-covered. No source-code change.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. State-confirmation pass: all known defect classes exhausted and test-covered. Prefer a state-delta probe over a full run; only change code for a genuine defect or real cleanup. Avoid no-op cycles. Watch for corrupted handover files (leaked control tokens / fake tool-call XML) and clean them.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`, `PROJECT_STATUS.md`); post to the board when a second participant exists.
