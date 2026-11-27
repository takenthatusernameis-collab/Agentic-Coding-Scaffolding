# Task for Next Agent

Session (2026-11-27): state verified green at HEAD b7e55cd8; audit scan now 0 issues (triaged `operator_utils` divide/modulo `ZeroDivisionError` delegation). Accepts-invalid-input NaN/Infinity hunt is exhausted across hand-rolled numeric modules (shapes/stats/calculator/cmath/duration/interval/cooldown/number/prime all guard `isfinite`).

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Targeted defect hunt on hand-rolled modules not yet reviewed (string/text/terminal utils, ring_buffer_utils, semver_utils, slugify_utils); accepts-invalid-input NaN/Infinity class is exhausted — look for off-by-one, type-confusion, or unhandled edge cases instead; add tests first.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.