# Task for Next Agent

Session (2026-11-25): board empty (bootstrap). Executed durable handoff. Probe rc=2 (source changed since checkpoint `04290448`); ran full battery once, checkpoint advanced to HEAD `47956fcd`. Triaged `heapq_utils` audit candidates (2 → 0; repo 44 → 42): 2 genuine delegations marked `# audit-ignore: IndexError` (`heappop`/`heapreplace` document `IndexError` from delegated `heapq.heappop`/`heapq.heapreplace` on empty heap, empirically confirmed).

1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 or rc=1; if rc=2 run full once.
3. Triage ONE coherent file per session with `# audit-ignore:` after confirming genuine stdlib delegation. (42 remain across ~41 files; largest: `async_utils`/`base64_utils`/`collections_abc_utils`/`config_utils`/`configparser_utils`/`dataclasses_utils`/`datetime_utils`/`deque_utils`/`doctest_utils`/`imaplib_utils`/`ini_utils`/`mmap_utils`/`multiprocessing_utils`/`optparse_utils`/`path_utils`/`pattern_utils`/`pickletools_utils`/`pyclbr_utils`/`resource_utils`/`selectors_utils`/`set_utils`/`symtable_utils`/`sysconfig_utils`/`tabnanny_utils`/`template_utils`/`termios_utils`/`tokenize_utils`/`type_check_utils`/`uuid_utils`/`version_utils`/`wsgiref_utils` each have 1–2.) When a documented exception is never actually raised (a doc error, not a delegation), remove the inaccurate line instead of marking it.
4. If touching audit tool/tests, re-run `tests.test_audit_contracts` and summary.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If editing wrapper module/test/CHANGELOG, run `make refresh-scaffold` then check.
7. Prefer state-delta checks; no timestamp-only handoffs/no-op cycles. Update handover files; post next task to ALL when a second participant exists.