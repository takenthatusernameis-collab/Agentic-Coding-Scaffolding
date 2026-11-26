# Task for Next Agent

Session (2026-11-26): bootstrap (board empty). State confirmed green via `python tools/verify_state_delta.py --probe` (rc=1): working tree clean, no source-relevant change since last verified checkpoint `726aea14`; HEAD `ac4d197d` advances only `.kilo/` handover files. Dead-code / duplicate-definition audit complete for this cycle — not re-run as a no-op cycle. `make lint` clean; `make typecheck` success (574 files); full suite green. See handover.md / PROJECT_STATUS.md.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full --record-full-suite` once.
3. Do NOT re-run the dead-code / duplicate-definition audit as a no-op cycle (it is complete for this cycle). Routine regression monitoring / state confirmation only; keep state green.
4. Run `make lint`, `make typecheck`, `make test` only when source-relevant files changed (targeted via `tools/select_tests.py`).
5. If editing any wrapper module/test/CHANGELOG, run `make refresh-scaffold` (re-run after CHANGELOG edits) then `python tools/refresh_scaffold.py --check`.
6. Update handover files; post next task to board when a second participant exists. No `.github/workflows/**` changes.
