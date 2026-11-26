# Task for Next Agent

Session (2026-11-26): Verification battery passed; `verify_state_delta --probe` rc=1 then --full rc=0; full test suite 12031 passed; mypy shows 17 errors in 3 files (platform/version-specific); test coverage ~32%. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Target test coverage bottleneck (~32%). Pick a low-coverage module family and add meaningful unit tests to raise overall coverage above 35%.
4. Use `python -m coverage run -m pytest tests/test_<module>.py` and `coverage report --show-missing` to guide line-level gaps.
5. Ensure new tests follow existing patterns (test_* naming, Test* classes, `assert`/`assertEqual` style).
6. Run `make test` and `python tools/verify_state_delta.py --full` to validate.
7. Update handover files.

(End of file)
