# Task for Next Agent

## Next task (real, bounded, non-spinning)

Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
modules: `readline_utils`, `regex_utils`, `reprlib_utils`, `resource_utils`, and
`retry_utils`.

1. Review each module for a real, demonstrable bug. Fix any bug found with a
   focused regression test; otherwise record the clean result.
2. Use `python tools/verify_state_delta.py --probe` to skip the redundant
   verification battery when the state is unchanged (exit 0/1 = skip, 2 = run).
   Run targeted tests only after a local change.
3. If you edit a wrapper module or its test, run `make refresh-scaffold` so the
   copies embedded in `scaffold.sh` stay byte-identical.
4. Do not manufacture commits or timestamp-only handoffs. A clean batch records
   the result and hands off the next batch; that is sufficient progress.

## This session (2026-11-28, HEAD add4bd49)

Read-only bug hunt across `queue_utils`, `quopri_utils`, `random_utils`,
`rate_limiter_utils`, and `re_utils`.

- `random_utils.random_gaussian`: `mu` accepted non-finite values (NaN, ±inf)
  and non-numeric types (str, None, bool), silently returning NaN/±inf or
  raising unclear stdlib `TypeError` from `gauss`. Added validation that `mu`
  and `sigma` are numbers (not bool) and finite, matching the existing `sigma`
  validation and the `random_uniform`/`random_bool` convention. Added focused
  regression tests `test_non_finite_mu_raises`, `test_non_numeric_mu_raises`,
  and `test_bool_sigma_raises`.
- `queue_utils`, `quopri_utils`, `rate_limiter_utils`, `re_utils`: No
  demonstrable bug found; existing tests pass (136 tests, quopri tests skipped
  without pytest) and edge-case probes matched documented contracts.
- Ran `make refresh-scaffold` to sync embedded copies in `scaffold.sh`.
- Lint and typecheck clean for modified files; doctests pass.

## Durable fix log (recent, most recent first)

These are the real code fixes made in earlier sessions; the per-session clean
bug-hunt logs were removed to keep this handover readable.

- `secrets_utils.choice`: validates `Sequence` input, rejects non-sequences.
- `random_utils.random_gaussian`: validates `mu` is a finite number (not bool,
  not NaN/±inf), matching existing `sigma` validation.
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