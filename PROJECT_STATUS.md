# Task for Next Agent

## Next task (real, bounded, non-spinning)

Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
modules: `rlcompleter_utils`, `roman_utils`, `runpy_utils`, `sched_utils`, and
`secrets_utils`.

1. Review each module for a real, demonstrable bug. Fix any bug found with a
   focused regression test; otherwise record the clean result.
2. Use `python tools/verify_state_delta.py --probe` to skip the redundant
   verification battery when the state is unchanged (exit 0/1 = skip, 2 = run).
   Run targeted tests only after a local change.
3. If you edit a wrapper module or its test, run `make refresh-scaffold` so the
   copies embedded in `scaffold.sh` stay byte-identical.
4. Do not manufacture commits or timestamp-only handoffs. A clean batch records
   the result and hands off the next batch; that is sufficient progress.

## This session (2026-11-28, HEAD de8c1ace)

Read-only bug hunt across `readline_utils`, `regex_utils`, `reprlib_utils`,
`resource_utils`, `retry_utils`.

- All five modules reviewed; **no demonstrable bug found**. The existing 151
  targeted tests pass, and an edge-case probe (readline 1-based<->0-based
  position conversion for remove/replace plus out-of-range handling and
  `make_completer`; `reprlib.Repr` maxlevel validation for `-1`/`True`/`3.5`/
  `None`/`0`; `resource` limit name/value round-trip and `usage_as_dict`;
  `regex` findall/named_groups; `retry` max_attempts validation) all matched the
  documented contracts.
- State-delta probe returned "no source-relevant change since the last verified
  checkpoint", so the redundant battery was skipped.
- No wrapper module or test was edited, so `make refresh-scaffold` was not
  required; no source changes to commit from this session.

## Durable fix log (recent, most recent first)

These are the real code fixes made in earlier sessions; the per-session clean
bug-hunt logs were removed to keep this handover readable.

- `numbers_utils.is_perfect_power`: exact integer nth root; no longer raises
  `OverflowError` on large perfect powers (`10**400`, `2**2000`).
- `mmap_utils.create_file_mmap`: closed the file-descriptor leak.
- `pickle_utils.is_valid_protocol`: rejects non-int protocols (e.g. `2.0`) so it
  agrees with `validate_protocol`.
- `locale_utils.is_valid_locale`: rejects >2-part and empty-part locales.
- `logging_utils.get_logger`: validates `name` is `str` or `None` consistently.
- `lzma_utils`: preset range validation (0-9) for compress/write/open.
- `dict_utils.unflatten_dict`: handles scalar/nested key collision.

## Workflow reminders

- Do NOT modify `.github/workflows/**` (maintainer-managed).
- `make test` / `make lint` / `make typecheck` are the developer commands.
- The CI checkpoint only counts changes outside `.github/workflows/`.