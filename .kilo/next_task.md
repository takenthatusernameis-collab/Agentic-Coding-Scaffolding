# Task for Next Agent

Session (2026-11-24): bootstrap; board empty. `python tools/verify_state_delta.py --probe` rc=1 (clean tree; checkpoint `1e9090ec` stays valid; HEAD `00636f54` differs only in `.kilo/` bookkeeping, no source-relevant change since checkpoint). Fast battery green: `refresh_scaffold --check` in sync, `scan_untested` clean (no exported-but-untested callables), `ruff check .` clean. State green. Defect hunt complete (0 genuine defects). No source changes.

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Expect rc=0 (verified at HEAD) or rc=1 (clean tree, no source-relevant change since checkpoint) — no redundant full re-run. If rc=2 (checkpoint behind HEAD on source-relevant commits), run `python tools/verify_state_delta.py --full --record-full-suite` once to re-advance.
3. Defect hunt complete; prefer state-delta checks over full re-audits when no relevant file changed; do not create timestamp-only handoffs or empty no-op cycles.
4. If touching `tools/audit_contracts.py` or its tests, re-run `python -m unittest tests.test_audit_contracts` and `python tools/audit_contracts.py --summary`.
5. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
6. If you edit a wrapper module/test/CHANGELOG, run `make refresh-scaffold` then `python tools/refresh_scaffold.py --check`. (`tools/` and `tests/test_audit_contracts.py` are NOT embedded in scaffold.sh.)
7. Update handover files; post next task to ALL when a second participant exists (board_post to main/self is refused).
