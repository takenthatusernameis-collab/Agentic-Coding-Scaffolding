# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. If rc!=0, run `python tools/verify_state_delta.py --full` and advance the checkpoint before making new edits.
3. Continue the **broad-except swallowing / incorrect-fallback** correctness audit in `*_utils.py` on the remaining un-audited sites: `importlib_utils`, `email_utils`, `zipfile_utils`, `weakref_utils`, `marshal_utils`, `either_utils`, `maybe_utils`, `retry_utils`, `backoff_utils`, `sre_parse_utils`, `sre_constants_utils`, `uuid_utils` (and any others still carrying `except Exception`). Treat availability guards/import fallbacks in legacy-stdlib wrappers and intentional retry/wrapper behavior as likely intentional unless a documented contract is violated; fix only genuine contract violations (failing test first).
4. When you find a genuine defect: write a failing test first, fix the source, run targeted verification plus `python -m ruff check`/`python -m mypy` on changed files, run `python tools/refresh_scaffold.py --check` if any embedded surface changed, and prepend a `CHANGELOG.md` entry. Run the full verification battery at a coherent milestone.
5. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`. Do not post duplicate/empty handoffs or commit no-op cycles.

(End of file)
