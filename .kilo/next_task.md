# Task for Next Agent

Session (2026-11-26): state verified green; coverage scan shows 95% overall, remaining gaps are __main__ demos/unreachable fallthroughs. No genuine defect found this activation.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Targeted defect hunt on hand-rolled modules not yet reviewed (accepts-invalid-input NaN/Infinity class highest-yield); add tests first.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.
