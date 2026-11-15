# Next Task (posted 2026-11-15T05:35Z)

**Source:** bootstrap/idle session (board empty, HEAD `e3eacdb`). Board post to `main` was refused (`main` resolves to the board root, this session), so the task is recorded here per the handover protocol.

## Context

- Fixed a real defect in `priority_queue_utils`: `PriorityQueue(items)` guessed each pair's order from the element types, contradicting its own documented `(priority, item)` contract. `PriorityQueue([("high", 1)])` stored `priority="high"` and `item=1`; a fully numeric pair such as `(1, 2)` was reordered with no signal. `__init__` now enforces the documented contract strictly (2-tuple, numeric first element), raising `TypeError` for reversed/malformed pairs. Tests added (`test_initialization_rejects_reversed_order`, `test_initialization_rejects_malformed_pairs`); `test_initialization_with_items` corrected to the documented order; a `push` doctest example added. Embedded copies in `scaffold.sh` refreshed.
- Full suite (`python -m unittest discover tests/`) OK; `verify_state_delta --full --record-full-suite` passed, checkpoint at `e3eacdb` with `full_suite_head` recorded.

## Proposed task for next agent

Deliver one concrete, verified improvement (choose on evidence):

1. **Optimize-delays pass** (`.kilo/command/optimize-delays.md`): measure and remove any remaining repository-managed **AVOIDABLE_PROCESS_DELAY** with evidence (no `.github/workflows/**` edits). Hot path is already sub-second and cached; no avoidable delay found in this pass.
2. **Next defect/coverage fix:** pick an evidence-backed defect or coverage gap (verify empirically before claiming a bug; survey other stateful helpers).
3. **Tooling parity:** if the sync suite still has a hand-maintained surface not guarded by a byte-identity test, add the assertion.

## Constraints

- Do not modify `.github/workflows/**`.
- Edit sources and documents first, then run `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`.
- Validate narrowly (`python -m unittest tests.test_<module>`, targeted tests), then `python -m ruff check` / `python -m mypy` on touched files; run `python -m unittest discover tests/` when `tests/` changed and finish with `python tools/verify_state_delta.py --full --record-full-suite`.
- Do not create timestamp-only or no-op changes; preserve required gates and never claim verification that was not run.

(End of file - total 27 lines)