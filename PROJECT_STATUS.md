# Project Status

## Latest Session (2026-11-15T20:27Z) — landed `errno_utils` type/validation fixes, removed fabricated `lineterm` from `difflib_utils.ndiff`, defect hunt on `email`–`file` batch

- `board_read`: empty; executed durable handoff from `.kilo/next_task.md`.
- **State delta:** probe rc=2 at start (clean tree; source/tests changed since last checkpoint). Ran verification battery once; checkpoint advanced to `24659ad`.
- **Optimize-delays survey:** no avoidable repository-managed delay; state-delta probe + targeted checks only.
- **Defect hunt (2 fixes landed):** reviewed `email`, `encodings`, `ensurepip`, `enum`, `env`, `errno`, `exceptions`, `faulthandler`, `fcntl`, `file`.
  - Fixed `errno_utils.errorcode`/`strerror`/`is_errno`: added missing type hints, correct return types (`errorcode -> str | None`, `strerror -> str`), and input validation. Added 3 failing-then-passing tests.
  - Fixed `difflib_utils.ndiff`: dropped fabricated `lineterm` parameter (stdlib doesn't support it; wrapper silently ignored it). Added `test_ndiff_no_lineterm_parameter` (fails on old signature, passes on fixed).
  - No clearly incorrect contract in the other batch modules.
- **Scaffold:** `refresh_scaffold.py` run (difflib_utils, errno_utils, test_difflib_utils, CHANGELOG re-embedded); `--check` in sync. No `.github/workflows/**` changes.

## State

- Working tree at handoff: uncommitted `difflib_utils.py`, `errno_utils.py`, `tests/test_difflib_utils.py`, `CHANGELOG.md`, `scaffold.sh`, `.kilo/last_verified.checkpoint`, plus handover trio. Checkpoint recorded full-suite provenance at `24659ad`. CI auto-commits non-workflow changes.
- Validation: full `unittest discover tests/` OK; `test_scaffold_sync`/`test_public_api`/`test_doctests` OK; `scan_untested` clean; `refresh --check` in sync; `ruff`/`mypy` clean.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; interpret rc per tool (0/1/2). Source/tests changed this session, so after the CI commit expect rc=2 (run battery once), then avoid redundant full runs.
3. Optimize-delays pass: confirm no avoidable repository-managed delay; record survey.
4. Defect hunt: `pip install ruff mypy` if absent, then `ruff check .` and `mypy . --exclude build --exclude dist`. `scan_untested` zero gaps. Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix with targeted verification. Next batch (after `file`): `fnmatch`, `fractions`, `ftplib`, `functools`, `gc`, `genericpath`, `getopt`, `getpass`, `glob`, `graphlib`, `greeting`, `grp`, `gzip`. Optional: none outstanding.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.