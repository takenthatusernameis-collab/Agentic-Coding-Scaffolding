# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`. Checkpoint is at `a5694fbe` (HEAD `a5694fbe`); expect probe rc=0. Only run `python tools/verify_state_delta.py --full --record-full-suite` if the probe reports rc=2 (source/tests changed).
3. Defect hunt: continue targeted review of hand-rolled modules not yet reviewed. Prefer a genuine logic defect; write the failing test first. Keep state green and record the next task in `.kilo/next_task.md` and `.kilo/handover.md`.
4. Avoid timestamp-only handoffs and no-op cycles; only commit genuine repository changes. If no defect found, record the negative result (as prior sessions have).
5. Routine gates at coherent milestone.
6. Test modules under `tests/`; no root-level test files. Keep `.github/workflows/**` unchanged.
7. If you edit utils/test/CHANGELOG, run `make refresh-scaffold` then check.
8. Update handover files; post next task to ALL when a second participant exists (board_post to main/self is refused).

## Modules already reviewed (do not re-review unless re-touching)

NaN/Infinity + bool-rejection sweep: `math_utils`, `subprocess_utils`, `sqlite3_utils`,
`telnetlib_utils`, `cprofile_utils`, `threading_utils`, `select_utils`, `duration_utils`,
`interval_utils`, `fractions_utils`, `calculator`, `stats`, `prime_utils`, `resource_utils`,
`trace_utils`, `numbers_utils`, `posix_utils`. Logic/contract review: `retry_utils`,
`priority_queue_utils`, `shapes`, `env_utils`, `email_utils`, `nntplib_utils`, `optparse_utils`,
`imaplib_utils`, `roman_utils`, `slugify_utils`, `semver_utils`, `ring_buffer_utils`,
`ttl_cache_utils`, `bit_utils`, `version_utils`, `graphlib_utils`, `maybe_utils`,
`either_utils`, `validation_utils`, `memoize_utils`, `cooldown_utils`, `antigravity_utils`.
Differential-fuzz clean (0 genuine mismatches vs references): `seq_utils`, `chunk_utils`,
`number_utils`, `sort_utils`, `template_utils`, `markdown_utils`, `pattern_utils`,
`hostname_utils`, `id_utils`, `textwrap_utils`, `data_utils`, `tree_utils`, `regex_utils`,
`url_utils`, `compression_utils`, `cache_utils`, `rate_limiter_utils`, `circuit_breaker_utils`,
`deque_utils`, `context_utils`, `uuid_utils`, `warnings_utils`, `random_utils`, `config_schema`,
`prompt_utils`, `dict_utils`. Prefer modules NOT in this list for the next hunt.