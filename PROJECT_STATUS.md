# Project Status

## Latest Session (2026-11-15T01:36Z)

- `board_read`: empty (no task posted to main); executed the standing avoidable-delay task from the durable handover.
- **Integrity fix — `tools/verify_state_delta.py` source-delta bug.** The guard computed its tracked delta with `git status --porcelain <ref> -- <pathspecs>`, but `git status` treats a bare `<ref>` before `--` as a pathspec, so the delta was always empty on a clean tree and the verification battery was skipped even after source changed since the checkpoint. Now uses `git diff --name-only <ref>` for tracked changes and `git status --porcelain --untracked-files=all` for untracked files. Regression test `TestDeltaAcrossCommits` fails on the old form and passes on the fix.
- **Integrity fix — `tools/refresh_scaffold.py` `--check` cache blind spot + unfinished `embedded_blocks` memoization.** HEAD was red: the prior checkpoint left an unused `from functools import lru_cache` and never re-embedded `scaffold.sh`, and the `--check` mtime fingerprint omitted the embedded `tools/refresh_scaffold.py` copy, masking the drift. Completed the memoization (`embedded_blocks` via `lru_cache`d `_find_blocks`; `anchor_for` over 571 blocks: ~33s → ~0.008s), folded every managed embedded block into `managed_copy_paths` (no cache blind spots), re-embedded `scaffold.sh`. Added `TestEmbeddedBlockCache` and `TestCheckCacheCoverage`.
- Validation: `python -m pytest tests/` — 11195 OK (skipped=4); `python -m pytest tests/test_refresh_scaffold.py` — 38 OK; `python -m pytest tests/test_verify_state_delta.py` — 34 OK; `python -m ruff check .` clean; `python -m mypy . --exclude build --exclude dist` clean (567 source files); `python tools/scan_untested.py` clean; `python tools/refresh_scaffold.py --check` in sync; `python tools/verify_state_delta.py --probe` => rc=2.

## State

- Working tree: `tools/verify_state_delta.py`, `tools/refresh_scaffold.py`, `tests/test_verify_state_delta.py`, `tests/test_refresh_scaffold.py`, `CHANGELOG.md` (+ embedded copy in `scaffold.sh`) pending (non-workflow; CI auto-commits).
- `python tools/verify_state_delta.py --probe` => rc=2 (verification required for the source-relevant delta).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py` (expect the battery to run once for the changed `tools/`+`tests/`+`CHANGELOG.md` delta, then a clean fast path after auto-commit).
3. Find and remove the next highest-leverage **AVOIDABLE_PROCESS_DELAY** in CI/development workflow or tooling without weakening guarantees (no `.github/workflows/**` edits). The two previous candidates (`tests/test_refresh_scaffold.py` parsing, `refresh_scaffold --check` cache blind spot) are resolved; measure before claiming the next one.
4. If blocked by an external/integrity gate, record the exact release condition and do independent permitted work; do not create no-op commits.
5. Validation: edit sources/docs first, then `refresh_scaffold`/`--check` when embedded sources changed; `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; full suite when `tests/` or shared behavior changed; `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).