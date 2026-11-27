# Task for Next Agent

Session (2026-11-27): email_utils audit complete — documented leaked stdlib exceptions
(AttributeError/IndexError/TypeError/ValueError) with `# audit-ignore` in
`email_parsedate`, `email_mktime_tz`, `email_formataddr`, `email_make_msgid`,
`email_quote`, `email_unquote`, `email_getaddresses`, `email_format_datetime`;
`email_formatdate` already complete. `urllib_utils` and `http_utils` confirmed
fully validated and clean. Full battery green at HEAD `e86d7229`; checkpoint
advanced.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. The email/urllib/http audit sweep is complete. Optionally extend the leaked-exception probe to other non-validating wrapper modules (modules that delegate to stdlib without input validation); document any leaks with `# audit-ignore` and write failing tests first.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.
