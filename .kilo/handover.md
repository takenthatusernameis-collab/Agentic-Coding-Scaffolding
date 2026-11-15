# Handover

## Latest Session (2026-11-15T01:36Z)

- `board_read`: empty (no task posted to main); executed the standing avoidable-delay task from the durable handover.
- **Integrity fix — `tools/verify_state_delta.py` computed its source delta with `git status --porcelain <ref> -- <pathspecs>`.** `git status` does not take a commit argument: a bare `<ref>` before `--` is a pathspec, so the command matched nothing and `_changed_and_untracked_since` returned an empty delta on a clean tree even after source files changed since the checkpoint. The clean-tree fast path then skipped the verification battery and the checkpoint could advance past unverified code. The tracked delta now comes from `git diff --name-only <ref>` and untracked files from `git status --porcelain --untracked-files=all`. Added `tests/test_verify_state_delta.py::TestDeltaAcrossCommits` (fails on the old form, passes on the fix).
- **Integrity fix — `tools/refresh_scaffold.py` `--check` cache blind spot + unfinished `embedded_blocks` memoization.** HEAD was red: the prior checkpoint added an unused `from functools import lru_cache` to `tools/refresh_scaffold.py` but never used it or re-embedded `scaffold.sh`, and the `--check` mtime fingerprint (from `managed_copy_paths`) omitted the embedded `tools/refresh_scaffold.py` copy, so `--check` falsely reported "in sync" while the generator held stale source. Two `tests/test_refresh_scaffold.py` tests failed. Completed the memoization (`embedded_blocks` now parses through `lru_cache`d `_find_blocks`; `anchor_for` over all 571 blocks dropped from ~33s to ~0.008s), folded every managed embedded block into `managed_copy_paths` (no more cache blind spots), and re-embedded `scaffold.sh`. Added `TestEmbeddedBlockCache` and `TestCheckCacheCoverage`.
- Validation: `python -m pytest tests/` — 11195 OK (skipped=4); `python -m pytest tests/test_refresh_scaffold.py` — 38 OK; `python -m pytest tests/test_verify_state_delta.py` — 34 OK; `python -m ruff check .` clean; `python -m mypy . --exclude build --exclude dist` clean (567 source files); `python tools/scan_untested.py` clean; `python tools/refresh_scaffold.py --check` in sync; `python tools/verify_state_delta.py --probe` => rc=2.

## State

- Working tree: `tools/verify_state_delta.py`, `tools/refresh_scaffold.py`, `tests/test_verify_state_delta.py`, `tests/test_refresh_scaffold.py`, `CHANGELOG.md` (+ embedded copy in `scaffold.sh`) modified (non-workflow). CI auto-commits non-workflow changes.
- `python tools/verify_state_delta.py --probe` => rc=2 (verification/tests required for this delta).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect a battery run for the changed `tools/`+`tests/`+`CHANGELOG.md` delta, then a clean fast path after auto-commit).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). The two handover candidates are now resolved: `tests/test_refresh_scaffold.py` (`embedded_blocks` memoized; `anchor_for` no longer rescans the 6 MB generator per block) and the `refresh_scaffold --check` cache blind spot. Look for the next real one (measure first).
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `python tools/refresh_scaffold.py` and `--check` when embedded sources changed; run `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; run full suite when `tests/` or shared behavior changed; then `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).