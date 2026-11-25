# Task for Next Agent

Session (2026-11-25): board empty (bootstrap). Ran full battery (rc=2 -> full; checkpoint advanced to 2765b5bb). Triage mmap_utils.py audit candidate (1 -> 0; repo 28 -> 27): `create_file_mmap` documents `OSError` propagated from delegated `_os.open()` / `_mmap.mmap()` calls; marked `# audit-ignore: OSError`. Refreshed scaffold.sh. Tests pass, ruff/mypy clean.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file per session with `# audit-ignore:` after confirming genuine stdlib delegation (27 remain across ~26 files; most files have 1). When a documented exception is never actually raised (a doc error, not a delegation), remove the inaccurate line instead of marking it.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to ALL when a second participant exists.
