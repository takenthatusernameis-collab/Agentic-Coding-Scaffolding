# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 at session start (dirty tree) then rc=0/1 once CI commits. Run `verify_state_delta.py --full --record-full-suite` once to advance the checkpoint.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey.
4. Defect hunt: `python -m ruff check .` and `python -m mypy . --exclude build --exclude dist` if source changed or confidence needed. `python tools/scan_untested.py` reports zero gaps. Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification. Next uninspected `*_utils.py` batch (alphabetical continuation after `webbrowser`): `wsgiref`, `xdrlib`, `xml`, `xmlrpc`, `zipapp`, `zipfile`, `zipimport`, `zlib`, `zoneinfo`.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.