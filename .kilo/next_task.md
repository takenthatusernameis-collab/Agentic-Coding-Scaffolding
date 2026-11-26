# Task for Next Agent

Session (2026-11-26): Fixed a genuine accepts-invalid-input defect — `number_utils.is_close` accepted `float("nan")`/`float("inf")`/`float("-inf")` for `rel_tol`/`abs_tol` (only `< 0` was checked). Added `math.isfinite` guards; added `test_nan_tolerances_raise`/`test_infinite_tolerances_raise`. Full battery green, checkpoint advanced to `db100fe29c841dff2dc690e2a2fa810cd1f48c9a`. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full` once.
3. Continue the targeted defect hunt on hand-rolled modules not yet reviewed. The classic accepts-invalid-input class (NaN/Infinity slipping past `< 0`/`<= 0` guards) is the highest-yield pattern; grep for `< 0`/`<= 0` guards that lack a preceding `math.isfinite` check. Other classes already swept: delegation errors, test-isolation side effects, symmetric-difference, off-by-one.
4. Write the failing test first, then the minimal fix; follow existing test patterns (`Test*` classes, `assertRaises`, `asyncio.run`/`IsolatedAsyncioTestCase`).
5. After editing any wrapper module or test, run `make refresh-scaffold` so the embedded copies in `scaffold.sh` stay byte-identical (a stale copy fails `tests.test_scaffold_sync` and blocks the checkpoint).
6. Run `make test` and `python tools/verify_state_delta.py --full` to validate.
7. Update handover files; post the next task to the board when a second participant exists (otherwise record in `.kilo/next_task.md` and `.kilo/handover.md`).