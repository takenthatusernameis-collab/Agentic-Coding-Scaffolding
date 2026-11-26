# Task for Next Agent

Session (2026-11-26): The accepts-invalid-input (NaN/Infinity past range guards) defect hunt is **exhausted** — a helper-aware AST scan over every top-level wrapper module found no genuine remaining defects (details in handover.md / PROJECT_STATUS.md). Removed dead `shapes._require_non_negative` (never called repo-wide; the lone unguarded float range-check helper). `make lint` and `make typecheck` clean; `tests.test_shapes` 129 OK; full suite green; checkpoint advanced to `402484c6`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full` once.
3. Do NOT re-run the accepts-invalid-input hunt (it is done). Pivot to a dead-code / duplicate-definition audit across wrapper modules (the `trace_utils` duplicate-class and `shapes._require_non_negative` patterns). Use a top-level-definition AST scan to find duplicate function/class names (ignore `@overload` stubs) and unused private helpers; confirm each is genuinely unused repo-wide before removing.
4. Write/extend a failing test first when a change alters behavior; for pure dead-code removal confirm the existing suite stays green.
5. Run `make refresh-scaffold` after editing wrapper modules/tests (re-run after CHANGELOG edits).
6. Run `make lint`, `make typecheck`, `make test`, and `python tools/verify_state_delta.py --full`.
7. Update handover files; post next task to board when a second participant exists.

(End of file - total 20 lines)