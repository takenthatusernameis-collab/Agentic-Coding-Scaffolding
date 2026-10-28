## Latest Session (2026-10-28) — added coerce_to_int to type_check_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6292 tests and passes, `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `__all__` to `type_check_utils.py` (it was the only wrapper module missing an explicit export list, inconsistent with every other module's convention).
- Added `coerce_to_int(value)` to `type_check_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation complementing `coerce_to_str`; it accepts ints (including bools), floats, and numeric strings, raising `TypeError` for unsupported types and `ValueError` for non-numeric strings.
- Added `TestCoerceToInt` to `tests/test_type_check_utils.py` covering ints, numeric strings, bools, floats, negative strings, the `ValueError` path, and the `TypeError` paths for lists and None (8 new tests).
- Updated the `type_check_utils` prose section of `README.md` to document `coerce_to_int`.
- Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes, `make lint` clean, `make typecheck` reports the same pre-existing errors as before (unchanged by this work), scaffold sync clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added digit_count to number_utils

The board held no task (bootstrap).

Completed in this session:

- Added `digit_count(value)` to `number_utils.py` returning the number of decimal digits of an integer (sign ignored; zero returns 1), with `TypeError` validation. Exported in `__all__`, Google-style docstring with doctests.
- Added `TestDigitCount` to `tests/test_number_utils.py` (4 new tests).
- Updated `README.md` and synchronized with `make refresh-scaffold`.

## Latest Session (2026-10-28) — added is_coprime to number_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` failed on scaffold-sync (embedded `number_utils.py`/`tests/test_number_utils.py` stale, missing `is_coprime`) and `make lint` reported an unused `is_coprime` import in `tests/test_number_utils.py`; `make typecheck` was clean.

Completed in this session:

- Added `TestIsCoprime` to `tests/test_number_utils.py` covering coprime pairs, non-coprime pairs, sign/zero edge cases, and the `TypeError` paths (13 new tests); this uses the previously imported-but-unused `is_coprime`, clearing the `F401` lint error.
- Updated the `number_utils` module tree entry and prose section of `README.md` to document `is_coprime`.
- Recorded the change in this Unreleased session entry of `CHANGELOG.md`.
- Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes, `make lint` clean, `make typecheck` clean, scaffold sync clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added digit_sum to number_utils

The board held no task (bootstrap). Verified repository health before starting: `make lint` was failing on a pre-existing import regression in `tests/test_number_utils.py` (8 ruff errors), `make typecheck` was clean, and `python tools/refresh_scaffold.py --check` reported 2 stale embedded copies (`number_utils.py`, `tests/test_number_utils.py`) left by the previous checkpoint commit; all were resolved before adding new work.

Completed in this session:

- Fixed a pre-existing lint regression in `tests/test_number_utils.py`: the `is_even` and `is_odd` top-level imports were unused because `TestIsEven`/`TestIsOdd` use local imports, causing 8 ruff errors (F401/F811); removed the unused imports.
- Added `digit_sum(value)` to `number_utils.py` returning the sum of the decimal digits of an integer (sign ignored), with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int/bool arguments.
- Added `TestDigitSum` to `tests/test_number_utils.py` covering basic sums, sign handling, single digits, and the `TypeError` path; imported `digit_sum` at the top of the test file to match the module's `__all__` contract.
- Updated the `number_utils` module tree entry and prose section of `README.md` to document `digit_sum`.
- Verified: `make test` (full suite) passes, `make lint` clean, `make typecheck` clean, `python tools/refresh_scaffold.py --check` in sync after `make refresh-scaffold`.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added largest_prime_factor to prime_utils

The board held no task. Verified repository health: `make test` passed (183 tests in test_prime_utils), `make lint` is clean, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `largest_prime_factor(n)` to `prime_utils.py` returning the largest prime factor, with validation (`TypeError` for non-int/bool, `ValueError` for n < 1 or n == 1), typed signature, `__all__` export, and Google-style docstring.
- Added `TestLargestPrimeFactor` to `tests/test_prime_utils.py` with basic, prime-power, and validation cases; imported `largest_prime_factor`.
- Updated `README.md` to list `largest_prime_factor` in the `prime_utils` module description.
- Verified: `make test` (full suite) passes, `make lint` clean, `python tools/refresh_scaffold.py --check` in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added is_close to number_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6262 tests and passes, `make lint` is clean, `python tools/refresh_scaffold.py --check` reports all embedded copies in sync, and `make typecheck` is not available in this environment (mypy not installed).

Completed in this session:

- Added `is_close(a, b, *, rel_tol=1e-09, abs_tol=0.0)` to `number_utils.py` returning whether two numbers are within a relative and absolute tolerance of each other (wrapping `math.isclose`), with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation consistent with the rest of the module.
- Added `TestIsClose` to `tests/test_number_utils.py` covering equal values, within/outside default tolerance, custom `abs_tol` and `rel_tol`, negative values, zeros, `TypeError` paths (non-number arguments, bool arguments, non-number tolerances), and negative-tolerance `ValueError` paths (9 new tests). Imported `is_close` in the test file's import block to match the `__all__` contract.
- Updated the `number_utils` module tree entry and prose section of `README.md` to document `is_close`.
- Verified the work: `make test` runs 6271 tests and passes, `make lint` is clean, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added round_half_up to number_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6224 tests and passes, `make lint` is clean, `python tools/refresh_scaffold.py --check` reports all embedded copies in sync, and `make typecheck` is not available in this environment (mypy not installed).

Completed in this session:

- Added `round_half_up(value, places=0)` to `number_utils.py` as a complement to `round_to`, which uses banker's rounding (round-half-to-even). The new helper rounds a value whose fractional part is exactly 0.5 at the requested precision away from zero (so `2.5` -> `3` and `-2.5` -> `-3`), using a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation consistent with the rest of the module.
- Added `TestRoundHalfUp` to `tests/test_number_utils.py` covering default places, negative halves rounding away from zero, multi-place rounding, zero places on integers, no-rounding cases, zero value, large precision, `TypeError` paths (non-number, non-int places, bool places), and the negative-places `ValueError` (10 new tests). Imported `round_half_up` in the test file's import block to match the `__all__` contract.
- Updated the `number_utils` module prose section and file listing of `README.md` to document `round_half_up`.
- Verified the work: `make test` runs 6234 tests and passes, `make lint` is clean, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added tests for count_words, truncate_lines, and normalize_line_endings

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6145 tests and passes, `make lint` and `make typecheck` are clean on touched files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Audited the `prompt_utils` module against its test suite and found three public exports listed in `__all__` and the README that had no corresponding tests: `count_words`, `truncate_lines`, and `normalize_line_endings` (all other 41 exports were already covered). These were fully implemented with typed signatures and input validation but left a coverage gap.
- Added `TestCountWords`, `TestTruncateLines`, and `TestNormalizeLineEndings` to `tests/test_prompt_utils.py`, covering basic counts/truncation/normalization, empty inputs, whitespace handling, CRLF/CR line endings, boundary behavior (exact line count, zero lines, custom/empty suffix), and the `TypeError`/`ValueError` paths for non-string and non-int arguments (28 new tests). Imported the three helpers in the test file's import block to match the `__all__` contract.
- Verified the work: `make test` runs 6173 tests and passes, `make lint` is clean on the touched files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added tests for count_lowercase, count_uppercase, count_digits, removeprefix, and removesuffix

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6145 tests and passes, `make lint` and `make typecheck` are clean on touched files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Audited the `strings` module against its test suite and found five public exports listed in `__all__` and the README that had no corresponding tests: `count_lowercase`, `count_uppercase`, `count_digits`, `removeprefix`, and `removesuffix` (`count_letters` was already covered). These were fully implemented with typed signatures and input validation but left a coverage gap.
- Added `TestCountLowercase`, `TestCountUppercase`, `TestCountDigits`, `TestRemovePrefix`, and `TestRemoveSuffix` to `tests/test_strings.py`, each covering basic counts/removals, empty inputs, case sensitivity, boundary behavior (full match, absent prefix/suffix), and the `TypeError` paths for non-string arguments (28 new tests). Imported the five helpers in the test file's import block to match the `__all__` contract.
- Added Google-style docstring `Examples` sections (with doctests) to `count_uppercase`, `count_lowercase`, `removeprefix`, `removesuffix`, and `count_digits` in `strings.py` to match the documentation style of the rest of the module.
- Updated the `strings` module prose section of `README.md` to list `count_lowercase`, `count_uppercase`, `count_digits`, and `count_letters` alongside the existing exports.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — extended version_utils with prerelease/build metadata helpers

The board held no task (bootstrap). Verified repository health before starting: `make test` ran 6120 tests with all passing, `make lint` and `make typecheck` were clean on touched files, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Extended `version_utils.py` with prerelease/build metadata helpers: `get_build_metadata` (with `get_build`), `strip_prerelease` (with aliases), `strip_build_metadata` (with aliases), and `strip_metadata` to remove both suffixes. Updated `__all__` and added Google-style docstrings with doctests.
- Added corresponding tests in `tests/test_version_utils.py` (new test classes for build metadata, stripping prerelease/build/combined) and updated imports.
- Updated `README.md` and `.kilo/command/scaffold-project.md` to document the new version utilities.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.


## Latest Session (2026-10-28) — fixed type_check_utils scaffold-sync failure

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6120 tests and fails once on `tests/test_scaffold_sync.py::TestScaffoldSync::test_every_module_is_asserted_by_scaffold_tests` for `type_check_utils` (a real registration gap, not environment-related), `make lint` reports only pre-existing errors outside the files touched, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Diagnosed the failure: `type_check_utils.py` and `tests/test_type_check_utils.py` exist in the repository and are registered in `pyproject.toml`, `README.md`, `.kilo/command/scaffold-project.md`, and the `scaffold.sh` heredocs, but `tests/test_scaffold.py`'s `expected` list (the file the sync test reads to confirm every module is asserted) was missing the `"type_check_utils.py"` / `"tests/test_type_check_utils.py"` pair. The sync test therefore flagged the module as unasserted.
- Added the missing `"type_check_utils.py"` and `"tests/test_type_check_utils.py"` entries to the `expected` list in `tests/test_scaffold.py` (in the three places the list repeats, next to the existing `"type_utils.py"` entries) so the scaffold assertions cover the module.
- Verified the work: `make test` runs 6120 tests and passes (OK), `make lint` reports no new errors in `tests/test_scaffold.py`, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added TestIsPowerOfTwo for is_power_of_two

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6116 tests and passes except 1 pre-existing failure in `tests/test_scaffold_sync.py` for `type_check_utils` (environment-related, unchanged by this work), `make lint` and `make typecheck` report only pre-existing errors outside the files touched, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Found that `prime_utils.py` exports `is_power_of_two(n)` in `__all__` and the README documents it, but `tests/test_prime_utils.py` had no test class for it (it was imported nowhere and untested), leaving a coverage gap in a module otherwise fully tested.
- Added `TestIsPowerOfTwo` to `tests/test_prime_utils.py` covering powers of two (including 1 and large values), non-powers, negatives, and the `TypeError` paths for floats, strings, None, and bools (14 new tests). Imported `is_power_of_two` at the top of the test file to match the module's `__all__` contract.
- Verified the work: `make test` runs 6130 tests and passes except the pre-existing `type_check_utils` scaffold-sync failure, `make lint` is clean on the touched files, `make typecheck` reports no issues in `tests/test_prime_utils.py`, and doctests for `prime_utils.py` pass.
- Synchronized `tests/test_prime_utils.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added is_rotation to strings.py

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6111 tests and passes except 1 pre-existing failure in `tests/test_scaffold_sync.py` for `type_check_utils` (environment-related, unchanged by this work), `make lint` and `make typecheck` report only pre-existing errors outside the files touched, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `is_rotation(s1, s2)` to `strings.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *s2* is a rotation of *s1* (equal length and *s2* is a substring of *s1* + *s1*), `False` otherwise, treating the empty string as a rotation of itself. Added `TestIsRotation` to `tests/test_strings.py` covering rotation true/false, empty inputs, case sensitivity, and the `TypeError` paths (5 new tests; 6116 tests now run). Updated the `strings` module prose section of `README.md`. Recorded the change in this CHANGELOG entry. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6116 tests and passes except the 1 pre-existing `type_check_utils` scaffold-sync failure, `make lint` passes cleanly on `strings.py` and `tests/test_strings.py`, `make typecheck` reports no issues in `strings.py`, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added random_choices

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6062 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 518 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `random_choices(items, weights=None, k=1, seed=None)` to `random_utils.py` returning ``k`` elements with replacement, with typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError`/`ValueError` validation (rejecting bool/non-int `k`, negative `k`, length mismatches, negative weights, zero-sum weights, and empty sequences).
- Added alias `random_choice_with_replacement` for `random_choices`.
- Added `TestRandomChoices` to `tests/test_random_utils.py` covering basic with-replacement sampling, weighted sampling with replacement, single-item sequences, reproducibility, alias, and validation paths.
- Updated the `random_utils` module prose section of `README.md` to list `random_choices` and its alias.
- Synchronized `random_utils.py`, `tests/test_random_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs all tests passing, `make lint` is clean, `make typecheck` reports no issues in 518 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

Completed in this session:

- Added `random_bool(probability=0.5, seed=None)` to `random_utils.py` with typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError`/`ValueError` validation (rejecting bools and non-numbers, enforcing `0 <= probability <= 1`).
- Added `coin_flip(seed=None)` to `random_utils.py` as a convenience wrapper for `random_bool(0.5, seed=seed)`.
- Added `TestRandomBool` and `TestCoinFlip` to `tests/test_random_utils.py` covering default/reproducibility, probability bounds (0.0/1.0), out-of-range `ValueError`, non-numeric/bool `TypeError` paths, and basic behavior.
- Updated the `random_utils` module prose section of `README.md` to list `random_bool` and `coin_flip`.
- Synchronized `random_utils.py`, `tests/test_random_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6062+ tests (all passing), `make lint` is clean, `make typecheck` reports no issues in 518 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

Completed in this session:

- Found that the preceding `chore(kilo): checkpoint agent session` commit (69fe317) added `standard_error(numbers)` to `stats.py` (typed signature, `__all__` export, Google-style docstring with doctests, `TypeError`/`ValueError` validation) but left the work incomplete: no test class existed in `tests/test_stats.py`, the `standard_error` helper was not imported at the top of the test file, the `stats` prose section of `README.md` did not mention it, and no Unreleased `CHANGELOG.md` entry existed.
- Added `TestStandardError` to `tests/test_stats.py` covering basic cases, three-value, negatives, floats, single-element `ValueError`, empty-list `ValueError`, non-list `TypeError`, non-numeric `TypeError`, and bool `TypeError` paths (9 new tests; 6053 tests now pass). Imported `standard_error` at the top of the test file to match the module's `__all__` contract.
- Updated the `stats` module prose section of `README.md` to document `standard_error`.
- Recorded the `standard_error` addition in the Unreleased section of `CHANGELOG.md`.
- Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6053 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 518 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added boundary tests for six stats helpers

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 5992 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 518 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Audited `stats.py` coverage and found six public functions exported in `__all__` with no test class: `range`, `sum_values`, `sum_of_cubes`, `coefficient_of_variation`, `geometric_mean`, and `harmonic_mean`.
- Added `TestRange`, `TestSumValues`, `TestSumOfCubes`, `TestCoefficientOfVariation`, `TestGeometricMean`, and `TestHarmonicMean` to `tests/test_stats.py` covering basic cases, single-element lists, negatives, floats, empty-list `ValueError`, non-list `TypeError`, non-numeric `TypeError`, and bool `TypeError` paths (47 new tests; 6039 tests now pass). Imported all six helpers at the top of the test file to match the module's `__all__` contract.
- Expanded the docstrings of those six functions in `stats.py` with `Args`/`Returns`/`Raises` sections and `Examples` doctests to match the style of the other functions in the module.
- Updated the `stats` module prose section of `README.md` to document the six helpers.
- Verified the work: `make test` runs 6044 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 518 source files.
- Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-27) — added count_non_blank_lines boundary tests

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 5942 tests and passes (1 failure and 6 errors are pre-existing, environment-related SyntaxErrors in platform modules — confirmed identical with the change stashed), `make lint` is clean, `make typecheck` reports 11 pre-existing errors in 10 files (identical with the change stashed), and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Found that `prompt_utils.py` exports `count_non_blank_lines(text)` in `__all__` and the README lists it, but `tests/test_prompt_utils.py` had no test class for it (it was imported nowhere and untested), leaving a coverage gap in a module otherwise fully tested.
- Added `TestCountNonBlankLines` to `tests/test_prompt_utils.py` covering empty, single, multiple, trailing-newline, blank-line exclusion, whitespace-only lines, all-blank, CRLF, and `TypeError` paths (10 new tests). Imported `count_non_blank_lines` at the top of the test file to match the module's `__all__` contract.
- Verified the work: `make test` runs 5952 tests and passes with no new failures, `make lint` is clean, and `make typecheck` reports the same 11 pre-existing errors in 10 files (unchanged by this work).
- Synchronized `tests/test_prompt_utils.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

- Added boundary tests for `count_non_blank_lines(text)` to `tests/test_prompt_utils.py` (`TestCountNonBlankLines`), covering empty, single, multiple, trailing-newline, blank-line exclusion, whitespace-only lines, all-blank, CRLF, and `TypeError` paths; the helper was already exported in `prompt_utils.__all__` but lacked test coverage. Synchronized `tests/test_prompt_utils.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `rstrip_lines(text)`, `lstrip_lines(text)`, and `strip_lines(text)` to `prompt_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation; they strip whitespace (spaces/tabs) from each line in the respective direction while preserving line endings and blank lines. Added `TestLstripLines` and `TestStripLines` to `tests/test_prompt_utils.py` covering basic cases, whitespace-only lines, empty strings, and `TypeError` paths. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Audited and hardened `math_utils.py` boundary cases to match project conventions: added typed `__all__`, a `_require_int` helper, and `TypeError`/`ValueError` validation on every public function (`factorial`, `fibonacci`, `gcd`, `lcm`, `is_prime`, `clamp`, `is_even`); `clamp` now accepts floats and rejects bools. Expanded `tests/test_math_utils.py` with boundary tests (zero, negatives, large factorials, zero/negative args for gcd/lcm, large primes, floats, bools, non-ints) and added `is_even` with tests. Updated the `math_utils` module tree entry and prose section of `README.md`. Synchronized `math_utils.py`, `tests/test_math_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `z_scores(numbers, population=True)` to `stats.py` returning the standardized z-scores of the values, measuring how many standard deviations each value is from the mean. Added `TestZScores` to `tests/test_stats.py`. Updated the `stats` module prose section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Audited `strings.py` boundary cases (empty strings, single char, whitespace-only, unicode edge cases, non-string/invalid-type inputs, negative/invalid ints, very long strings). Added boundary tests in `tests/test_strings.py` for partition/rpartition/split_lines/join_lines/replace_many/strip_html/between/contains_any/contains_all/char_frequency/snake_to_camel/is_subsequence unicode cases and more TypeError/ValueError paths; all existing behavior verified. Cross-checked helper logic against brute-force expectations where practical. Synchronized `tests/test_strings.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased

### Added
- Added `reverse_lines(text)` to `prompt_utils.py` reversing the order of lines in *text*, with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation. Added tests to `tests/test_prompt_utils.py`.
- Added `count_letters(s)` to `strings.py` returning the number of alphabetic characters in *s*, with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation. Added `TestCountLetters` to `tests/test_strings.py`.
- Added `count_characters(text)` to `prompt_utils.py` returning the number of characters in *text* (including whitespace), matching `len`, with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments. Added `TestCountCharacters` to `tests/test_prompt_utils.py` covering empty, ASCII, whitespace-counted, unicode, single-character, and `TypeError` paths. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `standard_error(numbers)` to `stats.py` returning the standard error of the mean (the sample standard deviation divided by the square root of the sample size), with typed signature, `__all__` export, Google-style docstring, and `TypeError`/`ValueError` validation (raising `ValueError` for empty lists or single-element lists). Added `TestStandardError` to `tests/test_stats.py` covering basic cases, negatives, floats, single-element `ValueError`, empty-list `ValueError`, and `TypeError` paths. Updated the `stats` module prose section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `format_farewell(name, farewell="Goodbye")` to `greeting_utils.py` returning a formatted farewell string, with typed signature, Google-style docstring, and `TypeError` validation. Added `TestFormatFarewell` to `tests/test_greeting_utils.py` covering default, custom, empty name, and `TypeError` paths. Updated the `greeting_utils` module prose section of `README.md`.
- Added comprehensive boundary tests for `strings.py` (empty strings, whitespace-only, unicode/multibyte, type errors, edge cases) to `tests/test_strings.py`.

- Added `get_prerelease(version)` and `get_prerelease_tag(version)` to `version_utils.py` returning the prerelease tag after `-` or `None` if absent, with `TypeError` validation and exports in `__all__`. Added `TestGetPrerelease` to `tests/test_version_utils.py`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_title(s)` to `strings.py` returning `True` when *s* is titlecased (all cased characters follow title-case rules and at least one alphabetic character is present), `False` otherwise. It validates that *s* is a string, raising `TypeError` otherwise, and is exported in `__all__` with a Google-style docstring. Added `TestIsTitle` to `tests/test_strings.py` covering titlecased, mixed-case, no-alphabetic, and `TypeError` paths. Updated the `strings` module prose section of `README.md`.

- Implemented `count_blank_lines(text)` in `prompt_utils.py` (declared in `__all__` and tested but previously undefined) returning the number of blank (whitespace-only) lines in *text*, with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation.

- Added `first_line(text)` and `last_line(text)` to `prompt_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation; they return the first and last lines with line endings stripped, handling empty strings and CRLF/CR. Added `TestFirstLine` and `TestLastLine` to `tests/test_prompt_utils.py` covering basic cases, CRLF/CR, trailing newlines, and `TypeError` paths. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `midhinge(numbers)` to `stats.py` returning the midhinge ((Q1 + Q3) / 2), a robust measure of central tendency. It validates its input (raising `TypeError` for non-lists or non-numeric values and `ValueError` for an empty list) and is exported in `__all__` with a Google-style docstring and doctests. Added `TestMidhinge` to `tests/test_stats.py`. Updated the `stats` module prose section of `README.md`.

- Added `product(numbers)` to `stats.py` returning the product of all values in a list of numbers, complementing `sum_values`. It validates its input (raising `TypeError` for non-lists or non-numeric values and `ValueError` for an empty list) and is exported in `__all__` with a Google-style docstring and doctests. Added `TestProduct` to `tests/test_stats.py`. Updated the `stats` module prose section of `README.md`.

- Added `is_prerelease(version)` to `version_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation; it returns `True` when *version* contains a pre-release marker (a hyphen suffix), `False` otherwise. Added `TestIsPrerelease` to `tests/test_version_utils.py`. Updated the `version_utils` module prose section of `README.md`.

- Added `is_isogram(text)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* is an isogram (no repeating letters, case-insensitive, ignoring non-letter characters), `False` otherwise, treating the empty string as an isogram. Added `TestIsIsogram` to `tests/test_string_utils.py` covering isograms, non-isograms, case-insensitivity, empty/single-char inputs, non-letter characters, unicode, whitespace-only, the `TypeError` path, and a very long string. Updated the `string_utils` module prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, README, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `primorial(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with `TypeError`/`ValueError` validation (returns `1` for `n < 2`, raises `ValueError` for `n < 0`), and it returns the product of all prime numbers less than or equal to *n* (*n#*). Added `TestPrimorial` to `tests/test_prime_utils.py`. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `product(numbers)` to `stats.py` returning the product of all values in a list of numbers, complementing `sum_values`. It validates its input (raising `TypeError` for non-lists or non-numeric values and `ValueError` for an empty list) and is exported in `__all__` with a Google-style docstring and doctests. Added `TestProduct` to `tests/test_stats.py`. Updated the `stats` module prose section of `README.md`.

- Added `is_prerelease(version)` to `version_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation; it returns `True` when *version* contains a pre-release marker (a hyphen suffix), `False` otherwise. Added `TestIsPrerelease` to `tests/test_version_utils.py` covering pre-release and stable cases plus the `TypeError` path.

- Added `is_isogram(text)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* is an isogram (no repeating letters, case-insensitive, ignoring non-letter characters), `False` otherwise, treating the empty string as an isogram. Added `TestIsIsogram` to `tests/test_string_utils.py` covering isograms, non-isograms, case-insensitivity, empty/single-char inputs, non-letter characters, unicode, whitespace-only, the `TypeError` path, and a very long string. Updated the `string_utils` module prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, README, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Audited `string_utils.py` boundary cases (very long strings, unicode, consecutive and leading/trailing underscores, empty and single-character inputs, `width=1`, non-string/invalid types including bools passed as ints) and added comprehensive boundary tests to `tests/test_string_utils.py` covering `slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `wrap_words`, `indent_text`, `remove_extra_whitespace`, `remove_blank_lines`, and `title_case`. Added invariant-based cross-check tests (slug character class, line widths, word order preservation, title-case capitalization, pluralize count-one) verifying behavior against expectations. Moved the `if __name__ == "__main__"` block to the end of `tests/test_string_utils.py` so `TestWrapWords` runs when the file is executed directly, matching the convention applied to `tests/test_strings.py` and `tests/test_shapes.py`. Cross-checked behavior against expectations; all string_utils tests pass. Synchronized `tests/test_string_utils.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Audited `string_utils.py` boundary cases (empty strings, single char, whitespace-only, unicode, non-string/invalid types, bools passed as ints, negative/invalid widths/lengths/max_words, suffix/ prefix validation) and added comprehensive boundary tests to `tests/test_string_utils.py` covering `slugify` unicode/whitespace, `truncate` edge cases (empty string, single char, suffix longer than length), `wrap_text` and `wrap_words` boundary paths, `truncate_words` bool/negative/empty cases, `remove_blank_lines`/`remove_extra_whitespace`, and `title_case` with custom small words and empty strings. Cross-checked behavior against expectations; all string_utils tests pass. Updated `string_utils` module prose section in `README.md`. Synchronized `tests/test_string_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Repaired pre-existing lint regressions in `tests/test_strings.py` (introduced by an earlier `strings.py` boundary-audit session but never corrected): removed 100 unused-import (`F401`) and redundant-blank-line (`W293`) errors and fixed a single over-length comment line (`E501`). `make lint` now reports "All checks passed!" across the whole tree, restoring the project's claimed green-lint invariant. All 349 `test_strings.py` tests still pass. Synchronized `tests/test_strings.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `truncate_words(text, max_words, suffix="...")` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError`/`ValueError` validation; it truncates a string to at most *max_words* whitespace-separated words and appends *suffix* when truncation occurs, returning the text unchanged when it already fits. Added `TestTruncateWords` to `tests/test_string_utils.py` covering the default suffix, a custom suffix, no-truncation cases, the exact word count, the empty string, zero max words, whitespace collapsing, and the `TypeError`/`ValueError` paths. Updated the `string_utils` module tree entry and prose section of `README.md` and the `string_utils` line of `.kilo/command/scaffold-project.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, README, the command doc, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `remove_blank_lines(text)` to `prompt_utils.py` with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation; it removes blank (whitespace-only) lines from *text*.

- Audited `strings.py` boundary cases (empty strings, single char, whitespace-only, unicode edge cases, non-string/invalid-type inputs, negative/invalid ints, bools for int params, very long strings) and added comprehensive boundary tests to `tests/test_strings.py` covering `is_alpha`, `is_alphanumeric`, `is_ascii`, `is_digit`, `is_hex`, `is_integer`, `is_printable`, `is_identifier`, `is_pangram`, `is_palindrome` with flag variants, `first_n`/`last_n`/`take`/`drop`, `count_occurrences`, `starts_with`/`ends_with`, `levenshtein_distance`, `chunk_string`, `initials`, `swap_case`, and more TypeError/ValueError paths; all existing behavior verified. Cross-checked helper logic against Python string semantics where practical. Synchronized `tests/test_strings.py` and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `root_mean_square` to `stats.py` with tests.
- Bootstrap session verified scaffold sync, lint, and typecheck all pass; posted next task to audit `math_utils.py` boundary cases.
- Audited and hardened `array_utils.py` boundary cases (non-array/non-string/non-int/invalid iterables), added stricter TypeError validation consistent with project style, and expanded `tests/test_array_utils.py` with boundary tests; synchronized `array_utils.py`, `tests/test_array_utils.py`, `README.md`, `CHANGELOG.md` into `scaffold.sh` with `make refresh-scaffold`.

- Added `hostname_utils.py` with `is_valid_hostname`, `normalize_hostname`, `get_local_hostname`, `is_fully_qualified`, and `split_hostname` helpers, each with a typed signature, `__all__` export, a Google-style docstring, and `TypeError`/`ValueError` input validation, plus unit tests in `tests/test_hostname_utils.py`. Synchronized `hostname_utils.py`, `tests/test_hostname_utils.py`, `README.md`, `.kilo/command/scaffold-project.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Audited `prime_utils` boundary cases (negative inputs, 0, 1, 2, 3, large primes, large prime powers) and confirmed every helper classifies them correctly: `is_prime`, `is_composite`, `is_semiprime`, `is_squarefree`, `is_prime_power`, `is_circular_prime`, `is_emirp`, `is_twin_prime`, `is_cousin_prime`, `is_sexy_prime`, `is_palindromic_prime`, `is_mersenne_prime`, `is_safe_prime`, `is_sophie_germain_prime`, `is_perfect_number`, `is_abundant_number`, `is_deficient_number`, `sum_of_proper_divisors`, `primes_up_to`, `nth_prime`, `next_prime`, `prev_prime`, `is_coprime`, `is_perfect_square`, and `prime_count` all behave as documented. Cross-checked `is_prime`, `prime_factors`, `prime_count`, `is_squarefree`, `is_semiprime`, and `is_prime_power` against brute-force reference implementations for the ranges −50..500 and 2..2000 with zero mismatches.

- Added `prime_count` to the `prime_utils` module prose section of `README.md`; it was present in the architecture tree but missing from the prose description.

- Added boundary test classes to `tests/test_prime_utils.py`: `TestPrimeCount`, `TestPrimeClassificationNegatives`, `TestSumOfProperDivisorsEdge`, `TestIsPrimePowerLarge`, `TestIsSquarefreeEdge`, `TestIsSemiprimeEdge`, `TestIsPerfectSquareEdge`, `TestNextPrevPrimeEdge`, `TestPrimesUpToEdge`, `TestIsCoprimeEdge`, and `TestIsPerfectAbundantDeficientEdge`, covering negative inputs, 0, 1, 2, 3, large prime powers (2^31, 2^62, 3^20), and the `TypeError` paths. Synchronized `tests/test_prime_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `remove_blank_lines` to `strings.py`.

- Added `is_subsequence(needle, haystack)` to `strings.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-string arguments; it returns `True` when *needle* is a subsequence of *haystack* (every character of *needle* appears in *haystack* in the same relative order, not necessarily consecutively), `False` otherwise; the empty needle is a subsequence of any string. Added `TestIsSubsequence` to `tests/test_strings.py` covering present/missing cases, the empty-needle case, empty haystack, case sensitivity, and the `TypeError` paths. Updated the `strings` module prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `chunk_string(s, size)` to `strings.py` with validation (TypeError for non-string/non-int, ValueError for non-positive size) returning chunks of length *size* (empty list for empty string). Added `TestChunkString` to `tests/test_strings.py`. Updated `README.md`. Synchronized into scaffold.

- Added `indent_lines(text, prefix="    ", *, skip_blank=False)` to `prompt_utils.py` as a companion to `truncate_lines` and `wrap_prompt`: it prefixes every line of *text* with *prefix*, leaving blank lines untouched when *skip_blank* is True. It validates that *text* and *prefix* are strings and *skip_blank* is a bool, raising `TypeError` otherwise. Added `TestIndentLines` to `tests/test_prompt_utils.py` covering the default prefix, a custom prefix, blank-line handling with both modes, the empty-string case, and the `TypeError` paths. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `truncate_lines` to `prompt_utils.py`.
- Added `is_pangram(s)` to `strings.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-string arguments; it returns `True` when *s* contains every letter of the English alphabet at least once (case-insensitive, ignoring non-alphabetic characters), `False` otherwise (including for the empty string). Added `TestIsPangram` to `tests/test_strings.py`. Updated the `strings` module section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `decrement_version(version, part="patch")` to `version_utils.py` as the symmetric counterpart to `bump_version`: it validates that *version* is a string and *part* is a string, is case-insensitive on the recognized component names (`"major"`, `"minor"`, `"patch"`), and dispatches to the existing `decrement_major`/`decrement_minor`/`decrement_patch` helpers, raising `ValueError` for unrecognized parts or when the chosen component is already 0. Also exported `decrement_major`, `decrement_minor`, and `decrement_patch` (they were previously defined but absent from `__all__`), and added the `decrement` alias. Added `TestDecrementMajor`, `TestDecrementMinor`, `TestDecrementPatch`, and `TestDecrementVersion` to `tests/test_version_utils.py`. Updated the `version_utils` module tree entry and prose section of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_compatible` to `version_utils.py`.

- Added `trimmed_mean(numbers, trim_count=0)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError`/`ValueError` validation; it discards *trim_count* values from each end of the sorted list and returns the arithmetic mean of the remaining interior values, raising `ValueError` for a negative *trim_count* or one that is at least half the list length (so at least one value remains). It defaults to *trim_count* 0, in which case it matches `mean`. Added `TestTrimmedMean` to `tests/test_stats.py`. Updated the `stats` module section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `multimode(numbers)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError`/`ValueError` validation; it returns every value that shares the highest frequency in the order each value first appears (a companion to `mode`, like `statistics.multimode`). Added `TestMultimode` to `tests/test_stats.py`. Updated the `stats` module section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_initial_release` to `version_utils.py`.

- Added `has_placeholders(template)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-string arguments; it returns `True` when *template* contains at least one ``{name}`` placeholder, `False` otherwise. Added `TestHasPlaceholders` to `tests/test_prompt_utils.py`. Updated the `prompt_utils` module section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## case_utils

- Add `case_utils.py` with `kebab_case`, `pascal_case`, and `constant_case` helpers that split text on whitespace, separators, and case transitions, each with a typed signature, `__all__` export, a Google-style docstring, and input validation raising `TypeError` for non-string arguments, plus unit tests in `tests/test_case_utils.py`.
- Synchronized `case_utils.py` and `tests/test_case_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, and this CHANGELOG.

## backoff_utils

- Add `backoff_utils.py` wrapping backoff utilities with `constant_backoff` and `exponential_backoff` helpers, input validation, and typed signatures, plus unit tests in `tests/test_backoff_utils.py`.
- Synchronized `backoff_utils.py` and `tests/test_backoff_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.

- Added `kurtosis(numbers)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError`/`ValueError` validation; it returns the excess kurtosis of a list of numbers, raising `ValueError` for fewer than 4 elements or a zero standard deviation. Added tests in `tests/test_stats.py`. Updated the `stats` module section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `prime_count(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-int arguments (rejecting `bool`); it returns the number of primes less than or equal to *n* (the prime counting function π(*n*)), returning 0 for *n* < 2. Added `TestPrimeCount` to `tests/test_prime_utils.py`. Updated the `prime_utils` module section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_stable(version)` to `version_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-string arguments; it returns `True` when the major version component is at least 1, `False` otherwise. Added `TestIsStable` to `tests/test_version_utils.py`. Updated the `version_utils` module section of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_circular_prime(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-int arguments (rejecting `bool`); it returns `True` when *n* is a prime that remains prime under every cyclic rotation of its decimal digits (single-digit primes are circular primes), `False` otherwise. Added `TestIsCircularPrime` to `tests/test_prime_utils.py`. Updated the `prime_utils` module sections of `README.md` and `.kilo/command/scaffold-project.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `.kilo/command/scaffold-project.md`, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `extract_placeholders(template)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-string arguments; it returns the placeholder names in order of first appearance without duplicates. Added `TestExtractPlaceholders` to `tests/test_prompt_utils.py`. Updated the `prompt_utils` module section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_squarefree(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-int arguments (rejecting `bool`); it returns `True` when *n* is squarefree (not divisible by the square of any prime; every prime factor appears at most once), `False` otherwise (0, numbers divisible by a prime square like 4, 8, 12, 16, and negatives return the squarefree-ness of their absolute value). Added `TestSquarefree` to `tests/test_prime_utils.py`. Updated the `prime_utils` module section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added 3D shape helpers `sphere_surface_area`/`sphere_volume`, `cube_surface_area`/`cube_volume`, `cylinder_surface_area`/`cylinder_volume`, `cone_surface_area`/`cone_volume`. Synchronized into `scaffold.sh`.

- Added `cuboid_surface_area`/`cuboid_volume` (and `rectangular_prism_surface_area`/`rectangular_prism_volume` aliases) to `shapes.py` with typed signatures, `__all__` exports, validation (raising `TypeError` for non-numbers including `bool`, `ValueError` for negatives), and tests in `tests/test_shapes.py`. Updated `README.md`. Synchronized `shapes.py`, `tests/test_shapes.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_power_of_two(n)` to `prime_utils.py` with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation for non-int arguments (rejecting `bool`); returns `True` for positive powers of two (1,2,4,...), `False` otherwise (including 0 and negatives). Added tests in `tests/test_prime_utils.py`. Updated `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_whitespace`, `is_space`, `is_printable`, and `is_identifier` to `strings.py` with typed signatures, `__all__` exports, Google-style docstrings, and `TypeError` validation for non-string arguments. `is_whitespace`/`is_space` return `False` for empty strings; `is_printable` returns `False` for whitespace/control characters; `is_identifier` uses `str.isidentifier()`. Added corresponding tests in `tests/test_strings.py`. Updated `README.md` and `.kilo/command/scaffold-project.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `.kilo/command/scaffold-project.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `skewness(numbers)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError`/`ValueError` validation; it returns the population skewness of a list of numbers, raising `ValueError` for fewer than 3 elements or a zero standard deviation. Added `TestSkewness` to `tests/test_stats.py` covering symmetric, positively skewed, and invalid-input cases. Updated the `stats` module section of `README.md` to list the new helper. Synchronized `stats.py`, `tests/test_stats.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `roman_utils.py` with `to_roman`, `from_roman`, and `is_valid_roman` helpers for converting between integers and Roman numerals in the range 1 to 3999, each with a typed signature, a Google-style docstring, and input validation raising `TypeError` or `ValueError` on invalid arguments, plus unit tests in `tests/test_roman_utils.py`. Synchronized `roman_utils.py` and `tests/test_roman_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.

- Added `is_finite(value)`, `is_infinite(value)`, and `is_nan(value)` to `number_utils.py` with typed signatures, `__all__` exports, Google-style docstrings, and `TypeError` validation for non-number arguments (values are finite/inf/nan classified correctly for floats, with ints treated as finite). Added tests in `tests/test_number_utils.py`. Updated the `number_utils` module tree entry and prose section of `README.md` to list the new helpers. Synchronized `number_utils.py`, `tests/test_number_utils.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `is_non_negative(value)` and `is_non_positive(value)` to `number_utils.py` with typed signatures, `__all__` exports, Google-style docstrings, and `TypeError` validation for non-number arguments; added tests in `tests/test_number_utils.py`. Updated the `number_utils` module tree entry and prose section of `README.md` and `.kilo/command/scaffold-project.md` to list the new helpers. Synchronized `number_utils.py`, `tests/test_number_utils.py`, README, the command doc, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `is_palindromic_number(value)` to `number_utils.py` with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation for non-number arguments (rejecting `bool`). Returns `True` for non-negative integers whose decimal representation is a palindrome; raises `ValueError` for negative integers. Added tests in `tests/test_number_utils.py`. Updated documentation and synchronized copies into `scaffold.sh`.
- Added 3D shape helpers to `shapes.py`: `sphere_surface_area`/`sphere_volume`, `cube_surface_area`/`cube_volume`, `cylinder_surface_area`/`cylinder_volume`, `cone_surface_area`/`cone_volume` with typed APIs, `__all__` exports, validation (raising `TypeError` for non-numbers including `bool`, `ValueError` for negatives), and tests in `tests/test_shapes.py`. Updated `README.md` and `.kilo/command/scaffold-project.md` to document the new helpers. Synchronized `shapes.py`, `tests/test_shapes.py`, README, and the command doc into `scaffold.sh`.
- Added `is_negative(value)`, `is_positive(value)`, and `is_zero(value)` to `number_utils.py` with typed signatures, `__all__` exports, Google-style docstrings, and `TypeError` validation for non-number arguments; added tests in `tests/test_number_utils.py`. Updated the `number_utils` module tree entry and prose section of `README.md` and `.kilo/command/scaffold-project.md` to list the new helpers. Synchronized `number_utils.py`, `tests/test_number_utils.py`, README, the command doc, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `is_perfect_square(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-int arguments; returns False for negative integers and uses `math.isqrt` to test whether a non-negative integer is a perfect square. Added tests in `tests/test_prime_utils.py` covering zero, small and large squares, non-squares, negatives, and the `TypeError` path. Updated the `prime_utils` prose sections of `README.md` and `.kilo/command/scaffold-project.md` to list the new helper. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, README, the command doc, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Bootstrap session: verified repository health — `make test` runs 5410 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 544 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. The board held no task, so this session proceeded as a bootstrap.
- Added `bump_version(version, part="patch")` to `version_utils.py` as a dispatcher over the existing `bump_major`/`bump_minor`/`bump_patch` helpers: it validates that *version* is a string and *part* is a string, is case-insensitive on the recognized component names (`"major"`, `"minor"`, `"patch"`), and raises `ValueError` for unrecognized parts. Added tests in `tests/test_version_utils.py` covering the default, each explicit component, case-insensitivity, single-component inputs, and the `TypeError`/`ValueError` paths. Synchronized `version_utils.py`, `tests/test_version_utils.py`, README, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Fixed four pre-existing `ruff` errors in `strings.py` and `case_utils.py`: the `drop` alias in `strings.py` and the `dot_case` and `slash_case` aliases in `case_utils.py` were assigned `lambda` expressions (E731) and `drop` exceeded the line length limit (E501). All three are now real `def` functions with typed signatures, Google-style docstrings, and `TypeError`/`ValueError` validation matching the surrounding helpers. `drop` validates that *s* is a string and *n* is a non-negative integer, returning `s[n:]`; `dot_case` and `slash_case` validate that *text* is a string. Added tests in `tests/test_strings.py` for the `drop` edge cases (zero, full length, non-string, non-int, negative) and in `tests/test_case_utils.py` the aliases remain covered. Synchronized `strings.py`, `case_utils.py`, their tests, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Refreshed the embedded copies of `strings.py`, `tests/test_strings.py`, `case_utils.py`, and `tests/test_case_utils.py` inside `scaffold.sh` that had drifted from the repository sources, so `tests/test_scaffold_sync.py` passes again.
- Verified the work: `make test` runs 5403 tests and passes, `mypy` is clean on all 544 source files, and `ruff` reports only two pre-existing I001 import-sorting warnings in `tests/test_strings.py` and `tests/test_shapes.py` that predate this session's changes.

- Added input validation to `prompt_utils.py`: every public helper now validates its arguments and raises `TypeError` or `ValueError` on invalid inputs, matching the convention documented in `README.md`. Added `_require_string` and `_require_int` helpers; `truncate_prompt` validates `text`, `max_length`, and `suffix`; `format_prompt_template` validates `template` and converts a missing-template-key `KeyError` into a `ValueError`; `clean_prompt` validates `text`; `extract_keywords` validates `text` and `min_length`; `wrap_prompt` validates `text` and `width`; `estimate_token_count` validates `text`. Added validation tests in `tests/test_prompt_utils.py`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.

- Closed the synchronization drift left by the interrupted checkpoint commit: `shapes.py`, `tests/test_shapes.py`, `stats.py`, and `tests/test_stats.py` were committed without refreshing the embedded copies in `scaffold.sh`, so `python tools/refresh_scaffold.py --check` reported four stale copies and `tests/test_refresh_scaffold.py` failed. Ran `make refresh-scaffold`; all embedded copies are in sync.
- Repaired an API regression in `shapes.py` introduced by the interrupted checkpoint commit: `regular_polygon_area` and `regular_polygon_perimeter` were dropped from `__all__` even though the functions still exist and `regular_polygon_area` was still imported and tested. Restored both names to `__all__`.
- Gave `regular_polygon_perimeter` the typed signature, Google-style docstring, and `TypeError`/`ValueError` validation the rest of the module uses, matching `regular_polygon_area`.
- Added `TestRegularPolygonPerimeter` to `tests/test_shapes.py` covering the square, the triangle, a zero side, a negative side, too few sides, and a non-integer side count.
- Updated the `shapes` module prose section of `README.md` to list the regular polygon and ellipse helpers the module exports; synchronized `shapes.py`, `tests/test_shapes.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 5300 tests and passes, `ruff` and `mypy` are clean on the files touched, and scaffold sync is clean.

- Bootstrap session: verified full test suite (5301 tests), ruff, mypy, and scaffold sync all green; posted next handover task.
- Added `is_alpha` to `strings.py` with a typed signature, `__all__` export, a Google-style docstring, and input validation raising `TypeError` for non-string arguments; added tests in `tests/test_strings.py`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.
- Closed documentation drift in the `strings` module prose section of `README.md`: the section referenced `is_numeric` and `is_alphanumeric`, which belong to `validation_utils.py` and are not part of the `strings` public API; the section now lists only the helpers `strings.py` actually exports. Synchronized the corrected README into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `midrange` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring, and input validation raising `TypeError` for non-list or non-numeric arguments and `ValueError` for empty lists; added tests in `tests/test_stats.py`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.
- Added `sector_area` and `arc_length` to `shapes.py` with typed signatures, `__all__` exports, Google-style docstrings, and input validation raising `TypeError` for a non-numeric angle and `ValueError` for a negative radius or an angle outside [0, 360]; added tests in `tests/test_shapes.py`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.
- Hardened `polygon_area` in `shapes.py` to validate that every vertex is a 2-tuple of numbers, raising `TypeError` for a malformed vertex or a non-numeric component; added tests in `tests/test_shapes.py`; synchronized the module, its tests, and this CHANGELOG into `scaffold.sh`.
- Closed documentation drift in the `greeting_utils` module section: the README tree, the prose section, and `.kilo/command/scaffold-project.md` listed nonexistent `greet` and `random_greeting` helpers; the section now lists only the public API (`format_greeting`, `format_names`) that `greeting_utils.py` actually exports. Synchronized the corrected README and command documentation into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Hardened the `prime_utils` module with typed `__all__`, Google-style docstrings, and input validation (`TypeError` for non-int arguments, `ValueError` for out-of-range values) on `primes_up_to`, `nth_prime`, `prime_factors`, and `is_coprime`; added validation tests in `tests/test_prime_utils.py`; synchronized the module, its tests, README, and CHANGELOG into `scaffold.sh`.
- Fixed the `if __name__ == "__main__"` block placement in `tests/test_strings.py` and `tests/test_shapes.py` so their tests run when the files are executed directly, and added `tests/test_prime_utils.py` and `tests/test_version_utils.py` covering the previously untested modules; synchronized all four test files into the embedded copies of `scaffold.sh`.
- Verified full test suite (5211 tests), ruff, mypy, and scaffold sync; all green. Posted next handover task.
- Hardened the `strings` module with `reverse_words` and synchronized `strings.py`, its tests, and scaffold documentation (README and embedded `scaffold.sh`) so generated projects and docs reflect the expanded string utilities API.
- Added `is_prime` to `prime_utils.py` with input validation (`TypeError` for non-int arguments) and tests in `tests/test_prime_utils.py`; fixed the `is_coprime` docstring typo; synchronized the module, its tests, README, and CHANGELOG into `scaffold.sh`.
- Added `sort_versions` to `version_utils.py` with input validation (`TypeError` for non-list or non-string elements, `ValueError` for invalid version strings) and tests in `tests/test_version_utils.py`; synchronized the module, its tests, README, and CHANGELOG into `scaffold.sh`.
- Hardened the `strings` module with `common_prefix` and `common_suffix` helpers, each with typed signatures, Google-style docstrings, `__all__` exports, and input validation raising `TypeError` for non-string arguments; added tests in `tests/test_strings.py`; synchronized the module, its tests, and this CHANGELOG into `scaffold.sh`.
- Added `is_alphanumeric` to `strings.py` with a typed signature, `__all__` export, a Google-style docstring, and input validation raising `TypeError` for non-string arguments; added tests in `tests/test_strings.py`; updated the `strings` module section in `README.md`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.
- Added `is_digit` and `is_integer` to `strings.py` with typed signatures, `__all__` exports, Google-style docstrings, and input validation raising `TypeError` for non-string arguments; added tests in `tests/test_strings.py`; updated the `strings` module section in `README.md`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.
- Added `triangle_inradius` and `triangle_circumradius` to `shapes.py` with typed signatures, `__all__` exports, Google-style docstrings, and input validation consistent with triangle helpers; added tests in `tests/test_shapes.py`; updated the `shapes` module section in `README.md`; synchronized the module, its tests, README, and this CHANGELOG into `scaffold.sh`.

- Added `abc_utils.py` and `tests/test_abc_utils.py`.
- Added `aifc_utils.py` and `tests/test_aifc_utils.py`.
- Added `ossaudiodev_utils.py` and `tests/test_ossaudiodev_utils.py`.
- Added `antigravity_utils.py` and `tests/test_antigravity_utils.py`.
- Added `argparse_utils.py` and `tests/test_argparse_utils.py`.
- Added `array_utils.py` and `tests/test_array_utils.py`.
- Added `ast_utils.py` and `tests/test_ast_utils.py`.
- Added `async_utils.py` and `tests/test_async_utils.py`.
- Added `asyncio_utils.py` and `tests/test_asyncio_utils.py`.
- Added `atexit_utils.py` and `tests/test_atexit_utils.py`.
- Added `audioop_utils.py` and `tests/test_audioop_utils.py`.
- Added `base64_utils.py` and `tests/test_base64_utils.py`.
- Added `bdb_utils.py` and `tests/test_bdb_utils.py`.
- Added `binascii_utils.py` and `tests/test_binascii_utils.py`.
- Added `bisect_utils.py` and `tests/test_bisect_utils.py`.
- Added `bit_utils.py` and `tests/test_bit_utils.py`.
- Added `builtins_utils.py` and `tests/test_builtins_utils.py`.
- Added `bytes_utils.py` and `tests/test_bytes_utils.py`.
- Added `bz2_utils.py` and `tests/test_bz2_utils.py`.
- Added `cache_utils.py` and `tests/test_cache_utils.py`.
- Added `calendar_utils.py` and `tests/test_calendar_utils.py`.
- Added `call_once_utils.py` and `tests/test_call_once_utils.py`.
- Added `cgi_utils.py` and `tests/test_cgi_utils.py`.
- Added `cgitb_utils.py` and `tests/test_cgitb_utils.py`.
- Added `chunk_utils.py` and `tests/test_chunk_utils.py`.
- Added `circuit_breaker_utils.py` and `tests/test_circuit_breaker_utils.py`.
- Added `cli_utils.py` and `tests/test_cli_utils.py`.
- Added `cmath_utils.py` and `tests/test_cmath_utils.py`.
- Added `cmd_utils.py` and `tests/test_cmd_utils.py`.
- Added `code_utils.py` and `tests/test_code_utils.py`.
- Added `codecs_utils.py` and `tests/test_codecs_utils.py`.
- Added `codeop_utils.py` and `tests/test_codeop_utils.py`.
- Added `collections_utils.py` and `tests/test_collections_utils.py`.
- Added `color_utils.py` and `tests/test_color_utils.py`.
- Added `colorsys_utils.py` and `tests/test_colorsys_utils.py`.
- Added `compileall_utils.py` and `tests/test_compileall_utils.py`.
- Added `compression_utils.py` and `tests/test_compression_utils.py`.
- Added `concurrent_futures_utils.py` and `tests/test_concurrent_futures_utils.py`.
- Added `concurrent_utils.py` and `tests/test_concurrent_utils.py`.
- Added `config_utils.py` and `tests/test_config_utils.py`.
- Added `configparser_utils.py` and `tests/test_configparser_utils.py`.
- Added `context_utils.py` and `tests/test_context_utils.py`.
- Added `contextlib_utils.py` and `tests/test_contextlib_utils.py`.
- Added `contextvars_utils.py` and `tests/test_contextvars_utils.py`.
- Added `cooldown_utils.py` and `tests/test_cooldown_utils.py`.
- Added `copy_utils.py` and `tests/test_copy_utils.py`.
- Added `copyreg_utils.py` and `tests/test_copyreg_utils.py`.
- Added `cprofile_utils.py` and `tests/test_cprofile_utils.py`.
- Added `crypt_utils.py` and `tests/test_crypt_utils.py`.
- Added `crypto_utils.py` and `tests/test_crypto_utils.py`.
- Added `csv_utils.py` and `tests/test_csv_utils.py`.
- Added `ctypes_utils.py` and `tests/test_ctypes_utils.py`.
- Added `curses_utils.py` and `tests/test_curses_utils.py`.
- Added `data_utils.py` and `tests/test_data_utils.py`.
- Added `dataclasses_utils.py` and `tests/test_dataclasses_utils.py`.
- Added `datetime_utils.py` and `tests/test_datetime_utils.py`.
- Added `dbm_utils.py` and `tests/test_dbm_utils.py`.
- Added `decimal_utils.py` and `tests/test_decimal_utils.py`.
- Added `deprecation_utils.py` and `tests/test_deprecation_utils.py`.
- Added `dict_utils.py` and `tests/test_dict_utils.py`.
- Added `difflib_utils.py` and `tests/test_difflib_utils.py`.
- Added `html_parser_utils.py` and `tests/test_html_parser_utils.py`.
- Added `html_entities_utils.py` and `tests/test_html_entities_utils.py`.
- Added `dis_utils.py` and `tests/test_dis_utils.py`.
- Added `doctest_utils.py` and `tests/test_doctest_utils.py`.
- Added `duration_utils.py` and `tests/test_duration_utils.py`.
- Added `either_utils.py` and `tests/test_either_utils.py`.
- Added `email_utils.py` and `tests/test_email_utils.py`.
- Added `encodings_utils.py` and `tests/test_encodings_utils.py`.
- Added `ensurepip_utils.py` and `tests/test_ensurepip_utils.py`.
- Added `enum_utils.py` and `tests/test_enum_utils.py`.
- Added `env_utils.py` and `tests/test_env_utils.py`.
- Added `errno_utils.py` and `tests/test_errno_utils.py`.
- Added `exceptions_utils.py` and `tests/test_exceptions_utils.py`.
- Added `faulthandler_utils.py` and `tests/test_faulthandler_utils.py`.
- Added `fcntl_utils.py` and `tests/test_fcntl_utils.py`.
- Added `file_utils.py` and `tests/test_file_utils.py`.
- Added `filecmp_utils.py` and `tests/test_filecmp_utils.py`.
- Added `fileinput_utils.py` and `tests/test_fileinput_utils.py`.
- Added `fnmatch_utils.py` and `tests/test_fnmatch_utils.py`.
- Added `fractions_utils.py` and `tests/test_fractions_utils.py`.
- Added `ftplib_utils.py` and `tests/test_ftplib_utils.py`.
- Added `functools_utils.py` and `tests/test_functools_utils.py`.
- Added `gc_utils.py` and `tests/test_gc_utils.py`.
- Added `genericpath_utils.py` and `tests/test_genericpath_utils.py`.
- Added `getopt_utils.py` and `tests/test_getopt_utils.py`.
- Added `getpass_utils.py` and `tests/test_getpass_utils.py`.
- Added `gettext_utils.py` and `tests/test_gettext_utils.py`.
- Added `glob_utils.py` and `tests/test_glob_utils.py`.
- Added `graphlib_utils.py` and `tests/test_graphlib_utils.py`.
- Added `greeting_utils.py` and `tests/test_greeting_utils.py`.
- Added `grp_utils.py` and `tests/test_grp_utils.py`.
- Added `gzip_utils.py` and `tests/test_gzip_utils.py`.
- Added `hash_utils.py` and `tests/test_hash_utils.py`.
- Added `hashlib_utils.py` and `tests/test_hashlib_utils.py`.
- Added `heapq_utils.py` and `tests/test_heapq_utils.py`.
- Added `hmac_utils.py` and `tests/test_hmac_utils.py`.
- Added `html_utils.py` and `tests/test_html_utils.py`.
- Added `http_utils.py` and `tests/test_http_utils.py`.
- Added `id_utils.py` and `tests/test_id_utils.py`.
- Added `imaplib_utils.py` and `tests/test_imaplib_utils.py`.
- Added `imghdr_utils.py` and `tests/test_imghdr_utils.py`.
- Added `importlib_utils.py` and `tests/test_importlib_utils.py`.
- Added `ini_utils.py` and `tests/test_ini_utils.py`.
- Added `inspect_utils.py` and `tests/test_inspect_utils.py`.
- Added `interval_utils.py` and `tests/test_interval_utils.py`.
- Extended `interval_utils.py` with `interval_midpoint`, `interval_distance`, `interval_is_subset`, `interval_shift`, and `interval_symmetric_difference`, added `__all__`, and expanded the tests and README section to cover them.
- Added `io_utils.py` and `tests/test_io_utils.py`.
- Added `ip_utils.py` and `tests/test_ip_utils.py`.
- Added `ipaddress_utils.py` and `tests/test_ipaddress_utils.py`.
- Added `itertools_utils.py` and `tests/test_itertools_utils.py`.
- Added `json_utils.py` and `tests/test_json_utils.py`.
- Added `keyword_utils.py` and `tests/test_keyword_utils.py`.
- Added `linecache_utils.py` and `tests/test_linecache_utils.py`.
- Added `list_utils.py` and `tests/test_list_utils.py`.
- Added `locale_utils.py` and `tests/test_locale_utils.py`.
- Added `logging_utils.py` and `tests/test_logging_utils.py`.
- Added `lzma_utils.py` and `tests/test_lzma_utils.py`.
- Added `mailbox_utils.py` and `tests/test_mailbox_utils.py`.
- Added `mailcap_utils.py` and `tests/test_mailcap_utils.py`.
- Added `markdown_utils.py` and `tests/test_markdown_utils.py`.
- Added `marshal_utils.py` and `tests/test_marshal_utils.py`.
- Added `math_utils.py` and `tests/test_math_utils.py`.
- Added `maybe_utils.py` and `tests/test_maybe_utils.py`.
- Added `memoize_utils.py` and `tests/test_memoize_utils.py`.
- Added `mimetypes_utils.py` and `tests/test_mimetypes_utils.py`.
- Added `mmap_utils.py` and `tests/test_mmap_utils.py`.
- Added `modulefinder_utils.py` and `tests/test_modulefinder_utils.py`.
- Added `multiprocessing_utils.py` and `tests/test_multiprocessing_utils.py`.
- Added `netrc_utils.py` and `tests/test_netrc_utils.py`.
- Added `networking_utils.py` and `tests/test_networking_utils.py`.
- Added `nntplib_utils.py` and `tests/test_nntplib_utils.py`.
- Added `ntpath_utils.py` and `tests/test_ntpath_utils.py`.
- Added `nturl2path_utils.py` and `tests/test_nturl2path_utils.py`.
- Added `number_utils.py` and `tests/test_number_utils.py`.
- Added `numbers_utils.py` and `tests/test_numbers_utils.py`.
- Added `opcode_utils.py` and `tests/test_opcode_utils.py`.
- Added `operator_utils.py` and `tests/test_operator_utils.py`.
- Added `optparse_utils.py` and `tests/test_optparse_utils.py`.
- Added `os_utils.py` and `tests/test_os_utils.py`.
- Added `path_utils.py` and `tests/test_path_utils.py`.
- Added `pathlib_utils.py` and `tests/test_pathlib_utils.py`.
- Added `pattern_utils.py` and `tests/test_pattern_utils.py`.
- Added `pdb_utils.py` and `tests/test_pdb_utils.py`.
- Added `pickle_utils.py` and `tests/test_pickle_utils.py`.
- Added `pickletools_utils.py` and `tests/test_pickletools_utils.py`.
- Added `pipes_utils.py` and `tests/test_pipes_utils.py`.
- Added `pkgutil_utils.py` and `tests/test_pkgutil_utils.py`.
- Added `platform_utils.py` and `tests/test_platform_utils.py`.
- Added `plistlib_utils.py` and `tests/test_plistlib_utils.py`.
- Added `poplib_utils.py` and `tests/test_poplib_utils.py`.
- Added `posix_utils.py` and `tests/test_posix_utils.py`.
- Added `posixpath_utils.py` and `tests/test_posixpath_utils.py`.
- Added `pprint_utils.py` and `tests/test_pprint_utils.py`.
- Added `prime_utils.py` and `tests/test_prime_utils.py`.
- Added `priority_queue_utils.py` and `tests/test_priority_queue_utils.py`.
- Added `profile_utils.py` and `tests/test_profile_utils.py`.
- Added `prompt_utils.py` and `tests/test_prompt_utils.py`.
- Added `pstats_utils.py` and `tests/test_pstats_utils.py`.
- Added `pty_utils.py` and `tests/test_pty_utils.py`.
- Added `pwd_utils.py` and `tests/test_pwd_utils.py`.
- Added `py_compile_utils.py` and `tests/test_py_compile_utils.py`.
- Added `pyclbr_utils.py` and `tests/test_pyclbr_utils.py`.
- Added `pydoc_data_utils.py` and `tests/test_pydoc_data_utils.py`.
- Added `pydoc_utils.py` and `tests/test_pydoc_utils.py`.
- Added `pyexpat_utils.py` and `tests/test_pyexpat_utils.py`.
- Added `queue_utils.py` and `tests/test_queue_utils.py`.
- Added `quopri_utils.py` and `tests/test_quopri_utils.py`.
- Added `random_utils.py` and `tests/test_random_utils.py`.
- Added `rate_limiter_utils.py` and `tests/test_rate_limiter_utils.py`.
- Added `re_utils.py` and `tests/test_re_utils.py`.
- Added `readline_utils.py` and `tests/test_readline_utils.py`.
- Added `regex_utils.py` and `tests/test_regex_utils.py`.
- Added `reprlib_utils.py` and `tests/test_reprlib_utils.py`.
- Added `resource_utils.py` and `tests/test_resource_utils.py`.
- Added `retry_utils.py` and `tests/test_retry_utils.py`.
- Added `ring_buffer_utils.py` and `tests/test_ring_buffer_utils.py`.
- Added `rlcompleter_utils.py` and `tests/test_rlcompleter_utils.py`.
- Added `runpy_utils.py` and `tests/test_runpy_utils.py`.
- Added `sched_utils.py` and `tests/test_sched_utils.py`.
- Added `secrets_utils.py` and `tests/test_secrets_utils.py`.
- Added `select_utils.py` and `tests/test_select_utils.py`.
- Added `selectors_utils.py` and `tests/test_selectors_utils.py`.
- Added `semver_utils.py` and `tests/test_semver_utils.py`.
- Added `seq_utils.py` and `tests/test_seq_utils.py`.
- Added `set_utils.py` and `tests/test_set_utils.py`.
- Added `shelve_utils.py` and `tests/test_shelve_utils.py`.
- Added `shlex_utils.py` and `tests/test_shlex_utils.py`.
- Added `shutil_utils.py` and `tests/test_shutil_utils.py`.
- Added `signal_utils.py` and `tests/test_signal_utils.py`.
- Added `site_utils.py` and `tests/test_site_utils.py`.
- Added `slugify_utils.py` and `tests/test_slugify_utils.py`.
- Added `smtplib_utils.py` and `tests/test_smtplib_utils.py`.
- Added `sndhdr_utils.py` and `tests/test_sndhdr_utils.py`.
- Added `socket_utils.py` and `tests/test_socket_utils.py`.
- Added `socketserver_utils.py` and `tests/test_socketserver_utils.py`.
- Added `sort_utils.py` and `tests/test_sort_utils.py`.
- Added `spwd_utils.py` and `tests/test_spwd_utils.py`.
- Added `sqlite3_utils.py` and `tests/test_sqlite3_utils.py`.
- Added `sre_compile_utils.py` and `tests/test_sre_compile_utils.py`.
- Added `sre_constants_utils.py` and `tests/test_sre_constants_utils.py`.
- Added `sre_parse_utils.py` and `tests/test_sre_parse_utils.py`.
- Added `ssl_utils.py` and `tests/test_ssl_utils.py`.
- Added `stat_utils.py` and `tests/test_stat_utils.py`.
- Added `statistics_utils.py` and `tests/test_statistics_utils.py`.
- Added `string_utils.py` and `tests/test_string_utils.py`.
- Added `stringprep_utils.py` and `tests/test_stringprep_utils.py`.
- Added `struct_utils.py` and `tests/test_struct_utils.py`.
- Added `subprocess_utils.py` and `tests/test_subprocess_utils.py`.
- Added `sunau_utils.py` and `tests/test_sunau_utils.py`.
- Added `symtable_utils.py` and `tests/test_symtable_utils.py`.
- Added `sys_utils.py` and `tests/test_sys_utils.py`.
- Added `sysconfig_utils.py` and `tests/test_sysconfig_utils.py`.
- Added `syslog_utils.py` and `tests/test_syslog_utils.py`.
- Added `tabnanny_utils.py` and `tests/test_tabnanny_utils.py`.
- Added `tarfile_utils.py` and `tests/test_tarfile_utils.py`.
- Added `telnetlib_utils.py` and `tests/test_telnetlib_utils.py`.
- Added `temp_utils.py` and `tests/test_temp_utils.py`.
- Added `tempfile_utils.py` and `tests/test_tempfile_utils.py`.
- Added `template_utils.py` and `tests/test_template_utils.py`.
- Added `terminal_utils.py` and `tests/test_terminal_utils.py`.
- Added `termios_utils.py` and `tests/test_termios_utils.py`.
- Added `textwrap_utils.py` and `tests/test_textwrap_utils.py`.
- Added `this_utils.py` and `tests/test_this_utils.py`.
- Added `threading_utils.py` and `tests/test_threading_utils.py`.
- Added `time_utils.py` and `tests/test_time_utils.py`.
- Added `timeit_utils.py` and `tests/test_timeit_utils.py`.
- Added `timezone_utils.py` and `tests/test_timezone_utils.py`.
- Added `timing_utils.py` and `tests/test_timing_utils.py`.
- Added `token_utils.py` and `tests/test_token_utils.py`.
- Added `tokenize_utils.py` and `tests/test_tokenize_utils.py`.
- Added `tomllib_utils.py` and `tests/test_tomllib_utils.py`.
- Added `trace_utils.py` and `tests/test_trace_utils.py`.
- Added `traceback_utils.py` and `tests/test_traceback_utils.py`.
- Added `tracemalloc_utils.py` and `tests/test_tracemalloc_utils.py`.
- Added `tree_utils.py` and `tests/test_tree_utils.py`.
- Added `tty_utils.py` and `tests/test_tty_utils.py`.
- Added `type_utils.py` and `tests/test_type_utils.py`.
- Added `types_utils.py` and `tests/test_types_utils.py`.
- Added `typing_utils.py` and `tests/test_typing_utils.py`.
- Added `unicodedata_utils.py` and `tests/test_unicodedata_utils.py`.
- Added `unittest_utils.py` and `tests/test_unittest_utils.py`.
- Added `url_utils.py` and `tests/test_url_utils.py`.
- Added `urllib_utils.py` and `tests/test_urllib_utils.py`.
- Added `uu_utils.py` and `tests/test_uu_utils.py`.
- Added `uuid_utils.py` and `tests/test_uuid_utils.py`.
- Added `validation_utils.py` and `tests/test_validation_utils.py`.
- Added `venv_utils.py` and `tests/test_venv_utils.py`.
- Added `version_utils.py` and `tests/test_version_utils.py`.
- Added `warnings_utils.py` and `tests/test_warnings_utils.py`.
- Added `wave_utils.py` and `tests/test_wave_utils.py`.
- Added `weakref_utils.py` and `tests/test_weakref_utils.py`.
- Added `webbrowser_utils.py` and `tests/test_webbrowser_utils.py`.
- Added `wsgiref_utils.py` and `tests/test_wsgiref_utils.py`.
- Added `xdrlib_utils.py` and `tests/test_xdrlib_utils.py`.
- Added `xml_utils.py` and `tests/test_xml_utils.py`.
- Added `xmlrpc_utils.py` and `tests/test_xmlrpc_utils.py`.
- Added `zipapp_utils.py` and `tests/test_zipapp_utils.py`.
- Added `zipfile_utils.py` and `tests/test_zipfile_utils.py`.
- Added `zipimport_utils.py` and `tests/test_zipimport_utils.py`.
- Added `zlib_utils.py` and `tests/test_zlib_utils.py`.
- Added `zoneinfo_utils.py` and `tests/test_zoneinfo_utils.py`.

- Added `calculator.py` and `tests/test_calculator.py`.
- Added `shapes.py` and `tests/test_shapes.py`.
- Added `stats.py` and `tests/test_stats.py`.
- Added `strings.py` and `tests/test_strings.py`.
- Added `utils.py` and `tests/test_utils.py`.
- Added `config_schema.py` and `tests/test_config_schema.py`.
- Added `.pre-commit-config.yaml`.
- Added `CHANGELOG.md`.
- Added `.kilo/.gitignore`.
- Added `is_between(value, lower, upper, inclusive=True)` to `number_utils.py` with range membership testing and validation (raising `TypeError`/ValueError); updated `__all__`, README, and tests.

- Added `is_between(value, lower, upper, inclusive=True)` to `number_utils.py` with typed signature, `__all__` export, Google-style docstring, and validation raising `TypeError`/`ValueError` for range membership testing (inclusive by default). Added `TestIsBetween` to `tests/test_number_utils.py`. Updated `number_utils` module sections in `README.md`. Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`.

- Added `type_check_utils.py` and `tests/test_type_check_utils.py` with type checking helpers and tests. Updated `pyproject.toml`, `README.md`, and synchronized embedded copies.

## Latest Session (2026-10-28) — added combination and permutation to math_utils

The board held no task (bootstrap context). Verified repository health: all tests pass, `make lint` is clean, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `combination(n, k)` and `permutation(n, k)` to `math_utils.py` with full validation consistent with module conventions (`TypeError` for non-ints/bools, `ValueError` for negative values and `k > n`), exported via `__all__`, Google-style docstrings, and examples. Implementations use efficient iterative formulas without relying on heavy helpers.
- Added `TestCombination` and `TestPermutation` to `tests/test_math_utils.py` covering basic cases, edge values (k=0, k=n), large values, type errors, and value errors; updated imports to include the new functions.
- Updated `README.md` to document `combination` and `permutation` in both the file listing and module description.
- Refreshed embedded copies in `scaffold.sh` with `make refresh-scaffold` and verified with `python tools/refresh_scaffold.py --check`; all tests pass.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.
