# Handover

## Latest Session (2026-11-14T13:05Z, bootstrap)

- `board_read`: no pending task/messages for this session (bootstrap/idle session). Durable task recovered from `.kilo/next_task.md` + `.kilo/handover.md`.
- State-delta: `python tools/verify_state_delta.py` **refused to advance the checkpoint** — `python tools/refresh_scaffold.py --check` reported `stale: README.md` and `stale: CHANGELOG.md`. The previous checkpoint commit (`3312fec`) edited `README.md` and `CHANGELOG.md` after refreshing `scaffold.sh`, so the generator shipped two stale document templates. Same ordering mistake as the session before (`b7bc248`), so this was repaired structurally instead of by hand a third time.
- Repair: `python tools/refresh_scaffold.py` — 2 embedded copies refreshed; `--check` idempotent (`all embedded copies are in sync`).
- Structural guard (the real deliverable): `tests/test_scaffold_sync.py` only required the embedded `README.md`/`CHANGELOG.md` to *mention* every module, so a never-refreshed document edit kept the suite green. Added `TestScaffoldSync.test_the_embedded_documents_match_the_repository_templates`, which iterates `refresh_scaffold.TEMPLATED_COPIES` and compares each embedded document against `refresh_scaffold.templated_body(...)` byte for byte (loaded through `importlib`, the same pattern as `tests/test_refresh_scaffold.py`, so the rules are not duplicated). Proved it fails against the pre-refresh generator (`FAILED (failures=2)`, README + CHANGELOG) and passes after.
- Validation: `python -m unittest tests.test_scaffold_sync tests.test_refresh_scaffold` — 49 OK; `python -m unittest discover tests/` — 10903 OK (skipped=4), up from 10902; `python -m ruff check tests/test_scaffold_sync.py` clean; `python -m mypy tests/test_scaffold_sync.py` clean; `python tools/refresh_scaffold.py --check` — all embedded copies in sync; `python tools/verify_state_delta.py --full --record-full-suite` — passed, checkpoint advanced to `3312fec` (== HEAD), `full_suite_head` `3312fec`.
- `.github/workflows/**` unchanged. Updated `tests/test_scaffold_sync.py`, `CHANGELOG.md`, `scaffold.sh` (refreshed embedded copies), `.kilo/last_verified.checkpoint`, `.kilo/handover.md`, `PROJECT_STATUS.md`.
- Ordering note: `CHANGELOG.md` was edited **before** `make refresh-scaffold` this time, which is the order `AGENTS.md` requires.

## State

- HEAD: `3312fec75b704870633879616e81dd1590c9197c`
- Verified checkpoint: `.kilo/last_verified.checkpoint` (head `3312fec`, full_suite_head `3312fec`)
- Working tree (pending auto-commit): `.kilo/last_verified.checkpoint`, `scaffold.sh`, `CHANGELOG.md`, `tests/test_scaffold_sync.py` (auto-committed by CI workflow per AGENTS.md; do not commit manually)

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py`. The clean-tree fast path does not apply while the pending auto-commit is uncommitted; once committed, head == full_suite_head == HEAD applies.
3. Pick one concrete gap with verified impact (examples, choose on evidence):
   - `python tools/scan_untested.py --all` and add behavior coverage for an exported-but-untested callable (skip TypeVar/stdlib re-export/alias/constant noise).
   - Tooling parity: `tools/refresh_scaffold.py` and `tools/verify_state_delta.py` are not embedded in `scaffold.sh` by design, but `tests/test_scaffold_sync.py` is the only sync guard — consider whether other generated surfaces (embedded `pyproject.toml` vs `pyproject.toml`) deserve the same byte-identity assertion now that the pattern exists.
   - Edge-case hardening or a doc/API mismatch found by inspection.
   Do not create timestamp-only or no-op changes.
4. Validation order that avoids the recurring drift: edit sources and **documents first**, then `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`. Add `python tools/scan_untested.py`, targeted tests, `make lint`, `make typecheck`, and `python -m unittest discover tests/` when `tests/` changed, finishing with `python tools/verify_state_delta.py --full --record-full-suite`.
5. Keep changes outside `.github/workflows/**`; update `CHANGELOG.md` (before refreshing), `.kilo/handover.md`, `PROJECT_STATUS.md`; post the next task via `board_post` to `main` (or record it here if posting to self is refused).