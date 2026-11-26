# Task for Next Agent

Session (2026-11-26): closed reachable per-module coverage gaps.

- `validation_utils` 97% -> 100%: added `test_min_length_non_collection_returns_false`, `test_max_length_non_collection_returns_false`, `test_hostname_too_long_without_trailing_dot` (lines 155, 175, 233).
- `interval_utils` 98% -> 99% reachable: added `test_touching_intervals_both_sides_extend` (lines 390, 392); line 253 is an unreachable defensive fallthrough, skipped per convention.
- `duration_utils` 97%: lines 150/161 are unreachable defensive fallthroughs; 489-491 is the `__main__` demo — all skipped per convention.
- `memoize_utils` 98%: line 88 is an unreachable defensive raise — skipped per convention.
- `refresh-scaffold` + `--check` in sync (tests/test_interval_utils.py, tests/test_validation_utils.py refreshed in scaffold.sh); ruff/mypy clean; 258 tests across four modules green; scaffold_sync/public_api/doctests green.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps. Survey remaining logic modules below 100% (use `make coverage` or per-module `coverage run --source=<mod> -m pytest tests/test_<mod>`). Skip `__main__` demos and unreachable defensive fallthroughs.
4. For reachable edge branches add tests pinning existing behavior; for unreachable dead code either fix source to make reachable + tests or skip. Keep changes minimal.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.
