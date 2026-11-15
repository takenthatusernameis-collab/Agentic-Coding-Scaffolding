# Handover

## Latest Session (2026-11-15T03:21Z)

- `board_read`: empty (no task posted to main). `python tools/verify_state_delta.py --probe` rc=1 (working tree clean, no source-relevant file changed since verified checkpoint `1b6b4df`); `refresh_scaffold.py --check` in sync; `scan_untested.py` clean; `ruff`/`mypy` clean per prior verified state.
- **Optimize-delays measurement (evidence):** probed hot-path tools — `verify_state_delta --probe` ~0.06s real, `refresh_scaffold --check` ~0.22s real (cache hit, `.kilo/refresh_scaffold_cache.json` present), `scan_untested` ~0.04s real (cache hit), `select_tests --from-git --include-untracked` ~0.05s real. `make test` already short-circuits on probe rc=0/1 to skip redundant smoke/full runs. `scan_untested --all` remains exhausted (TypeVar/constant/class/re-export/entry-point noise only). No remaining high-leverage **AVOIDABLE_PROCESS_DELAY** identified in repository-managed tooling without weakening guarantees; `.github/workflows/**` edits are out of scope (maintainer-managed).
- No source/test behavior changes this session (documentation/state handover update only). No embedded module/test/doc template changed; `refresh_scaffold --check` remains in sync.

## State

- Working tree: `.kilo/handover.md`, `PROJECT_STATUS.md`, `CHANGELOG.md` modified (non-workflow). CI auto-commits non-workflow changes.
- Checkpoint: `1b6b4df` (full suite recorded). After auto-commit expect `verify_state_delta --probe` rc=0 at HEAD.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py --probe` (expect rc=0 clean/verified at HEAD after the auto-commit).
3. Continue optimize-delays pass (`.kilo/command/optimize-delays.md`): if any **AVOIDABLE_PROCESS_DELAY** remains in repository-managed CI/dev tooling, measure with evidence and remove it without weakening guarantees (no `.github/workflows/**` edits). Current hot paths are cached/fast; `scan_untested --all` exhausted.
4. If no avoidable delay is found, do independent permitted work that adds durable value (e.g. edge-case/portability tests for an under-covered exported helper, or a small hermetic utility consistent with existing API conventions) rather than a no-op commit.
5. Validation: edit sources/docs first, then `python tools/refresh_scaffold.py` and `--check` when embedded sources changed; run `scan_untested.py`, targeted tests, `make lint`, `make typecheck`; run full suite when `tests/` or shared behavior changed; then `python tools/verify_state_delta.py --full --record-full-suite` as appropriate.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` (before refresh when applicable), `.kilo/handover.md`, `PROJECT_STATUS.md`; post next task to `main` via `board_post` (record if self-post refused).
