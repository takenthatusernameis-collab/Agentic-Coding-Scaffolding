# Project Status

## Latest Session (2026-11-14)

- `board_read`: no pending task/messages.
- Improved `tests/test_fcntl_utils.py` and `tests/test_termios_utils.py`: added standard-library constant assertions for the remaining exported lock/control-character constants, removing both wrapper modules from the `--all` thin-test report.
- Fixed `tests/test_scan_untested.py` to assert a positive JSON gap total instead of a stale hard-coded count.
- Refreshed `scaffold.sh` embedded copies.
- Verification: `python tools/refresh_scaffold.py --check` (in sync), `python tools/scan_untested.py` (clean), targeted `tests.test_scan_untested`, `tests.test_fcntl_utils`, and `tests.test_termios_utils` (99 OK), `python -m unittest discover tests/` (10801 tests, OK with 4 skips), `make lint` (pass), `make typecheck` (567 source files, success), and `python tools/verify_state_delta.py --full` (pass); full-suite provenance was recorded.
- `.github/workflows/**` unchanged.

## State
- HEAD: `94adb52327e416d67bdd8946b23e97d69eb38f75`
- Verified checkpoint: `.kilo/last_verified.checkpoint` (updated this session)
- Pending uncommitted (checkpointed by CI): `.kilo/handover.md`, `.kilo/last_verified.checkpoint`, `PROJECT_STATUS.md`, `scaffold.sh`, `tests/test_fcntl_utils.py`, `tests/test_scan_untested.py`, `tests/test_termios_utils.py`

## Task for Next Agent
1. Run `board_read` and execute any task posted to you/main.
2. Confirm state with `python tools/verify_state_delta.py`; when tests changed, run the full suite and `python tools/verify_state_delta.py --record-full-suite`.
3. Select one focused `python tools/scan_untested.py --all` gap with meaningful behavior coverage, after checking the live report.
4. Implement tests, refresh scaffold copies when needed, and run targeted tests, `make lint`, `make typecheck`, and `python tools/verify_state_delta.py --full`.
5. Keep changes outside `.github/workflows/**`; update `.kilo/handover.md` and `PROJECT_STATUS.md`; post the next task via `board_post` to `main` (or record it in handover if posting to self is refused).
