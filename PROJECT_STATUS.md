# Project Status

## Latest Session (2026-11-16T12:02Z) — repaired stale `scaffold.sh` embedded copies (CI was red) and made `scan_untested --all` tests coverage-independent

- `board_read`: empty (no task posted to main); executed the durable handoff task from `.kilo/next_task.md`.
- **State:** `python tools/verify_state_delta.py --probe` returned rc=2 at session start (HEAD `62d6837` ahead of checkpoint `4361997`); the intervening commits carried the previous session's committed work, and the checkpoint was advanced to `62d6837` with full-suite provenance at the end of this session.
- **Root cause — the committed `scaffold.sh` had drifted out of sync: 28 embedded copies (27 `tests/test_*.py` + `CHANGELOG.md`) were stale, so the full suite failed 32 tests.** The previous session committed test and `CHANGELOG.md` edits without re-embedding them; the verification battery's `refresh_scaffold.py --check` is exactly that check, so the drift persisted until now. `python tools/refresh_scaffold.py` regenerated the embedded copies; `--check` reports all in sync.
- **Test fix — `tests/test_scan_untested.py`:** five `--all`/`--json`/`--summary`/cache cases hard-coded a now-false assumption that `scan_untested --all` still finds gaps (non-zero exit, positive total, `help` gap). Now that `--all` is clean, they were rewritten to build a throwaway fixture project (a function, a constant, and a class export its test never references) and run a copied scanner against it, verifying the default-vs-`--all` distinction independent of the repository's coverage state.
- **Validation (targeted):** `python -m unittest tests.test_scan_untested tests.test_scaffold_sync tests.test_refresh_scaffold` — 102 OK.
- **Full suite:** `python -m unittest discover tests/` — 11238 OK (skipped=4).
- **Gates:** `python -m ruff check .` — clean; `python -m mypy . --exclude build --exclude dist` — clean (568 files); `python tools/refresh_scaffold.py --check` — in sync; `python tools/scan_untested.py --all` — clean (zero gaps).
- **State:** uncommitted source changes pending CI auto-commit (`scaffold.sh`, `tests/test_scan_untested.py`, `CHANGELOG.md`, handover/status/next_task, `.kilo/last_verified.checkpoint`). No `.github/workflows/**` changes.

## Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; expect rc=2 at session start (HEAD ahead of checkpoint because this session's changes are uncommitted until CI auto-commits) or rc=0/1 once committed. Run `--full --record-full-suite` once to advance the checkpoint only when the probe reports a source-relevant change.
3. Optimize-delays pass: confirm no avoidable repository-managed delay remains; record the survey. Do not manufacture timestamp-only handovers or empty commits.
4. **Next focus: correctness defect hunt (failing-test-first) on the numeric/algorithm-heavy `*_utils.py` modules** most likely to hide subtle contract bugs (cf. `numbers_utils`, `version_utils`, `zipapp_utils`). Concrete starting batch: `bit_utils`, `cmath_utils`, `decimal_utils`, `fractions_utils`, `math_utils`, `prime_utils`, `random_utils`, `statistics_utils`, `stats`. `scan_untested --all` is already clean, so the deliverable is correctness, not coverage.
5. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry for user-visible fixes and refresh again.
6. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.