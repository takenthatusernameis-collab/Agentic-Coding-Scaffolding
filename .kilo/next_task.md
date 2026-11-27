# Task for Next Agent

Session (2026-11-27): leaked-exception audit swept `tomllib_utils`, `csv_utils`, `colorsys_utils`, and `imghdr_utils`. Documented stdlib-delegation leaks with `# audit-ignore:`:
- `tomllib_utils.read_toml` leaks `FileNotFoundError` (missing path) and `TOMLDecodeError` (invalid TOML); `tomllib_utils.load_toml_string` leaks `TOMLDecodeError`.
- `csv_utils.read_csv`/`read_csv_as_lists`/`write_csv`/`write_csv_from_lists`/`append_csv_row` leak `FileNotFoundError` when the path or its parent directory is missing (thin `open()` wrappers).
- `colorsys_utils` conversions leak `TypeError` on non-numeric input.
- `imghdr_utils.detect`/`matching_formats` leak `AttributeError` on a non-readable `file` (e.g. `None`).
Added failing-first `assertRaises` tests for each. `graphlib_utils` swept and found already clean (its `TypeError`/`CycleError` are raised by the wrapper itself). Full battery green at HEAD `3c3f6e43`; scaffold refreshed and in sync; CHANGELOG updated.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Finish the leaked-exception audit on the remaining re-export candidates `sndhdr_utils`, `sunau_utils`, `aifc_utils` (pure `what`/`whathdr`/`open` re-exports delegating to stdlib): probe edge inputs (None, missing files), document any genuine leaks in `Raises:` with `# audit-ignore:` (converting re-exports to thin `def` wrappers only where it stays minimal), or mark them clean if no doc gap exists. `sndhdr_utils.what`/`whathdr` leak `TypeError` on `None`; `sunau_utils.open`/`aifc_utils.open` leak `FileNotFoundError` on missing files.
4. Write failing-first tests for any documented leaks; keep `graphlib_utils`/`tomllib_utils`/`csv_utils`/`colorsys_utils`/`imghdr_utils` as done — do not re-run.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; `python tools/refresh_scaffold.py --check`.
6. Update handover files; no `.github/workflows/**` changes.
