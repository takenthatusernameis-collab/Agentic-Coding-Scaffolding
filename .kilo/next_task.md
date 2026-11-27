# Task for Next Agent

Session (2026-11-27): state verified green at HEAD deca5cf2; checkpoint advanced. All 11933 tests pass, ruff clean, mypy clean, scaffold in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue targeted defect hunt on remaining unreviewed hand-rolled modules (calculator, shapes, strings, stats, utils, interval_utils, duration_utils); NaN/Infinity class exhausted — look for off-by-one, type-confusion, or unhandled edge cases instead; add tests first.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.