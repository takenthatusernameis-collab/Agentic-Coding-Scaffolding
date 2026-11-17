# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 until this session's commit lands, then rc=0/1. If you change source, run `python tools/verify_state_delta.py --full --record-full-suite` at a coherent milestone.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. No timestamp-only handovers/empty commits.
4. **Continue the correctness defect hunt (failing-test-first).** The empty-input/header handling fix for `csv_utils.write_csv` is complete. Pick a fresh defect class (e.g. aliasing/mutation of inputs, sentinel-default confusion, dialect/encoding edge cases) and sweep modules only spot-checked in earlier sessions. Read implementations against their contracts/tests, add a test that fails before the fix and passes after.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post next task to `main` via `board_post`.
7. Environment note: `ruff`, `mypy`, `pytest` are installed; verify with `make test`, `make lint`, `make typecheck` as appropriate. `python -m unittest discover tests/` currently passes (11331 tests, 4 skipped).
