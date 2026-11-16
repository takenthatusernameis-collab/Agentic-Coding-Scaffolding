# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=0/1 now that the checkpoint is at HEAD `48f1b82`. Run `--full --record-full-suite` only when the probe reports a source-relevant change.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. Do not manufacture timestamp-only handovers or empty commits.
4. **Continue the correctness defect hunt (failing-test-first) on `*_utils.py` modules not yet defect-hunted.** The numeric/algorithm-heavy batch (`bit_utils`, `cmath_utils`, `decimal_utils`, `fractions_utils`, `math_utils`, `prime_utils`, `random_utils`, `statistics_utils`, `stats`) was completed this session with no defects found — every doctest, the full suite, ruff, mypy (568 files), `refresh_scaffold --check`, and `scan_untested --all` are green, and the checkpoint is at `48f1b82`. Pick the next set of unwrapped modules, read each implementation against the standard library it wraps, look for off-by-one/boundary/reset/aliasing defects, and add a test that fails before the fix and passes after.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.
