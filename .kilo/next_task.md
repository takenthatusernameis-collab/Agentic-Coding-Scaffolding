# Task for Next Agent

Session (2026-11-26): Resolved all pre-existing lint/typecheck issues in `tests/test_trace_utils.py` (removed duplicate `TestRunScriptTracedEdgeCases` class; fixed 7 import-ordering violations). Ran `make refresh-scaffold`; scaffold sync check passes. `make lint` and `make typecheck` are now fully clean. Full suite: 11842 tests OK (skipped=4). `verify_state_delta.py --full` passed; checkpoint advanced to d8919ae411f1f528548684ec73d79f63e62f4824.

The accepts-invalid-input (NaN/Infinity past range guards) defect hunt is complete for all previously reviewed modules (see handover.md for the full list).

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full` once.
3. Continue the targeted defect hunt on any remaining hand-rolled wrapper modules not yet reviewed for accepts-invalid-input (NaN/Infinity slipping past range guards, or missing type/range validation). Prefer modules with numeric/float parameters lacking `math.isfinite` guards. Run `make lint` and `make typecheck` first to confirm a clean baseline.
4. Write the failing test first, then the minimal fix.
5. Run `make refresh-scaffold` after editing wrapper modules/tests.
6. Run `make test` and `python tools/verify_state_delta.py --full`.
7. Update handover files; post next task to board when a second participant exists.

(End of file - total 20 lines)