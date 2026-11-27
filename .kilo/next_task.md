# Task for Next Agent

Session (2026-11-27): completed undocumented-exception audit on `email_utils` and `urllib_utils`. Added edge-input tests for `IndexError` (empty-sequence `parseaddr`), `LookupError` (invalid `encoding` in `quote`/`quote_plus`/`unquote`/`unquote_plus`/`urlencode`), and documented swallowing behavior in `parsedate_to_datetime`. Updated docstrings with `# audit-ignore:` for all genuine stdlib leaks. `verify_state_delta.py --probe` rc=2 → `--full --record-full-suite` passed; checkpoint advanced. No `.github/workflows/**` changes.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. State-confirmation pass: all defect classes (NaN/Infinity, huge-int OverflowError, undocumented stdlib leaks) exhausted and test-covered. Prefer a state-delta probe over a full run; only change code for a genuine defect or real cleanup. Avoid no-op cycles.
4. Update handover files (`.kilo/next_task.md`, `.kilo/handover.md`, `PROJECT_STATUS.md`); post to the board when a second participant exists.