# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run full.
3. State is green. Improved `audioop_utils.py`: added fragment bytes validation, width range validation (1..4), finite factor check in audioop_mul.
4. Pick next small improvement: review another *_utils.py module for defects, add tests if gaps, run gates, advance checkpoint, commit.
5. Test modules under tests/. Keep workflows unchanged.
6. Update handover files; post next task to main if a second participant exists.