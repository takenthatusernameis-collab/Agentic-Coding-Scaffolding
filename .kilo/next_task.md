# Task for Next Agent

Session (2026-11-26): Verification battery passed; `verify_state_delta --probe` returned 0 (HEAD verified); full test suite blocked on multiprocessing hang; mypy on sources shows 17 errors in 3 files (platform/version-specific); `scan_untested` reports 0 untested exports; docstring coverage 88%; **test coverage 30%** (79,628 statements, 56,118 missed). No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Target the test coverage bottleneck (currently 30%). Pick a low-coverage module family from the coverage report (e.g., `number_utils` 10%, `prime_utils` 11%, `bytes_utils` 17%, `itertools_utils` 14%, `posix_utils` 24%) and add meaningful unit tests to raise overall coverage above 35%.
4. Use `python -m coverage run -m pytest tests/test_<module>.py` and `coverage report --show-missing` to guide line-level gaps.
5. Ensure new tests follow existing patterns (test_* naming, Test* classes, `assert`/`assertEqual` style).
6. Run `make test` and `python tools/verify_state_delta.py --full` to validate.
7. Update handover files; post next task to board when a second participant exists.