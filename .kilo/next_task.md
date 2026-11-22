# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc=1, state is already verified; no redundant full re-run unless a source-relevant change occurred. If rc=2, run `python tools/verify_state_delta.py --full --record-full-suite`.
3. Prior session summary — fixed a genuine defect in `rate_limiter_utils.py`: `acquire`/`acquire_blocking` now reject non-finite (NaN/inf) token counts via `math.isfinite()`, matching `__init__`'s finite-value contract; regression tests added; `scaffold.sh` re-embedded via `make refresh-scaffold`. State green at HEAD d38d2f38 (full battery passed: pytest 11979 passed / 4 skipped; ruff clean; mypy 574 files; refresh_scaffold --check in sync; scaffold sync tests OK).
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. All classic defect classes previously swept (incl. NaN/inf/bool token counts in rate limiter); audit_contracts reports low-signal candidates only. `tests/test_doctests.py` already enforces every top-level doctest example.
5. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
6. Routine gates at coherent milestone.
7. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
8. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
9. Update handover files; post next task to main when a second participant exists.