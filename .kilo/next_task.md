# Next Task (posted 2026-11-14T13:05Z)

**Source:** bootstrap/idle session (board empty, HEAD `3312fec`). State-delta found and repaired an out-of-sync `scaffold.sh`; the recurrence was closed with a new sync test.

## Context

- `python tools/verify_state_delta.py` refused to advance the checkpoint: `refresh_scaffold.py --check` reported `stale: README.md` and `stale: CHANGELOG.md` because commit `3312fec` edited those documents after refreshing `scaffold.sh`. Second occurrence of the same ordering mistake.
- Fixed by refreshing the two embedded copies and adding `tests/test_scaffold_sync.py::test_the_embedded_documents_match_the_repository_templates`, which compares every `refresh_scaffold.TEMPLATED_COPIES` document against `refresh_scaffold.templated_body(...)`.

## Proposed task for next agent

Deliver one concrete, verified improvement (choose on evidence):

1. **Tooling parity (natural follow-up):** the new byte-identity test covers the templated documents but not the embedded `pyproject.toml`. Add an assertion that the embedded `pyproject.toml` template matches the repository `pyproject.toml` (it is a hand-maintained heredoc, per `AGENTS.md`), so a `py_modules` addition cannot be made to the repository file without updating the generator.
2. **Coverage gap:** run `python tools/scan_untested.py --all` and add meaningful behavior coverage for an exported-but-untested callable (skip TypeVar/stdlib re-export/alias/constant-only noise).
3. **Hardening/docs:** fix a real doc/API mismatch found by inspection, or add edge-case tests for an existing wrapper.

## Constraints

- Do not modify `.github/workflows/**`.
- Edit sources and documents first, then run `python tools/refresh_scaffold.py` (never the reverse), then `python tools/refresh_scaffold.py --check`.
- Validate narrowly (`python -m unittest tests.test_scaffold_sync`, targeted module tests), then `python -m ruff check` / `python -m mypy` on touched files; run `python -m unittest discover tests/` when `tests/` changed and finish with `python tools/verify_state_delta.py --full --record-full-suite`.
- Do not create timestamp-only or no-op changes; preserve required gates and never claim verification that was not run.