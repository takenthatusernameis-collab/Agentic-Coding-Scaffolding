# Task for Next Agent

## Next task (real, bounded, non-spinning)

Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
modules: `queue_utils`, `quopri_utils`, `random_utils`, `rate_limiter_utils`, and
`re_utils`.

1. Review each module for a real, demonstrable bug. Fix any bug found with a
   focused regression test; otherwise record the clean result.
2. Use `python tools/verify_state_delta.py --probe` to skip the redundant
   verification battery when the state is unchanged (exit 0/1 = skip, 2 = run).
   Run targeted tests only after a local change.
3. If you edit a wrapper module or its test, run `make refresh-scaffold` so the
   copies embedded in `scaffold.sh` stay byte-identical.
4. Do not manufacture commits or timestamp-only handoffs. A clean batch records
   the result and hands off the next batch; that is sufficient progress.

## This session (2026-11-28, HEAD 14573387)

Read-only bug hunt across `rlcompleter_utils`, `roman_utils`, `runpy_utils`,
`sched_utils`, and `secrets_utils`.

- `secrets_utils`: Fixed `choice` to validate that the input is a `Sequence`;
  previously accepted non-sequences (e.g., `int`, `dict`, `None`) and raised
  confusing `TypeError`/`KeyError` from the standard library instead of a clear
  validation error. Added focused regression test `test_rejects_non_sequence`.
- `rlcompleter_utils`, `roman_utils`, `runpy_utils`, `sched_utils`: No
  demonstrable bug found; existing tests pass (57 tests) and edge-case probes
  matched documented contracts.
- Ran `make refresh-scaffold` to sync embedded copies in `scaffold.sh`.
- State-delta probe returned "no source-relevant change since the last verified
  checkpoint" before the fix; targeted tests run after the fix.
- Lint and typecheck clean for modified files.

## Durable fix log (recent, most recent first)

These are the real code fixes made in earlier sessions; the per-session clean
bug-hunt logs were removed to keep this handover readable.

- `secrets_utils.choice`: validates `Sequence` input, rejects non-sequences.
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