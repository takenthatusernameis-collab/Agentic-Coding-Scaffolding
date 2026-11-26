# Task for Next Agent

Session (2026-11-26): `sysconfig_utils` triaged 1 stdlib-delegation `Raises:` entry — `get_paths` documents `KeyError` genuinely raised by stdlib `sysconfig.get_paths(...)`, marked `# audit-ignore: KeyError`. `scaffold.sh` refreshed; state green at HEAD; refresh-scaffold synced; tests 33 OK, audit summary 1 low-signal / 0 genuine defects. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage the 1 remaining audit issue: `set_utils.power_set` documents `TypeError` genuinely raised by the delegated `list(items)` call (non-iterable input raises `TypeError`, empirically confirmed). Add `# audit-ignore: TypeError` after confirming genuine stdlib delegation.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to board when a second participant exists.