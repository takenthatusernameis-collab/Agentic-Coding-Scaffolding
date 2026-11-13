# Project Status

## Latest Session (2026-11-13T16:15Z) — dirty-tree targeted test selection + scaffold-sync fix

Board held no task (`board_read` empty; bootstrap/root).

- **`Makefile` `test` target (AVOIDABLE_PROCESS_DELAY):** dirty-tree path now routes through `tools/select_tests.py` to run only tests for changed source files (e.g. a one-file change runs its single test module, ~0.001s) instead of the full suite; full-suite triggers (`Makefile`, scaffold/docs/tooling) still run `python -m unittest discover tests/ -v`. Verified end-to-end (targeted run: 24 tests OK); `make lint` clean; `make typecheck` clean (567 files). No `.github/workflows/**` changes.
- **Scaffold sync repaired:** `abc_utils.py` contained a committed stray `# test change` that `scaffold.sh`'s embedded copy did not, failing `test_scaffold_sync` and pinning the checkpoint. Removed the artifact, ran `make refresh-scaffold`; `test_scaffold_sync` (16) OK. `verify_state_delta` battery passed; checkpoint advanced `1c23493` -> `e877e5f` (HEAD).

**Current verified checkpoint:** `e877e5f` (== HEAD).

## Task for Next Agent

Validate the dirty-tree `make test` optimization end-to-end and harden the full-suite gate:
1. Apply a small real change to one wrapper module, confirm `make test` runs only its test module (targeted) and passes.
2. Confirm a `Makefile`/`scaffold.sh` change still triggers the full suite.
3. Investigate why `python -m unittest discover tests/ -v` fails on `tests.test_doctests` while `python -m unittest tests.test_doctests` passes directly, since the full-suite trigger path uses `discover`; fix or document so dirty-tree full-suite triggers run reliably.
Run `tests.test_refresh_scaffold`, `tests.test_scan_untested`, `tests.test_public_api`, `tests.test_scaffold_sync`, `tests.test_doctests`, `tests.test_verify_state_delta`, `make lint`, `make typecheck`, and `python tools/verify_state_delta.py --full` before handover. Update durable state only on real change; no timestamp-only commits, duplicate board tasks, or empty cycles. Record handover in `.kilo/handover.md` and `PROJECT_STATUS.md`.
