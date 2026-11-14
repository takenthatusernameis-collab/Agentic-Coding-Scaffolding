# Project Status

## Latest Session (2026-11-14T21:42Z)

- `board_read`: no pending task/messages. Baseline probe showed clean verified checkpoint state (`verify_state_delta --probe` rc=1), scaffold embeds in sync, lint/mypy/smoke tests healthy.
- **Integrity fix:** `tools/verify_state_delta.py` now treats an unresolvable comparison ref as changed. `git status --porcelain <unknown-ref> ...` can exit 0 in this environment, which previously made `_changed_and_untracked_since` return no changes for refs like `000...0`; added `_ref_exists` (`git rev-parse --verify --quiet <ref>^{commit}`) so clean-state verification is not skipped when the ref cannot be compared. This also resolves the failing `tests.test_verify_state_delta.TestRepositoryState.test_source_changed_since_an_unknown_ref_is_true` observed during profiling.
- Validation: `python -m unittest tests.test_verify_state_delta` (27 OK), `python -m ruff check tools/verify_state_delta.py tests/test_verify_state_delta.py` (clean), `python -m mypy tools/verify_state_delta.py tests/test_verify_state_delta.py` (clean), `python tools/refresh_scaffold.py --check` (in sync), `python tools/scan_untested.py` (clean), `python -m unittest tests.test_public_api tests.test_doctests` (OK). No `.github/workflows/**` changes; no scaffold-embedded sources changed.

## State

- Working tree: `tools/verify_state_delta.py`, `CHANGELOG.md`, `.kilo/handover.md`, `PROJECT_STATUS.md` pending (non-workflow; CI auto-commits).
- Last verified checkpoint file currently reflects prior HEAD (`00039ca` context) until verification is advanced for new HEAD/changes as appropriate.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect clean fast path after auto-commit if unchanged).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). Profiling candidates: `TestStdlibModulefinder` (~5s total, opt-in), `test_verify_state_delta.py::TestCommandLine::test_the_check_mode_reports_a_synchronised_repository` (~1.0s), `test_doctests.py` (~0.76s), scaffold tests (~0.67–0.69s each), `scan_untested` cache/integration tests (~0.5s). Favor measured equal-coverage reductions (hermetic fixtures, caching/dedup of subprocess work, avoiding redundant checks) — do not weaken assertions.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).
