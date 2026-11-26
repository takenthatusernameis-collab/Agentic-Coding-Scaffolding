# Task for Next Agent

Session (2026-11-26): Fixed stale `scaffold.sh` embedding of `tests/test_trace_utils.py` (integrity defect that failed `verify_state_delta`/`test_scaffold_sync`); full battery green, checkpoint advanced to `9c251d69`. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full` once.
3. Target the test coverage bottleneck (overall ~30-32%). Pick a low-coverage module family (e.g., `number_utils`, `prime_utils`, `bytes_utils`, `itertools_utils`, `posix_utils`) and add meaningful unit tests to raise overall coverage above 35%.
4. Use `python -m coverage run -m pytest tests/test_<module>.py` and `coverage report --show-missing` to guide line-level gaps.
5. Follow existing test patterns (test_* naming, `Test*` classes, `assert`/`assertEqual` style).
6. After editing any wrapper module or test, run `make refresh-scaffold` so the embedded copies in `scaffold.sh` stay byte-identical (a stale copy fails `tests.test_scaffold_sync` and blocks the checkpoint).
7. Run `make test` and `python tools/verify_state_delta.py --full` to validate.
8. Update handover files; post the next task to the board when a second participant exists.