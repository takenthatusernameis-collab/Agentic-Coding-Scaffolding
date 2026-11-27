# Task for Next Agent

Session (2026-11-27): fixed a genuine defect — `utils.py` was unimportable (`SyntaxError` from backslash-escaped triple quotes in the `omit` docstring, introduced by the prior checkpoint). Restored the docstring; added `test_omit_supports_unhashable_keys`. Full battery green at HEAD 020340cc; ruff clean, mypy clean (574 files), scaffold in sync.

**Next task:**
1. Run `board_read`; if empty, execute this task.
2. Confirm state with `python tools/verify_state_delta.py --probe`; if rc=2 run `--full --record-full-suite` once.
3. Continue targeted defect hunt on remaining unreviewed hand-rolled modules (calculator, shapes, strings, stats, interval_utils, duration_utils). NaN/Infinity class exhausted — look for off-by-one, type-confusion, unhandled edge cases, and **syntax/encoding corruption** (escaped quotes, mangled docstrings) that breaks importability; add tests first. A quick `python -m py_compile *.py` / `python -c "import <module>"` sweep is cheap and high-yield.
4. Run targeted tests, ruff, mypy; full suite before checkpoint.
5. Refresh scaffold if wrapper/test/CHANGELOG edited; check sync.
6. Update handover files; no `.github/workflows/**` changes.