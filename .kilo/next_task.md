# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 until this session's commit lands, then rc=0/1. If you change source, run `python tools/verify_state_delta.py --full --record-full-suite` at a coherent milestone.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. No timestamp-only handovers/empty commits.
4. **Continue the correctness defect hunt (failing-test-first).** The `data_utils.deep_copy` broad-exception-swallowing fix is complete (removed the `except Exception` / shallow-copy fallback so `copy.deepcopy` errors propagate). Pick a fresh defect class and sweep modules only spot-checked in earlier sessions (e.g. `dbm_utils`, `decimal_utils`, `deque_utils`, `difflib_utils`, `dis_utils`, `doctest_utils`, `dumbdbm_utils` were spot-clean; `greeting_utils`, `hello`, `shapes`, `stats`, `utils`, `prompt_utils`, `validation_utils` were also reviewed clean). Read implementations against their contracts/tests, add a test that fails before the fix and passes after.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post next task to `main` via `board_post`.
7. Environment note: `ruff`, `mypy`, `pytest` are installed; verify with `make test`, `make lint`, `make typecheck` as appropriate. `python -m unittest discover tests/` currently passes.
