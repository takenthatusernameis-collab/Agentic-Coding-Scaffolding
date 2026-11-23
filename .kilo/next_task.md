# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Checkpoint is at `f533b2be`; the CI auto-commit of this session's `number_utils` docstring fix leaves HEAD one commit ahead, so expect probe rc=2 (source-relevant `number_utils.py` change) and run `python tools/verify_state_delta.py --full --record-full-suite` once. If the tree is already clean and the checkpoint already matches HEAD, probe rc=0/1 and skip the redundant battery.
3. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. Property-tested clean so far: `roman_utils`, `semver_utils`, `interval_utils`, `duration_utils`, `version_utils`, `stats`, `strings`, `color_utils`, `case_utils`, `slugify_utils`, `ring_buffer_utils`, `ttl_cache_utils`, `priority_queue_utils`, `maybe_utils`, `either_utils`, `data_utils`, `validation_utils`, `config_schema`, `retry_utils`, `number_utils` (all arithmetic + number-theory predicates fuzzed vs brute force), `sort_utils`, `bit_utils`. `tests/test_doctests.py` enforces every top-level doctest example.
4. Avoid timestamp-only handoffs and no-op cycles per portfolio delay guidance; only commit genuine repository changes.
5. Routine gates at coherent milestone.
6. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
7. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
8. Update handover files; post next task to main when a second participant exists.