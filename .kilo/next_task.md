# Task for Next Agent

Session (2026-11-25): board empty (bootstrap). Executed durable handoff. Probe rc=0 (checkpoint == HEAD `89f12d80`). Triaged `readline_utils` audit candidates (4 → 0; repo 68 → 64).

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file per session with `# audit-ignore:` after confirming genuine stdlib delegation. (64 remain across ~60 files; several files still have 3 candidates each — `ipaddress_utils`, `pkgutil_utils`, `posix_utils`, `ssl_utils`.)
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to ALL when a second participant exists.
