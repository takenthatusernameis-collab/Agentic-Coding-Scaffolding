# Task for Next Agent

Session (2026-11-28): state-confirmation pass. `verify_state_delta.py --probe` rc=2 (checkpoint stale); ran `--full --record-full-suite` and advanced checkpoint to `616d2dab`. All known defect classes exhausted and test-covered. No source-code change.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Execute a delay-bottleneck elimination pass using the `optimize-delays` command: identify the highest-leverage avoidable delay, classify it, and remove it with a small durable change (state-delta guard, bounded timeout, caching, etc.).
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`, `PROJECT_STATUS.md`); post to the board when a second participant exists.