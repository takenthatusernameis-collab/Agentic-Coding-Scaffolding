# Task for Next Agent

Session (2026-11-27): leaked-exception audit swept `sndhdr_utils`, `sunau_utils`, `aifc_utils`. Converted re-exports to thin wrappers documenting stdlib-delegation leaks with `# audit-ignore:`:
- `sndhdr_utils.what`/`whathdr` leak `TypeError` on `None`.
- `sunau_utils.open`/`aifc_utils.open` leak `FileNotFoundError` on missing files.
Full battery green; scaffold refreshed and in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. The leaked-exception audit on re-export candidates is complete; pivot to routine regression monitoring / state confirmation (prefer state-delta checks). Keep state green; no `.github/workflows/**` changes.
4. Update handover files.
