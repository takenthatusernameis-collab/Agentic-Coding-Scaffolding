# Task for Next Agent

Session (2026-11-27): leaked-exception audit extended to `quopri_utils` and
`uu_utils`. Documented stdlib-delegation leaks with `# audit-ignore`:
`quopri_utils.encode/decode` leak `TypeError` on non-bytes input;
`quopri_utils.encode_file/decode_file` leak `AttributeError` on non-file
streams; `uu_utils.encode/decode` leak `AttributeError` on non-file streams.
Added failing-first `assertRaises` tests for each. `binascii_utils` confirmed
clean (validates via `_to_bytes`). Full battery green at HEAD `218d9aff`;
scaffold refreshed and in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue the leaked-exception / stdlib-delegation audit on remaining non-validating wrapper modules not yet swept (candidates without `# audit-ignore`: `quopri_utils` done, `uu_utils` done; next try `binascii_utils` done; consider `csv_utils`, `tomllib_utils`, `graphlib_utils`, `colorsys_utils`, `imghdr_utils`, `sndhdr_utils`, `sunau_utils`, `aifc_utils`). Probe with edge inputs (None, wrong types, malformed strings, boundary values), document leaks in `Raises:` with `# audit-ignore:`, write failing tests first; prefer state-delta checks.
4. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
5. Update handover files; no `.github/workflows/**` changes.