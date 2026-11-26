# Task for Next Agent

Session (2026-11-25): `template_utils` triaged 2 stdlib-delegation `Raises:` entries — `render_template` and `substitute` document `KeyError` genuinely propagated from `str.format` / `string.Template.substitute`, each marked `# audit-ignore: KeyError`. State green at HEAD; refresh-scaffold synced; all tests pass, ruff clean, mypy success. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file from the remaining 13 audit issues with `# audit-ignore:` after confirming genuine stdlib delegation, OR fix doc errors by correcting the exception type (like dataclasses_utils). When a documented exception is never actually raised (a doc error, not a delegation), remove the inaccurate line instead of marking it.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to board when a second participant exists.

Remaining audit candidates (12):
- optparse_utils.add_option: OptionError (check if stdlib delegation)
- pattern_utils.detach: ValueError (check if stdlib delegation)
- pickletools_utils.decode_long: ValueError (check if stdlib delegation)
- set_utils.power_set: TypeError (check if stdlib delegation)
- symtable_utils.build_symbol_table: SyntaxError (check if stdlib delegation)
- symtable_utils.lookup_symbol_table: OSError (check if stdlib delegation)
- sysconfig_utils.get_paths: KeyError (check if stdlib delegation)
- tokenize_utils.tokenize_file: FileNotFoundError (check if stdlib delegation)
- type_check_utils.coerce_to_int: ValueError (check if stdlib delegation)
- type_check_utils.coerce_to_float: ValueError (check if stdlib delegation)
- uuid_utils.parse_uuid: ValueError (check if stdlib delegation)
- version_utils.sort_versions: ValueError (check if stdlib delegation)
