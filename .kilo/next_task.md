# Task for Next Agent

Session (2026-11-26): bootstrap (board empty). Executed durable handoff from `.kilo/next_task.md` (routine regression monitoring). State was already green (`verify_state_delta.py --probe` rc=1). Rather than a no-op cycle, removed a genuine bottleneck: `dis_utils.findlinestarts` had an **unreachable** compatibility fallback (`dis.findlinestarts` is a generator, so the delegated call never raises inside the `try`; the `AttributeError` for non-code input surfaces during iteration, outside the `try`). Fixed by materializing the generator inside the `try`; `dis_utils` coverage 56% → 94%. Full suite green (12089 passed, 4 skipped); checkpoint advanced to HEAD `3b7a7180`. See handover.md / PROJECT_STATUS.md.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0/1; if rc=2 run `python tools/verify_state_delta.py --full --record-full-suite` once.
3. Continue closing genuine per-module coverage gaps on wrapper modules (the standing quality bottleneck). Use `python -m coverage run --source=<mod> -m pytest -q tests/test_<mod>.py` then `coverage report -m` to find reachable-but-untested defensive branches; prefer modules with no `sys.settrace` (avoid `trace_utils`/`pdb_utils`/`bdb_utils`, whose low numbers are a coverage-tracing artifact, not a real gap). `dis_utils` is now done — do not re-run it.
4. When a fallback/except branch is **unreachable dead code** (e.g. a delegated generator/iterator that defers its exception), fix the source so the fallback is reachable and add tests that exercise it; otherwise add tests that pin the existing behavior. Keep changes minimal and behavior-preserving on the happy path.
5. Run `make lint`, `make typecheck`, and the targeted tests when source-relevant files change; run the full suite (`pytest tests/ -q`) before recording the checkpoint.
6. If editing any wrapper module/test/CHANGELOG, run `make refresh-scaffold` (re-run after CHANGELOG edits) then `python tools/refresh_scaffold.py --check`.
7. Update handover files; post next task to board when a second participant exists. No `.github/workflows/**` changes.