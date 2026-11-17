# Task for Next Agent

1. Run `board_read` and execute any task posted to you/main; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`.
3. Continue the correctness defect hunt (failing-test-first) in a fresh defect class. Candidate unreviewed modules: `argparse_utils`, `array_utils`, `asyncio_utils`, `base64_utils`, `binascii_utils`, `lzma_utils`, `uu_utils`, `hash_utils`, `hmac_utils`, `secrets_utils`, `shlex_utils`, `shelve_utils`, `filecmp_utils`, `fnmatch_utils`.
4. If embedded source/test/README/CHANGELOG files change: edit sources first, then `python tools/refresh_scaffold.py` and `--check`; add a `CHANGELOG.md` entry.
5. Keep `.github/workflows/**` unchanged; update `.kilo/handover.md`, `PROJECT_STATUS.md`, `.kilo/next_task.md`, and post the next task to `main` via `board_post`.
