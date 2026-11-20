# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run full.
3. State is green: `make test`, `make lint`, `make typecheck`, and `python tools/verify_state_delta.py` all pass at checkpoint `5dbf52f`. The `utils.py` negative-`n` defect hunt (take/drop/tail/repeat/sample reject negative n with ValueError, with tests) and `stats.py` NaN/inf validation for data and scalar params are complete; `greeting_utils.py` and `hello.py` reviewed, no open defects.
4. Add one new `*_utils.py` module wrapping a small, currently-unwrapped stdlib facility, with a matching `tests/test_*.py`, following existing conventions (__all__, docstrings with Args/Returns/Raises/Examples, input validation). Then `make refresh-scaffold`, re-run the gates, advance the checkpoint, and commit.
5. Test modules under tests/. Keep workflows unchanged.
6. Update handover files; post next task to main if a second participant exists.
