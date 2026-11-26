# Task for Next Agent

Session (2026-11-26): closed `circuit_breaker_utils` coverage gap (96% → 100%); state green at HEAD `9435d7c5` (after auto-commit).

- Added `test_expected_exception_tuple_counts_multiple` (valid non-empty-tuple `expected_exception`, line 86), `test_failure_threshold_property` (line 117), `test_recovery_timeout_property` (line 122), and `test_can_execute_false_during_half_open_trial` (line 156). Coverage 96% → 100%; no source change.
- `refresh-scaffold` + `--check` in sync; full suite green; checkpoint advanced with `--full --record-full-suite`.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps. Survey logic modules for reachable edge branches (candidates: `cooldown_utils` 97%, `duration_utils` 97%, `interval_utils` 98%, `validation_utils` 97%, `memoize_utils` 98%). Skip `__main__` demos and unreachable defensive fallthroughs.
4. When a fallback/except branch is unreachable dead code, fix source to make reachable + tests; otherwise pin existing behavior. Keep changes minimal.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.
