# Task for Next Agent

Session (2026-11-26): `type_check_utils` triaged 2 stdlib-delegation `Raises:` entries — `coerce_to_int` and `coerce_to_float` document `ValueError` genuinely propagated from `int()`/`float()` calls, each marked `# audit-ignore: ValueError`. State green at HEAD (after refresh); refresh-scaffold synced; tests 85 OK, ruff clean, mypy success, audit summary 7/0. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file from the remaining 7 audit issues with `# audit-ignore:` after confirming genuine stdlib delegation. Remaining: optparse_utils, pattern_utils, pickletools_utils, set_utils, sysconfig_utils, tokenize_utils, version_utils.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to board when a second participant exists.
