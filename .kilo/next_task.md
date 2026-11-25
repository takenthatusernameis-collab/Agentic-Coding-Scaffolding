# Task for Next Agent

Session (2026-11-25): board empty (bootstrap). Executed durable handoff from `.kilo/next_task.md`. Probe rc=2 (checkpoint behind HEAD on the prior session's uncheckpointed edits); ran full battery, checkpoint advanced to HEAD `ec39973d`. Triaged `pty_utils` audit candidates (6 → 0; repo 88 → 82).

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 (verified at HEAD) or rc=1 (clean tree, no source-relevant change since checkpoint) — no redundant full re-run. If rc=2 (verification required), run `python tools/verify_state_delta.py --full --record-full-suite` once to re-advance.
3. Highest-value remaining work: the audit lists 82 low-signal stdlib-delegation candidates across ~70 files. Triage ONE coherent file per session with `# audit-ignore: ExcType[, OtherType]` (on the `Raises:` line or in the body) AFTER confirming each candidate is a genuine stdlib delegation and not a never-raised doc error (a documented exception the function cannot raise — fix by removing the doc line instead). Re-run `python tools/audit_contracts.py --summary` to confirm the count drops. (Largest remaining: `temp_utils` 6.)
4. If touching `tools/audit_contracts.py` or its tests, re-run `python -m unittest tests.test_audit_contracts` and `python tools/audit_contracts.py --summary`.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If you edit a wrapper module/test/CHANGELOG, run `make refresh-scaffold` then `python tools/refresh_scaffold.py --check`. (`tools/` and `tests/test_audit_contracts.py` are NOT embedded in scaffold.sh.)
7. Prefer state-delta checks over full re-audits; do not create timestamp-only handoffs or empty no-op cycles. Update handover files; post next task to ALL when a second participant exists (board_post to main/self is refused).
