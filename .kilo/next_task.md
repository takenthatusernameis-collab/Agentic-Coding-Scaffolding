# Task for Next Agent

Session (2026-11-26): closed `ttl_cache_utils` coverage gap (91%→100%); state green at HEAD (after auto-commit).

- Added a deterministic `_SteppingCache` clock helper and 7 tests pinning: `_purge_expired` removal body, `__setitem__` update-existing-key path, expired branches of `__delitem__`/`pop`, `expire` default-to-configured-ttl and negative-ttl `ValueError`, and `ttl_cache` `maxsize` `TypeError`/`ValueError` guards. No source change; remaining gaps were all reachable defensive branches.
- `semver_utils` is now 100%; `slugify_utils` (96%) remaining lines are unreachable defensive while-loops — leave as-is; `backoff_utils` (97%) remaining gap is a `__main__` demo — skip.
- `priority_queue_utils` (90%, lines 164-170) is the next candidate. `rate_limiter_utils` (88%) gap is a `__main__` demo — skip.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps. Next candidate: `priority_queue_utils` (90%).
4. When a fallback/except branch is unreachable dead code, fix source to make reachable + tests; otherwise pin existing behavior. Keep changes minimal.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.