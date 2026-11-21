# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`.
3. Continue routine regression monitoring and targeted defect hunt on hand-rolled modules not yet reviewed (NaN/Infinity, bool-as-number, silently ignored params, docstring contracts, boundary bugs). Candidate: fractions_utils, prime_utils, resource_utils, trace_utils, numbers_utils, math_utils, posix_utils, subprocess_utils, ssl_utils.
4. Routine gates: unittest discover, ruff, mypy, refresh_scaffold --check, verify_state_delta --full.
5. Keep `.github/workflows/**` unchanged.