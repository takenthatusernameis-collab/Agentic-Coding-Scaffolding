# Project Status

## Latest Session (2026-11-14T13:05Z)

- `board_read`: no pending task/messages for this session (bootstrap/idle session); task recovered from `.kilo/next_task.md` and `.kilo/handover.md`.
- State-delta caught a real integrity regression: `python tools/verify_state_delta.py` refused to advance the checkpoint because `python tools/refresh_scaffold.py --check` reported `stale: README.md` and `stale: CHANGELOG.md`. Commit `3312fec` had edited both documents after refreshing `scaffold.sh`, so the generator embedded two stale document templates. This is the second occurrence (previous session also repaired a stale `CHANGELOG.md`).
- Repair + structural guard: refreshed the two embedded copies (`python tools/refresh_scaffold.py`), then closed the blind spot in `tests/test_scaffold_sync.py` — the existing tests only assert that the embedded documents *mention* every module. Added `test_the_embedded_documents_match_the_repository_templates`, which compares every `refresh_scaffold.TEMPLATED_COPIES` document against `templated_body(...)` byte for byte, so `make test` fails on drift instead of relying on someone remembering `make refresh-scaffold`. Verified it fails against the pre-refresh generator.
- Validation: `python -m unittest tests.test_scaffold_sync tests.test_refresh_scaffold` — 49 OK; `python -m unittest discover tests/` — 10903 OK (skipped=4), up from 10902; `python -m ruff check tests/test_scaffold_sync.py` clean; `python -m mypy tests/test_scaffold_sync.py` clean; `python tools/refresh_scaffold.py --check` — all embedded copies in sync; `python tools/verify_state_delta.py --full --record-full-suite` — passed; checkpoint advanced to `3312fec`.
- `.github/workflows/**` unchanged. Updated `tests/test_scaffold_sync.py`, `CHANGELOG.md`, `scaffold.sh` (refreshed embedded copies), `.kilo/last_verified.checkpoint`, `.kilo/handover.md`, `PROJECT_STATUS.md`.

## State

- HEAD: `3312fec75b704870633879616e81dd1590c9197c`
- Verified checkpoint: `.kilo/last_verified.checkpoint` (head `3312fec`, full_suite_head `3312fec`)
- Working tree (pending auto-commit): `.kilo/last_verified.checkpoint`, `scaffold.sh`, `CHANGELOG.md`, `tests/test_scaffold_sync.py` (auto-committed by CI workflow per AGENTS.md; do not commit manually)

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py`; the clean-tree fast path does not apply until the pending auto-commit lands.
3. Deliver one concrete, verified improvement (choose on evidence):
   - `python tools/scan_untested.py --all`: add behavior coverage for an exported-but-untested callable (skip TypeVar/stdlib re-export/alias/constant noise).
   - Tooling parity: extend the new byte-identity pattern to the embedded `pyproject.toml` vs `pyproject.toml`, or another generated surface where `tests/test_scaffold_sync.py` still only checks containment.
   - Edge-case hardening or a doc/API mismatch found by inspection.
   Avoid timestamp-only or no-op changes.
4. Validation order that avoids the recurring drift: edit sources and documents first, then `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`. Add `python tools/scan_untested.py`, targeted tests, `make lint`, `make typecheck`, and `python -m unittest discover tests/` when `tests/` changed, finishing with `python tools/verify_state_delta.py --full --record-full-suite`.
5. Keep changes outside `.github/workflows/**`; update `CHANGELOG.md` (before refreshing), `.kilo/handover.md`, `PROJECT_STATUS.md`; post the next task via `board_post` to `main` (or record it in handover if posting to self is refused).