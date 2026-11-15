# Next Task (posted 2026-11-15T14:51Z)

**Source:** board empty on activation; executed durable handoff task from `.kilo/next_task.md`.

## Context (this session)

- `board_read`: empty. Initial `verify_state_delta.py --probe` rc=2 (HEAD `f5afb3e` ahead of checkpoint) advanced checkpoint during verification pass.
- **Defect hunt:** inspected `roman_utils`, `duration_utils`, `collections_utils`, `tree_utils`, `compileall_utils`, `imaplib_utils`, `case_utils`, `csv_utils` against docstrings/doctests/contracts. `python -m doctest ...` clean; targeted unit tests passed (duration 46, collections 29, tree 25, compileall, imaplib 49, case 59, csv 5). No defects found; no code/scaffold/CHANGELOG changes.
- **Optimize-delays survey:** no remaining repository-managed AVOIDABLE_PROCESS_DELAY. State-delta guard used; no `.github/workflows/**` edits; no no-op code changes.

## Proposed Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; interpret rc per tool semantics and avoid redundant full verification when checkpoint already matches.
3. Optimize-delays pass: confirm no avoidable delay remains; record survey.
4. Defect hunt: inspect uninspected `*_utils.py` modules (candidates: `gzip_utils`, `mailcap_utils`, `pickle_utils`, `pickletools_utils`, `shutil_utils`, `tempfile_utils`, `filecmp_utils`, `fnmatch_utils`, `glob_utils`). Land changes only with failing-then-passing evidence or clearly incorrect doc/contract fix plus targeted verification. If you edit a test module, refresh `scaffold.sh` in the same session.
5. If embedded source/test/command files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`.
6. Keep `.github/workflows/**` unchanged; update `CHANGELOG.md` only for user-visible code/tooling changes (then refresh scaffold), update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`; post the next task to `main` via `board_post`.

## Constraints

- Do not modify `.github/workflows/**`.
- Never claim verification that was not run; preserve required gates and maintainer boundaries.
- Avoid duplicate board tasks and timestamp-only/no-op commits.

(End of file)