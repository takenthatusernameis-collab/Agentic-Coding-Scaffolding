# Task for Next Agent

Session (2026-11-26): dead-code / duplicate-definition audit complete. Top-level-definition AST scan of every wrapper module found zero within-module duplicate function/class definitions (ignoring `@overload` stubs) and removed five dead private helpers confirmed unused repo-wide: `concurrent_utils._add`, `concurrent_utils._inc`, `concurrent_utils._triple`, `pydoc_utils._check_optional_bool`, `sre_constants_utils._get`. `make lint` clean; `make typecheck` success (574 files); targeted tests 116 OK; `make refresh-scaffold` + `--check` in sync; full suite green; checkpoint advanced to `90b9aaa1`. See handover.md / PROJECT_STATUS.md.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full --record-full-suite` once.
3. Do NOT re-run the dead-code / duplicate-definition audit as a no-op cycle (it is complete for this cycle). Routine regression monitoring / state confirmation only; keep state green.
4. Run `make lint`, `make typecheck`, `make test` only when source-relevant files changed (targeted via `tools/select_tests.py`).
5. If editing any wrapper module/test/CHANGELOG, run `make refresh-scaffold` (re-run after CHANGELOG edits) then `python tools/refresh_scaffold.py --check`.
6. Update handover files; post next task to board when a second participant exists. No `.github/workflows/**` changes.
