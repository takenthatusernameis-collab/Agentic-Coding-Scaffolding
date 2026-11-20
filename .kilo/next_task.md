# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run full.
3. Continue targeted defect hunt on hand-rolled modules not yet reviewed. Next focus: `stats.py` scalar params (trim_count, p, q, percentiles) for NaN/inf; `utils.py` chunk/sample edge cases; `greeting_utils.py`, `hello.py`.
4. Routine gates at coherent milestone.
5. Test modules under tests/. Keep workflows unchanged.
6. Update handover files; post next task to main if second participant exists.
