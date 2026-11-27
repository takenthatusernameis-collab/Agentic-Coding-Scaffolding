# Task for Next Agent

Session (2026-11-27): state verification only. `board_read` empty (bootstrap session); no task from a previous agent. `python tools/verify_state_delta.py --probe` rc=2 (checkpoint behind HEAD `a904dd3e` on auto-committed checkpoint commits); ran `--full --record-full-suite` once — passed, checkpoint advanced to HEAD `a904dd3e`. Scanned `number_utils.py`/`prime_utils.py`/`stats.py` for remaining `float(...)`/`math.sqrt`/`math.factorial` conversions of huge ints; the prior session's fixes cover the live leak sites (`stats.py` all functions + `sum_of_proper_divisors`; `is_wilson_prime`/`is_perfect_power`/`is_prime_power` already safe). No new defects found; no source changes. ruff/mypy clean; `refresh_scaffold.py --check` in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. (Optional polish) Document the `OverflowError` → `ValueError("result is too large to represent as a finite float")` contract in the `Raises:` sections of the modified `stats.py` functions, mirroring `calculator.power`.
4. (Optional) Scan remaining hand-rolled numeric modules (`number_utils`, `prime_utils`, etc.) for any other undocumented `OverflowError`/`ValueError` leaks on huge or non-finite inputs (`float(...)`/`math.sqrt`/`math.log`/`math.factorial` conversions). Add tests first; prefer state-delta checks.
5. Run targeted tests, ruff, mypy; full suite before checkpoint.
6. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
7. Update handover files; no `.github/workflows/**` changes.

**State:** Checkpoint advanced to HEAD `a904dd3e`. Run `python tools/verify_state_delta.py --probe` first; if rc=2 run `--full --record-full-suite` once.
" filePath">
.kilo/next_task.md