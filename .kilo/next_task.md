# Task for Next Agent

Session (2026-11-26): `version_utils` triaged 1 stdlib-delegation `Raises:` entry — `sort_versions` documents `ValueError` genuinely propagated from `parse_version`, marked `# audit-ignore: ValueError`. State green at HEAD (after refresh); refresh-scaffold synced; tests 302 OK, ruff clean, mypy success, audit summary 6/0. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file from the remaining 6 audit issues with `# audit-ignore:` after confirming genuine stdlib delegation. Remaining: optparse_utils, pattern_utils, pickletools_utils, set_utils, sysconfig_utils, tokenize_utils.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to board when a second participant exists.

(End of file - total 11 lines)
