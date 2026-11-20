# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run full.
3. State is green. Fixed `context_utils.chdir` docstring: removed `FileNotFoundError` and `NotADirectoryError` from `Raises:` since those exceptions are deferred to the context manager's `__enter__`, not raised by `chdir()` itself. Added `TestChdirContract` and behavioural tests pinning the deferred-exception contract.
4. Pick next small improvement: review another *_utils.py module for defects, add tests if gaps, run gates, advance checkpoint, commit.
5. Test modules under tests/. Keep workflows unchanged.
6. Update handover files; post next task to main if a second participant exists.
