# Task for Next Agent

Session (2026-11-26): closed `slugify_utils` coverage gap (92%→96%); state green at HEAD (after auto-commit).

- Added 5 tests pinning `is_slug` invalid separator, `truncate_slug` invalid separator, search-limit clamp, trailing-separator stripping in prefix, and hard-cut trailing-separator stripping. 3 lines (102, 105, 110) remain uncovered — defensive while-loops that the current search_limit logic never reaches; left as-is per guidance.
- `ttl_cache_utils` (91%) remains the next candidate.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps. Next candidate: `ttl_cache_utils` (91%).
4. When a fallback/except branch is unreachable dead code, fix source to make reachable + tests; otherwise pin existing behavior. Keep changes minimal.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.
