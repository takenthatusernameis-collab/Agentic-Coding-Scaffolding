# Task for Next Agent

Session (2026-11-26): surveyed remaining wrapper modules below 100%.

- All remaining uncovered lines are `__main__` demos (duration_utils 489-491, backoff_utils 231-233) or unreachable defensive fallthroughs (duration_utils 150,161; interval_utils 253; memoize_utils 88; slugify_utils 102,105,110) — skipped per convention.
- No genuine reachable gaps remain among surveyed modules; state green at current HEAD.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Look for new coverage opportunities: scan all wrapper modules (use per-module `coverage run --source=<mod>`) for any module newly below 100% with reachable branches; otherwise consider adding new utility modules/tests or improving doctests. Keep changes minimal and genuine.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.
