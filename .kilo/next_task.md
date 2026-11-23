# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. The checkpoint was advanced to `08f717b7` by the full verification battery this session; HEAD may be one CI bookkeeping commit ahead (expect probe rc=1). If rc=1, state is already verified; no redundant battery run. Run `python tools/verify_state_delta.py --full --record-full-suite` only if the tree is dirty or the delta is non-empty.
3. Prior session summary — fixed `config_schema` docstring-vs-implementation defects: removed the nonexistent `:data:`schema_required`` reference, corrected the garbled `SchemaField` `Raises` clause (now documents the real `name` `ValueError`), and removed the false "later definitions win" claim from `ConfigSchema` (duplicate field names raise `ValueError`). Added `TestConfigSchemaConstruction.test_duplicate_field_names_raise`. Full battery green at HEAD `ac5c6780`.
4. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. Property-tested clean so far: `roman_utils`, `semver_utils`, `interval_utils`, `duration_utils`, `version_utils`, `stats`, `strings`, `color_utils`, `case_utils`, `slugify_utils`, `ring_buffer_utils`, `ttl_cache_utils`, `priority_queue_utils`, `maybe_utils`, `either_utils`, `data_utils`, `validation_utils`, `config_schema`, `retry_utils`. `tests/test_doctests.py` enforces every top-level doctest example.
5. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
6. Routine gates at coherent milestone.
7. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
8. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
9. Update handover files; post next task to main when a second participant exists.