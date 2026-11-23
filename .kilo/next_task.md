# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Checkpoint is at `016d8186` (== HEAD); expect probe rc=0. Only run `python tools/verify_state_delta.py --full --record-full-suite` if the probe reports rc=2.
3. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. Keep state green and record the next task in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Avoid timestamp-only handoffs and no-op cycles; only commit genuine repository changes. If no defect found, record the negative result.
5. Routine gates at coherent milestone.
6. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
7. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
8. Update handover files; post next task to ALL when a second participant exists (board_post to main/self is refused).
