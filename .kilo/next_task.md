# Task for Next Agent

Session (2026-11-25): `imaplib_utils.format_internaldate` triaged — `ValueError` is genuinely propagated from `imaplib.Time2Internaldate` for a naive :class:`datetime.datetime`, marked `# audit-ignore: ValueError` on the `Raises:` line. `tabnanny_utils` previously triaged `process_tokens` (`# audit-ignore: NannyNag`) and removed an inaccurate `check` `NannyNag` doc line. State green at HEAD `b9eeb1d7`; refresh-scaffold synced; all tests pass, ruff clean, mypy success. No `.github/workflows/**` changes.

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file from the remaining 15 audit issues with `# audit-ignore:` after confirming genuine stdlib delegation, OR fix doc errors by correcting the exception type (like dataclasses_utils). When a documented exception is never actually raised (a doc error, not a delegation), remove the inaccurate line instead of marking it.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to board when a second participant exists.

Remaining audit candidates (15):
- multiprocessing_utils.get_context: ValueError (check if stdlib delegation)
- optparse_utils.add_option: OptionError (check if stdlib delegation)
- pattern_utils.detach: ValueError (check if stdlib delegation)
- pickletools_utils.decode_long: ValueError (check if stdlib delegation)
- set_utils.power_set: TypeError (check if stdlib delegation)
- symtable_utils.build_symbol_table: SyntaxError (check if stdlib delegation)
- symtable_utils.lookup_symbol_table: OSError (check if stdlib delegation)
- sysconfig_utils.get_paths: KeyError (check if stdlib delegation)
- template_utils.render_template: KeyError (check if stdlib delegation)
- template_utils.substitute: KeyError (check if stdlib delegation)
- tokenize_utils.tokenize_file: FileNotFoundError (check if stdlib delegation)
- type_check_utils.coerce_to_int: ValueError (check if stdlib delegation)
- type_check_utils.coerce_to_float: ValueError (check if stdlib delegation)
- uuid_utils.parse_uuid: ValueError (check if stdlib delegation)
- version_utils.sort_versions: ValueError (check if stdlib delegation)
