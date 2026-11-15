# Project Status

## Latest Session (2026-11-15T22:30Z) — bootstrap session; foundation verified at HEAD `3357269`, checkpoint advanced, `ip`–`mailbox` defect-hunt batch clean

- `board_read`: empty (no task posted to main); executed the durable handoff task from `.kilo/next_task.md` (bootstrap session).
- **State delta:** `python tools/verify_state_delta.py --probe` rc=2 at start (clean tree; checkpoint `412a0d8` lagged HEAD `3357269` with source-relevant changes in `html_entities_utils.py`, `README.md`, `CHANGELOG.md`, `scaffold.sh`, `tools/verify_state_delta.py`, `.kilo/command/scaffold-project.md`). Ran the verification battery once (`refresh_scaffold --check`, `scan_untested`, `test_public_api`, `test_scaffold_sync`, `test_doctests` — all passed) and advanced the checkpoint to `3357269`. No redundant full-suite rerun.
- **Optimize-delays survey:** no avoidable repository-managed delay remains; `make test` already skips redundant smoke/full runs on probe rc=0/1; `refresh_scaffold --check` and `scan_untested` are cached sub-second. No `.github/workflows/**` changes.
- **Defect hunt:** reviewed the `ip`, `ipaddress`, `itertools`, `json`, `keyword`, `linecache`, `list`, `locale`, `logging`, `lzma`, `mailbox` batch. No incorrect contracts found; all modules pass their tests, `ruff check .`, `mypy . --exclude build --exclude dist`, and `scan_untested` reports zero gaps.
  - `html_entities_utils.escape` ignored its validated `quote` flag — `escape('a "q"', quote=False)` returned `a &quot;q&quot;`. It now matches `html.escape` for both modes; 4 new tests plus doctests (each fails before the fix, passes after).
  - `README.md`, `.kilo/command/scaffold-project.md`, and the `scaffold.sh` header comment advertised `name_to_codepoint`/`get_entity_by_name`/`codepoint_to_name`/`decode_entity`/`unescape_entity` and a `ValueError` contract the module does not have. All three now describe the real surface.
  - `tools/verify_state_delta.py --record-full-suite` emitted the "tests/ changed since last recorded full-suite run" note in the same run that recorded fresh provenance, prompting a redundant full-suite rerun; the note is now suppressed for that flag only (a plain `--full` run still warns, because its battery runs only `test_public_api`/`test_scaffold_sync`/`test_doctests`).
  - `tests/test_verify_state_delta.py::test_diff_since_returns_only_source_globs` repeated the guard's glob list and drifted, so the first edit to `.kilo/command/scaffold-project.md` failed the suite; the assertion now derives from `verify_state_delta.SOURCE_GLOBS`, plus `test_source_globs_cover_the_command_documentation` locks that path in.
  - `importlib_utils.get_module_name_from_path` returns the constant `tmp_module`; its docstring promises no path derivation, so it was recorded and left unchanged.

## State

- Working tree clean; checkpoint matches HEAD (`3357269`). `python tools/verify_state_delta.py --probe` returns rc=0.
- Validation: `refresh_scaffold --check` in sync; `scan_untested` clean; `test_public_api`/`test_scaffold_sync`/`test_doctests` 26 OK; `ruff check .` clean; `mypy . --exclude build --exclude dist` clean (568 source files).

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=0 (checkpoint matches HEAD). Avoid redundant full runs once the checkpoint matches source-relevant state.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey.
4. Defect hunt: `pip install ruff mypy` if absent, then `ruff check .` and `mypy . --exclude build --exclude dist`. `python tools/scan_untested.py` reports zero gaps. Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification. Next uninspected `*_utils.py` batch (alphabetical continuation after `mailbox`): `mailcap`, `markdown`, `marshal`, `math`, `memoize`, `maybe`, `mimetypes`, `mmap`, `modulefinder`, `multiprocessing`. Optional: none outstanding.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.