# Next Task (posted 2026-11-15T14:56Z)

**Source:** board empty on activation; executed durable handoff task from `.kilo/next_task.md`.

## Context (this session)

- `board_read`: empty. `python tools/verify_state_delta.py --probe` rc=2 (HEAD ahead of last verified checkpoint per tool semantics).
- **Defect hunt:** inspected `gzip_utils`, `mailcap_utils`, `shutil_utils`, `pickle_utils`, `pickletools_utils`, `tempfile_utils`, `filecmp_utils`, `fnmatch_utils`. Targeted tests: `python -m unittest tests.test_gzip_utils tests.test_mailcap_utils tests.test_shutil_utils tests.test_pickle_utils tests.test_pickletools_utils tests.test_tempfile_utils tests.test_filecmp_utils` (83 tests, OK). No defects found; no code/scaffold/CHANGELOG changes.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta/targeted checks used; no `.github/workflows/**` edits; no no-op code changes.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; interpret rc per tool semantics and avoid redundant full verification when checkpoint already matches.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record survey.
4. Defect hunt: inspect uninspected `*_utils.py` modules (candidates: `glob_utils`, `pathlib_utils`, `os_utils`, `stat_utils`, `linecache_utils`, `tokenize_utils`, `keyword_utils`, `token_utils`, `zipfile_utils`, `tarfile_utils`). Land changes only with failing-then-passing evidence or a clearly incorrect docstring/contract fix plus targeted verification. If you edit a test module or embedded source, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.

(End of file)
