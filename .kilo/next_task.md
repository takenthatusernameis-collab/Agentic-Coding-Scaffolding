# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` (and `--record-full-suite` when appropriate) before making new edits.
3. Continue the correctness-defect hunt for silently ignored parameters and docstring-vs-implementation contract violations in remaining top-level non-`*_utils` modules (e.g. `strings.py`, `utils.py`) and remaining `*_utils.py` modules; run `tools/audit_contracts.py` and triage candidates.
4. When you find a genuine defect: write a failing test first, fix the source, run targeted tests plus `python -m ruff check`/`python -m mypy` on changed files when available, run `python tools/refresh_scaffold.py --check` if any embedded surface changed, and prepend a `CHANGELOG.md` Unreleased entry. Run the full verification battery at a coherent milestone.
5. If no genuine defect is found in this pass, record the completed audit scope in `.kilo/handover.md`/`PROJECT_STATUS.md` and hand the hunt to the next coherent defect class or module set.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`. Do not post duplicate/empty handoffs or commit no-op cycles.
