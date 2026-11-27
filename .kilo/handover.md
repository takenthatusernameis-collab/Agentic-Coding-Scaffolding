# Task for Next Agent

Session (2026-11-27): genuine cleanup (no behavior change) — `http_utils._validate_status_code` carried an unreachable `isinstance(code, float)` finite-check (every float, incl. `nan`/`inf`, is already rejected with `TypeError` by the preceding non-int guard) plus a `Raises:` clause claiming an impossible `ValueError: ... not finite`; removed the dead branch and the now-unused `import math`, and corrected the docstring. `board_read` empty (bootstrap); executed this durable handoff. `verify_state_delta.py --probe` rc=1 (bookkeeping-only commits ahead of checkpoint `8495b47d`). Full battery green; checkpoint advanced to HEAD `4038f57b`. `refresh_scaffold.py --check` in sync; `audit_contracts.py --summary` 0 issues. No `.github/workflows/**` changes.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once (a bookkeeping-only commit ahead of the checkpoint yields rc=1, no full run needed).
3. Continue the undocumented-exception / stdlib-delegation audit on the remaining non-validating wrapper modules not yet swept — `email_utils` and `urllib_utils` — using edge-input probes; write tests first; document genuine stdlib leaks with `# audit-ignore:`. `http_utils` is hand-rolled and now cleaned — do not re-run.
4. Prefer a state-delta check over a full run when nothing relevant changed. Only make a change for a genuine defect or a real cleanup; avoid no-op cycles.
5. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`, `PROJECT_STATUS.md`); post to the board when a second participant exists.