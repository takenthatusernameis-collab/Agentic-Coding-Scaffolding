# Task for Next Agent

## Next task (real, bounded, non-spinning)

Continue the read-only bug hunt on the NEXT batch of unreviewed hand-written
modules: `sre_compile_utils`, `sre_constants_utils`, `sre_parse_utils`,
`ssl_utils`, and `stat_utils`.

1. Review each module for a real, demonstrable bug. Fix any bug found with a
   focused regression test; otherwise record the clean result.
2. Use `python tools/verify_state_delta.py --probe` to skip the redundant
   verification battery when the state is unchanged (exit 0/1 = skip, 2 = run).
   Run targeted tests only after a local change.
3. If you edit a wrapper module or its test, run `make refresh-scaffold` so the
   copies embedded in `scaffold.sh` stay byte-identical.
4. Do not manufacture commits or timestamp-only handoffs. A clean batch records
   the result and hands off the next batch; that is sufficient progress.

## This session (2026-11-28)

Read-only bug hunt across `socket_utils`, `socketserver_utils`, `sort_utils`,
`spwd_utils`, and `sqlite3_utils`.

- `socket_utils`: **fixed a finite-but-huge timeout leak.** `connect_socket`,
  `create_connection`, and `set_timeout` accepted a finite `timeout` too large
  for the platform C `time_t` (e.g. `1e300`); `_require_timeout` only checked
  finiteness/sign, so the value reached `settimeout`/`socket.create_connection`
  and raised an opaque `OverflowError: timestamp out of range for platform
  time_t`. `create_connection` additionally leaked the socket it had already
  created. Added `_timeout_in_platform_range`, which probes a throwaway socket's
  `settimeout` and is consulted by `_require_timeout`, so all three helpers now
  raise a clear `ValueError` before any socket is created. Updated the three
  `Raises:` docstrings; added `test_set_timeout_rejects_too_large_finite_value`,
  `test_connect_socket_rejects_too_large_finite_timeout`, and
  `test_create_connection_rejects_too_large_finite_timeout`.
- `socketserver_utils`, `sort_utils`, `spwd_utils`, `sqlite3_utils`: No
  demonstrable bug found; existing tests pass.
- Ran `make refresh-scaffold` to sync the embedded copies of `socket_utils.py`
  and its test. Full battery: 143 batch tests OK, `verify_state_delta --full`
  passed, audit 0 issues.

## Previous session (2026-11-28)

Read-only bug hunt across `signal_utils`, `site_utils`, `slugify_utils`,
`smtplib_utils`, and `sndhdr_utils`.

- `signal_utils`, `site_utils`, `slugify_utils`, `smtplib_utils`,
  `sndhdr_utils`: No demonstrable bug found; existing tests pass (185 tests).
- Ran targeted test suite; all passing.

"""


Read-only bug hunt across `semver_utils`, `seq_utils`, `set_utils`,
`shelve_utils`, and `shlex_utils`.

- `semver_utils`, `seq_utils`, `set_utils`, `shelve_utils`, `shlex_utils`: No
  demonstrable bug found; existing tests pass (458 tests).
- Ran targeted test suite; all passing.

## This session (2026-11-28, HEAD f40a766a)

Read-only bug hunt across `rlcompleter_utils`, `runpy_utils`, `sched_utils`,
`select_utils`, and `selectors_utils`.

- `select_utils`: `_require_optional_number` probed platform overflow by calling
  `_select.select([], [], [], timeout)`, which blocked for the full timeout
  duration (e.g. 5 seconds for timeout=5.0) on every validation. Removed the
  blocking probe and convert `OverflowError` to `ValueError` at the actual call
  sites in `select` and `poll_poll`, preserving the documented contract without
  the delay. Existing tests pass.
- `rlcompleter_utils`, `runpy_utils`, `sched_utils`, `selectors_utils`: No
  demonstrable bug found; existing tests pass.
- Ran `make refresh-scaffold` to sync the embedded copy of `select_utils.py`.

## This session (2026-11-28, HEAD f40a766a)

Read-only bug hunt across `readline_utils`, `regex_utils`, `reprlib_utils`,
`resource_utils`, and `retry_utils`.

- `retry_utils`: a *finite* `delay` too large for the platform's `time_t`
  (e.g. `1e300`, or a modest delay amplified by a huge `backoff`) reached
  `time.sleep` and raised an opaque `OverflowError: timestamp out of range for
  platform time_t` -- the exact low-level C-layer failure the finite-delay
  validation exists to prevent. Added a `_sleep` helper that converts that
  `OverflowError` into a clear `ValueError` naming the offending delay, and
  routed all three decorators (`retry`, `retry_with_backoff`, `retry_count`)
  through it. Added `TestRetrySleepRange` with four focused regression tests.
- `readline_utils`, `regex_utils`, `reprlib_utils`, `resource_utils`: No
  demonstrable bug found; existing tests pass and edge-case probes (capturing
  groups, optional groups, `indent`/`maxlevel` validation, `prlimit` read,
  `set_rlimit` soft>hard, huge-but-finite delays) matched documented contracts.
- Ran `make refresh-scaffold` to sync the embedded copies in `scaffold.sh`.
- Lint clean; typecheck clean for the changed files (the only 4 errors are
  pre-existing `pytest` import-not-found in unrelated test files). Full suite:
  12089 tests, only the 3 pre-existing `pytest`-unavailable import errors.

## Durable fix log (recent, most recent first)

These are the real code fixes made in earlier sessions; the per-session clean
bug-hunt logs were removed to keep this handover readable.

- `select_utils`: removed blocking overflow probe in `_require_optional_number`; OverflowError converted at call sites.
- `retry_utils`: `_sleep` helper turns a too-large-but-finite delay's
  `time.sleep` `OverflowError` into a clear `ValueError` (all 3 decorators).
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