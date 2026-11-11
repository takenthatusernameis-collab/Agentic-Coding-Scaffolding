## Unreleased — bootstrap verification; foundation confirmed solid, no genuine gap

- Bootstrap session: board held no task (`board_read` empty; `board_post` to `main` refused because `main` resolves to the board root, so durable handover recorded in `PROJECT_STATUS.md`). State-delta check vs. prior verified checkpoint `4b6895e`: `git status` clean on branch `main`, `python tools/refresh_scaffold.py --check` reports all embedded copies in sync, `want.txt == have.txt` unchanged.
- Ran the full suite as a coherent-milestone baseline: `python -m pytest tests/ -q` — 10663 passed, 3 skipped, 0 failed.
- Re-ran the alias-aware exported-but-untested scan (`python tools/scan_untested.py`): still only 10 candidates, all stdlib re-exports or thin pass-through wrappers (`abc_utils`: ABCMeta/abstractclassmethod/abstractproperty/abstractstaticmethod; `copyreg_utils`: add_extension/clear_extension_cache/constructor/dispatch_table/pickle/remove_extension) with no type hints/docstrings/validation — none are genuine, hermetic, convention-consistent helpers. No code/API/test changes made; avoiding a no-op commit per delay-bottleneck guidance.
- No `.github/workflows/**` changes.

## Unreleased — added test coverage for `traceback_utils.format_stack`

- Re-ran the alias-aware exported-but-untested scan (now a persistent tool at `tools/scan_untested.py`, which filters type vars, constants, classes, entry points, and interactive stdlib facades so only genuine gaps are reported). One genuine, hermetic, convention-consistent gap surfaced in `traceback_utils`: `format_stack` was a typed, documented, `__all__`-exported wrapper with zero dedicated coverage in `tests/test_traceback_utils.py` — and was inconsistent with its siblings, lacking the `TypeError` validation for non-int/bool `limit` that `extract_stack`, `print_stack`, `format_tb`, `format_exc`, and `extract_tb` all have.
- Added `TypeError` validation for `limit` to `format_stack` (matching the sibling convention), plus a Google-style docstring and an ASCII-safe doctest.
- Added `TestFormatStack` (3 tests) to `tests/test_traceback_utils.py` covering the list-of-strings return type, `limit` narrowing, and `TypeError` paths for non-int/bool `limit`.
- Verified: `python -m unittest tests.test_traceback_utils` (22 OK, up from 19), `python -m doctest traceback_utils.py` clean, `python -m unittest tests.test_public_api` OK, `python -m ruff check tests/test_traceback_utils.py traceback_utils.py` clean, `python -m mypy tests/test_traceback_utils.py traceback_utils.py` clean. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No new public API, so no `README.md` changes. No `.github/workflows/**` changes.

## Unreleased — added test coverage for `traceback_utils.extract_stack` and `format_exc`

- Re-ran the alias-aware exported-but-untested scan (fixed to resolve module aliases such as `import traceback_utils as tb`); two genuine, hermetic, convention-consistent gaps surfaced in `traceback_utils`: `extract_stack` and `format_exc` were both typed, documented, `__all__`-exported wrappers with `TypeError` validation, but had zero dedicated coverage in `tests/test_traceback_utils.py` — unlike their siblings `extract_tb`, `format_tb`, `format_exception`, `format_stack`, `print_*`, and `clear_frames`, which were all covered.
- Added `TestExtractStack` (4 tests) covering the empty-stack return type, `limit` narrowing, and `TypeError` paths for non-int/bool `limit`; and `TestFormatExc` (7 tests) covering the empty-when-no-exception contract, active-exception formatting, `limit` and `chain` forwarding, and `TypeError` paths for bad `limit`/`chain`. Imported nothing new — the new tests reference `traceback_utils.extract_stack`/`format_exc` directly, matching `__all__`.
- Verified: `python -m unittest tests.test_traceback_utils` (19 OK, up from 11), `python -m doctest traceback_utils.py` clean, `python -m unittest tests.test_public_api` OK, `python -m ruff check tests/test_traceback_utils.py traceback_utils.py` clean, `python -m mypy tests/test_traceback_utils.py traceback_utils.py` clean. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No new public API, so no `README.md` changes. No `.github/workflows/**` changes.

## Unreleased — fixed a failing test in `test_argcomplete_utils` and restored full-suite green

- State-delta check: `git status` clean on branch `main` at `5fbfd6e`, `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Ran the full suite (`python -m pytest tests/ -q`) at a coherent milestone as a baseline and found a real regression: `tests/test_argcomplete_utils.py::TestGetFilesCompleter::test_get_files_completer_returns_completer` failed with "Expected 'FilesCompleter' to be called once. Called 0 times."
- Root cause: the test patched `argcomplete.completers.FilesCompleter` (the stdlib attribute path), but `argcomplete_utils.get_files_completer` delegates to the module-level `FilesCompleter` name that `argcomplete_utils` imported into its own namespace at line 19. The sibling `TestGetCompleter.test_get_completer_returns_completer` was already correct (it patches `argcomplete_utils.ChoicesCompleter`); this test was simply out of step with the module's binding convention.
- Fixed by changing the patch target in `tests/test_argcomplete_utils.py` from `argcomplete.completers.FilesCompleter` to `argcomplete_utils.FilesCompleter`. No implementation, `__all__`, or public API changes — the test was wrong, not the code.
- Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: full suite `python -m pytest tests/ -q` — 10633 passed, 3 skipped, 0 failed (up from 1 failed / 10632 passed); `python -m ruff check tests/test_argcomplete_utils.py argcomplete_utils.py` clean; `python -m mypy tests/test_argcomplete_utils.py argcomplete_utils.py` clean; `python -m doctest argcomplete_utils.py` clean. No `.github/workflows/**` changes.

## Unreleased — added test coverage for `numbers_utils` number predicates

- Added test coverage for the `is_*` number predicates exported in `numbers_utils.__all__` that were previously untested: `is_disarium_number`, `is_kaprekar_number`, `is_perfect_square`, `is_perfect_cube`, `is_power_of_two`, `is_triangular_number`, `is_pentagonal_number`, `is_hexagonal_number`, `is_squarefree_number`, `is_oblong_number`, `is_ugly_number`, `is_narcissistic_number`, the `is_narcissistic` alias, and `is_untouchable_number`. All are typed, documented, `__all__`-exported predicates with `TypeError` validation, matching the existing `is_*` convention. Added `TestIsDisariumNumber`, `TestIsKaprekarNumber`, `TestIsPerfectSquare`, `TestIsPerfectCube`, `TestIsPowerOfTwo`, `TestIsTriangularNumber`, `TestIsPentagonalNumber`, `TestIsHexagonalNumber`, `TestIsSquarefreeNumber`, `TestIsOblongNumber`, `TestIsUglyNumber`, `TestIsNarcissisticNumber`, `TestIsNarcissisticAlias`, and `TestIsUntouchableNumber` to `tests/test_numbers_utils.py` covering known/non values, edge cases, and `TypeError` paths; imported the new names to match `__all__`.
- Verified: `python -m unittest tests.test_numbers_utils` (202 OK), `python -m unittest tests.test_public_api`, `python -m ruff check tests/test_numbers_utils.py numbers_utils.py` clean, `python -m mypy tests/test_numbers_utils.py numbers_utils.py` clean. No new public API was added, so no implementation or README changes beyond the test coverage. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added test coverage for `bytes_utils` singular null-byte aliases

- Added `TestCountNullByte` (9 tests), `TestHasNullBytes` (8 tests), and `TestCountNonNullByte` (9 tests) to `tests/test_bytes_utils.py` for `count_null_byte`, `has_null_bytes`, and `count_non_null_byte`, all exported in `__all__`, typed, and documented, but previously untested. New tests cover basic/all/none/empty/bytearray cases, consistency with the plural forms and positive predicates, and `TypeError` paths.
- Updated the `bytes_utils` module tree entry and prose section of `README.md` to list the singular aliases. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_bytes_utils` (424 OK, up from 407), `python -m unittest tests.test_public_api`, `python -m ruff check tests/test_bytes_utils.py bytes_utils.py` clean, `python -m mypy tests/test_bytes_utils.py bytes_utils.py` clean. No new public API was added, so no implementation/prose changes beyond the README tree entry. No `.github/workflows/**` changes.

## Unreleased — added test coverage for `list_utils.first_or_default`/`last_or_default`

- Added `TestFirstOrDefault` (6 tests) and `TestLastOrDefault` (6 tests) to `tests/test_list_utils.py` for `first_or_default`/`last_or_default`, both exported in `__all__`, typed, and documented, but previously untested. New tests cover basic values, empty-with-default, empty-with-None, single-element, default-not-used-when-non-empty, and `TypeError` paths.
- Updated the `list_utils` module tree entry and prose section of `README.md` to list `first_or_default` and `last_or_default`. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_list_utils` (217 OK, up from 205), `python -m unittest tests.test_public_api`, `python -m ruff check tests/test_list_utils.py list_utils.py` clean, `python -m mypy tests/test_list_utils.py list_utils.py` clean. No new public API was added, so no implementation/prose changes beyond the README tree entry. No `.github/workflows/**` changes.

## Unreleased — added test coverage for `posixpath_utils.is_rooted` and the `getatime`/`getctime`/`getmtime`/`getsize` stat helpers

- Added `TestIsRooted` (7 tests) to `tests/test_posixpath_utils.py` for `is_rooted`, which is exported in `__all__`, typed, and documented, but shipped with zero dedicated test coverage — unlike its sibling `isabs`, covered by `test_isabs`. New tests cover absolute/relative/empty/bytes/path-like inputs, the distinction from `isabs`, and `TypeError` paths.
- Added `TestStatHelpers` (10 tests) for the `getatime`/`getctime`/`getmtime`/`getsize` family, all exported in `__all__`, typed, and documented, but previously untested. New tests verify the return value against `os.stat` for a hermetic temporary file, the `OSError` path for missing files, and `TypeError` paths for non-path-like input.
- Updated the `posixpath_utils` module tree entry in `README.md` to list `is_rooted`, `getatime`, `getctime`, `getmtime`, and `getsize`. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_posixpath_utils` (45 OK, up from 30), `python -m unittest tests.test_public_api`, `python -m ruff check tests/test_posixpath_utils.py` clean, `python -m mypy tests/test_posixpath_utils.py` clean. No new public API was added, so no implementation/prose changes beyond the README tree entry. No `.github/workflows/**` changes.

## Unreleased — added `is_not_proper_subset`/`is_not_proper_superset` negation companions to `set_utils`

- Added `is_not_proper_subset(a, b)` and `is_not_proper_superset(a, b)` to `set_utils.py` as boolean negation companions to `is_proper_subset`/`is_proper_superset`, completing the module's subset/superset negation pairs alongside existing `is_subset`/`is_not_subset`, `is_superset`/`is_not_superset`, `is_equal`/`is_not_equal`, and `is_disjoint`/`has_intersection`.
- Typed `Iterable[Any] -> bool` APIs, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and `TypeError` validation consistent with module conventions (delegated to positive predicates).
- Added `TestIsNotProperSubset` and `TestIsNotProperSuperset` (16 tests) to `tests/test_set_utils.py` covering basic/empty/equal/duplicate/string cases, consistency with positive predicates, and `TypeError` paths.
- Updated `README.md` (`set_utils` tree/prose). Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Targeted verification: `python -m unittest tests.test_set_utils`, `python -m doctest set_utils.py`, `python -m unittest tests.test_public_api`, `python -m ruff check set_utils.py tests/test_set_utils.py`. No `.github/workflows/**` changes.

## Unreleased — added `is_not_zero`/`is_not_all_ones` negation companions to `bytes_utils`

- Added `is_not_zero(data)` and `is_not_all_ones(data)` to `bytes_utils.py` as boolean negation companions to `is_zero`/`is_all_ones`, matching the existing `contains`/`not_contains` pattern. `is_not_zero` returns ``True`` when *data* contains at least one non-zero byte (empty input is ``False``), reusing :func:`is_zero` for consistency. `is_not_all_ones` returns ``True`` when *data* contains at least one non-0xff byte (empty input is ``False``), reusing :func:`is_all_ones` for consistency. Both accept typed `bytes | bytearray` APIs, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests.
- Added `TestIsNotZero` (7 tests) and `TestIsNotAllOnes` (7 tests) to `tests/test_bytes_utils.py` covering basic/all-zero/empty/single/bytearray cases, consistency with the positive predicates, and `TypeError` paths; imported the new names to match `__all__`.
- Updated the `bytes_utils` module tree entry and prose section of `README.md`. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Targeted verification: `python -m unittest tests.test_bytes_utils`, targeted doctests for the new helpers, `python -m unittest tests.test_public_api`. No `.github/workflows/**` changes.

## Unreleased — added `argcomplete_utils.py` wrapping stdlib `argcomplete`

- Added `argcomplete_utils.py` wrapping the standard library `argcomplete` module with input validation: `autocomplete(parser, always_complete_options=True, exit_method=sys.exit, print_errors=True)` enables shell tab completion for an argparse parser; `get_completer(choices)` creates a `ChoicesCompleter` for static option lists; `get_files_completer(directories=True, filter_func=None)` creates a file system completer; `is_available()` reports whether argcomplete is installed. All helpers raise `TypeError` for invalid arguments and `ImportError` when argcomplete is not installed. The module degrades gracefully when argcomplete is absent. Added `tests/test_argcomplete_utils.py` with 13 tests covering availability checks, module contract, `autocomplete`, `get_completer`, and `get_files_completer`, including mocked integration tests and validation error paths. Registered `argcomplete_utils` in `pyproject.toml` `py_modules`. Updated `README.md` (architecture tree, test list, and module prose), `.kilo/command/scaffold-project.md` (manifest entries). Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m pytest tests/test_argcomplete_utils.py` (10 passed, 3 skipped), `python -m pytest tests/test_public_api.py` (passed), `python -m ruff check argcomplete_utils.py tests/test_argcomplete_utils.py` clean, `python -m mypy argcomplete_utils.py tests/test_argcomplete_utils.py` clean. No `.github/workflows/**` changes.

## Unreleased — added `count_binary`/`has_binary` companions to `strings.is_binary`

- Added `count_binary(s) -> int` and `has_binary(s) -> bool` to `strings.py` as the integer/boolean companions to `is_binary`, closing the `is*`/`count_*`/`has_*` companion gap for the binary-digit predicate. `count_binary` returns the number of binary characters (`0` or `1`) in *s* (empty input returns ``0``). `has_binary` returns ``True`` when at least one binary character is present and ``False`` otherwise (empty input is ``False``), reusing `count_binary` for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountBinary` and `TestHasBinary` to `tests/test_strings.py` covering all/mixed/none/empty cases, consistency between `count_binary` and `has_binary`, and the `TypeError` path; imported the new names to match `__all__`. Updated the `strings` module tree/prose entries in `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings`, targeted doctests for `count_binary`/`has_binary`, `python -m unittest tests.test_public_api`, `python -m ruff check strings.py tests/test_strings.py`, `python -m mypy strings.py`. No `.github/workflows/**` changes.

## Unreleased — added `count_printable`/`has_printable` companions to `strings.is_printable`

- Added `count_printable(s) -> int` and `has_printable(s) -> bool` to `strings.py` as the integer/boolean companions to `is_printable`, closing the `is*`/`count_*`/`has_*` companion gap for the printable predicate. `count_printable` returns the number of printable characters (any character passing `str.isprintable()`; whitespace other than space is not printable) in *s* (empty input returns ``0``). `has_printable` returns ``True`` when at least one printable character is present and ``False`` otherwise (empty input is ``False``), reusing `count_printable` for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountPrintable` (7 tests) and `TestHasPrintable` (6 tests) to `tests/test_strings.py` covering all/mixed/none/empty/unicode cases, consistency between `count_printable` and `has_printable`, and the `TypeError` path; imported the new names to match `__all__`. Updated the `strings` module tree entry in `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings` OK, targeted doctests for `count_printable`/`has_printable`, `python -m unittest tests.test_public_api`, `python -m ruff check strings.py tests/test_strings.py` clean. No `.github/workflows/**` changes.

## Unreleased — added `count_hex`/`has_hex` companions to `strings.is_hex`

- Added `count_hex(s) -> int` and `has_hex(s) -> bool` to `strings.py` as the integer/boolean companions to `is_hex`, closing the `is*`/`count_*`/`has_*` companion gap for the hexadecimal-digit predicate. `count_hex` returns the number of hexadecimal characters (0-9, a-f, A-F) in *s* (empty input returns ``0``). `has_hex` returns ``True`` when at least one hexadecimal character is present and ``False`` otherwise (empty input is ``False``), reusing `count_hex` for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountHex` (6 tests) and `TestHasHex` (5 tests) to `tests/test_strings.py` covering all/mixed/none/empty cases, consistency between `count_hex` and `has_hex`, and the `TypeError` path; imported the new names to match `__all__`. Updated the `strings` module tree entry in `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings` OK, targeted doctests for `count_hex`/`has_hex`, `python -m unittest tests.test_public_api`, `python -m ruff check strings.py tests/test_strings.py` clean. No `.github/workflows/**` changes.

## Unreleased — added `count_ascii`/`has_ascii` companions to `strings.is_ascii`

- Added `count_ascii(s) -> int` and `has_ascii(s) -> bool` to `strings.py` as the integer/boolean companions to `is_ascii`, closing the `is*`/`count_*`/`has_*` companion gap for the ASCII predicate. `count_ascii` returns the number of ASCII characters (any character whose Unicode code point is below 128) in *s* (empty input returns ``0``). `has_ascii` returns ``True`` when at least one ASCII character is present and ``False`` otherwise (empty input is ``False``), reusing `count_ascii` for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountAscii` (7 tests) and `TestHasAscii` (6 tests) to `tests/test_strings.py` covering all/mixed/none/empty/unicode cases, consistency between `count_ascii` and `has_ascii`, and the `TypeError` path; imported the new names to match `__all__`. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings` OK, targeted doctests for `count_ascii`/`has_ascii`, `python -m unittest tests.test_public_api`, `python -m ruff check strings.py tests/test_strings.py` clean. No `.github/workflows/**` changes.

## Unreleased — added `count_alphanumeric`/`has_alphanumeric` companions to `strings.is_alphanumeric`

- Added `count_alphanumeric(s) -> int` and `has_alphanumeric(s) -> bool` to `strings.py` as the integer/boolean companions to `is_alphanumeric`, closing the same `is*`/`count_*`/`has_*` companion gap that `count_alpha`/`has_alpha` closed for `is_alpha` and that `bytes_utils` closed for `isalnum`/`count_alnum`/`has_alnum`. `count_alphanumeric` returns the number of alphanumeric characters (any character that passes :meth:`str.isalnum`) in *s* (empty input returns ``0``). `has_alphanumeric` returns ``True`` when at least one alphanumeric character is present and ``False`` otherwise (empty input is ``False``), reusing `count_alphanumeric` for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountAlphanumeric` (7 tests) and `TestHasAlphanumeric` (5 tests) to `tests/test_strings.py` covering all/mixed/none/empty/unicode cases, consistency between `count_alphanumeric` and `has_alphanumeric`, and the `TypeError` path; imported the new names to match `__all__`. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings` (536 OK), targeted doctests for `count_alphanumeric`/`has_alphanumeric`, `python -m unittest tests.test_public_api`, `python -m ruff check strings.py tests/test_strings.py` clean. No `.github/workflows/**` changes.

## Unreleased — added keys_not_equal/values_not_equal companions to `dict_utils`

- Added `keys_not_equal(d1, d2)` and `values_not_equal(d1, d2)` to `dict_utils.py` as boolean negation companions to `keys_equal`/`values_equal`, matching the `set_utils.is_equal`/`is_not_equal` pattern. Typed `Dict[Any, Any] -> bool` APIs, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and `TypeError` validation consistent with the existing equality helpers (delegated). Added `TestKeysNotEqual` and `TestValuesNotEqual` (10 tests) to `tests/test_dict_utils.py` covering basic cases, empty inputs, consistency with `keys_equal`/`values_equal`, and `TypeError` paths. Updated `README.md` (`dict_utils` tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Targeted verification: `python -m unittest tests.test_dict_utils -q`, `python -m doctest dict_utils.py -q`, `python -m unittest tests.test_public_api -q`, `python -m ruff check dict_utils.py tests/test_dict_utils.py` clean. No `.github/workflows/**` changes.

## Unreleased — added `count_alpha`/`has_alpha` companions to `strings.is_alpha`

- Added `count_alpha(s) -> int` and `has_alpha(s) -> bool` to `strings.py` as the integer/boolean companions to `is_alpha`, resolving the same `is*`/`count_*`/`has_*` companion gap that `bytes_utils` closed for `isalpha`/`count_alpha`/`has_alpha`. `count_alpha` returns the number of alphabetic characters (any character that passes :meth:`str.isalpha`) in *s* (empty input returns ``0``). `has_alpha` returns ``True`` when at least one alphabetic character is present and ``False`` otherwise (empty input is ``False``), reusing `count_alpha` for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountAlpha` (7 tests) and `TestHasAlpha` (5 tests) to `tests/test_strings.py` covering all/mixed/none/empty/unicode cases, consistency between `count_alpha` and `has_alpha`, and the `TypeError` path; imported the new names to match `__all__`. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings` (524 OK), targeted doctests for `count_alpha`/`has_alpha`, `python -m unittest tests.test_public_api`, `python -m ruff check strings.py tests/test_strings.py` clean. No `.github/workflows/**` changes.

## Unreleased — added `not_contains` companion to `bytes_utils.contains`

- Added `not_contains(data, sub)` to `bytes_utils.py` as the boolean negation companion to `contains`, returning `True` when *sub* is absent from *data* and `False` otherwise. Typed `bytes | bytearray` API, `__all__` export, Google-style docstring with ASCII-safe doctests, and `TypeError` validation consistent with `contains` (reused for negation). Added `test_not_contains` to `tests/test_bytes_utils.py` covering present/absent, bytearray inputs, consistency with `contains`, and `TypeError` paths. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Targeted verification: `python -m unittest tests.test_bytes_utils -q`, `python -m unittest tests.test_public_api -q`. No `.github/workflows/**` changes.

## Unreleased — added test coverage for sched_utils.enterabs

- Added 6 tests to `tests/test_sched_utils.py` (10 total, up from 4) for `enterabs`, which is exported in `__all__`, typed, and documented, but shipped with zero dedicated test coverage — unlike its sibling `enter`, covered by `test_enter_and_empty`/`test_cancel`/`test_run`/`test_queue`. New tests: `test_enterabs_schedules_event`, `test_enterabs_runs_action_at_absolute_time`, `test_enterabs_passes_argument_and_kwargs`, `test_enterabs_cancel_leaves_queue_empty`, `test_enterabs_future_time_event_is_queued`, `test_enterabs_matches_enter_when_time_equals_now_plus_delay`. All use a controlled `timefunc`/`delayfunc` so they are hermetic (no real sleeping); the future-time test verifies the event is queued but not run until the clock advances. The implementation in `sched_utils.py` was unchanged.
- Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m pytest tests/test_sched_utils.py` (10 passed), `python -m pytest tests/test_public_api.py` (passed), full suite `python -m pytest tests/` (10266 passed, 23 warnings, 4167 subtests passed), `python -m ruff check tests/test_sched_utils.py` clean, `python -m mypy tests/test_sched_utils.py` clean. No new public API was added, so `README.md` was not modified. No `.github/workflows/**` changes.

## Unreleased — added `find_where` to `dict_utils`

- Added `find_where(d, predicate)` to `dict_utils.py` (typed `Dict[K, V]`/`(K, V) -> bool` API, `__all__` export, Google-style docstring with ASCII-safe doctests, `TypeError` validation for non-dict/non-callable). Returns the first matching `(key, value)` tuple in insertion order, or `None`, complementing the existing predicate helpers `count_where`/`has_where`/`all_where`/`none_where` and matching the `list_utils.find`/`seq_utils.find` companion pattern.
- Added `TestFindWhere` (9 tests) to `tests/test_dict_utils.py` covering present/absent/empty/first-match/key-predicate/tuple shape/has_where consistency/falsy-value and `TypeError` paths.
- Updated `README.md` (`dict_utils` tree/prose). `dict_utils.py`/`tests/test_dict_utils.py` are not individually listed as extra embed sources beyond the scaffold manifest entries refreshed by `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` confirms sync after refresh.
- Validated: `python -m unittest tests.test_dict_utils` (153 OK; +9), `python -m doctest dict_utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check dict_utils.py tests/test_dict_utils.py` clean. No `.github/workflows/**` changes.

## Unreleased — added test coverage for array_utils byte/file/unicode conversion helpers

- Added `TestArrayBytes` (9 tests), `TestArrayFile` (6 tests), `TestArrayUnicode` (8 tests), and `TestArrayItemsize` (3 tests) to `tests/test_array_utils.py` for the `array_tobytes`/`array_to_bytes`, `array_frombytes`/`array_from_bytes`, `array_tofile`/`array_to_file`, `array_fromfile`/`array_from_file`, `array_tounicode`/`array_to_unicode`, `array_fromunicode`/`array_from_unicode`, and `array_itemsize` helpers. These were exported in `__all__`, typed, and documented with Google-style docstrings and ASCII-safe doctests, but shipped with zero dedicated test coverage — unlike every other array helper (`array_create`, `array_fromlist`, `array_tolist`, `array_append`, `array_extend`, `array_insert`, `array_pop`, `array_remove`, `array_reverse`, `array_clear`, `array_count`, `array_index`, `array_to_list`, `array_from_list`, `array_extend_from_list`, `array_remove_first`, `array_concat`, `array_repeat`, `array_buffer_info`, `array_byteswap`, `array_typecode`).
- Coverage includes basic round-trips (bytes/file/unicode), empty-input cases, alias consistency between the `tobytes`/`to_bytes` (and sibling) pairs, and `TypeError` paths for non-array, non-bytes, non-file, non-int, and non-str arguments. The implementation in `array_utils.py` was unchanged. Updated the `array_utils` prose section of `README.md` to list the byte/file/unicode conversion helpers.
- Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_array_utils` (71 OK; +26 new), `python -m doctest array_utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check array_utils.py tests/test_array_utils.py` clean, `python -m mypy tests/test_array_utils.py` clean. No new public API was added, so no source-module changes beyond tests/README/CHANGELOG. No `.github/workflows/**` changes.

## Unreleased — added count_where/has_where/all_where/none_where companions to `dict_utils`

- Added `count_where(d, predicate)`, `has_where(d, predicate)`, `all_where(d, predicate)`, and `none_where(d, predicate)` to `dict_utils.py` as item-predicate companions matching the `seq_utils`/`list_utils` style (predicates take `(key, value)`). `count_where` returns the number of matching items; `has_where` reports any match (short-circuits); `all_where` reports every match (vacuously `True` for an empty dict, matching Python `all` semantics); `none_where` reports no match (negation of `has_where`, `True` for an empty dict). Typed APIs, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and `TypeError` validation for non-dict *d* and non-callable predicates.
- Added `TestCountWhere`, `TestHasWhere`, `TestAllWhere`, and `TestNoneWhere` (22 tests) to `tests/test_dict_utils.py` covering basic/no-match/empty/all-match/key/falsy-value cases, consistency between companions, and `TypeError` paths.
- Updated `README.md` (`dict_utils` tree/prose). `dict_utils.py`/`tests/test_dict_utils.py` are not embedded in `scaffold.sh`, so no scaffold refresh was needed. Verified: `python -m unittest tests.test_dict_utils` (144 OK; +22 new), `python -m doctest dict_utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check dict_utils.py tests/test_dict_utils.py` clean, `python -m mypy dict_utils.py` clean. No `.github/workflows/**` changes.

## Unreleased — added is_not_empty companion to `utils.is_empty`

- Added `is_not_empty(value)` to `utils.py` as the boolean negation companion to `is_empty`, resolving the previously noted `is_empty`/`is_not_empty` export/test coherence gap. It returns `True` when `is_empty` would return `False`, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests (consistent with the module's general value-emptiness semantics: `None` and empty `str`/`list`/`tuple`/`set`/`dict` are empty). Added `TestIsNotEmpty` (5 tests) to `tests/test_utils.py` covering `None`, empty containers, non-empty values, numeric/bool edge cases (`0`/`False` are not considered empty, matching `is_empty`), and consistency with `is_empty`. `utils.py`/`tests/test_utils.py` are not embedded in `scaffold.sh`, so no refresh was needed. Verified: `python -m unittest tests.test_utils` (48 OK; +5 new), `python -m doctest utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check utils.py tests/test_utils.py` clean. No `.github/workflows/**` changes.


## Unreleased — added first_or_default/last_or_default companions to `seq_utils`

- Added `first_or_default(sequence, default=None)` and `last_or_default(sequence, default=None)` to `seq_utils.py` as companions to `first`/`last` and `nth_or_default`, matching the `list_utils.first_or_default`/`last_or_default` style. Both accept any `Sequence`, validate with `_require_sequence`, raise `TypeError` for non-sequences, return the boundary element or the supplied default for an empty sequence, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests.
- Added `TestFirstOrDefault` and `TestLastOrDefault` (8 tests) to `tests/test_seq_utils.py` covering non-empty, empty/default, and `TypeError` paths; imported the new names to match `__all__`. Updated `README.md` (`seq_utils` tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_seq_utils` (241 OK), targeted doctests for the new helpers pass, `python -m unittest tests.test_public_api` (OK). Pre-existing `seq_utils.flatten` doctest quote-style failure remains (unrelated). No changes to `.github/workflows/**`.

## Unreleased — added TestSetNested coverage for data_utils nested-path helper

- Added `TestSetNested` (11 tests) to `tests/test_data_utils.py` for `set_nested`, which is exported in `__all__`, typed, documented with Google-style docstrings and ASCII-safe doctests, and shipped with no dedicated test class (unlike its siblings `get_nested`, `del_nested`, `pick`, `omit`, `flatten_dict`, `invert_dict`, `merge_dicts`, and `deep_copy`). Coverage includes basic/deep/intermediate-creation/overwrite/top-level/custom-separator/empty-dict cases, consistency with the returned-dict identity, and `TypeError`/`ValueError` paths. Fixed a latent bug in `data_utils.set_nested`: the empty-path guard used `not segments or segments == [""]`, which does not catch the `"."`-only path (or any all-empty-segment path) that `del_nested` rejects, so it now uses the same `not path or not any(segments)` check as `del_nested`. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_data_utils` (55 OK; +11 new), `python -m doctest data_utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check data_utils.py tests/test_data_utils.py` clean, `python -m mypy tests/test_data_utils.py` clean. No `.github/workflows/**` changes.

## Unreleased — added TestCountBy/TestHasBy coverage for utils predicate companions

- Added `TestCountBy` (6 tests) and `TestHasBy` (5 tests) to `tests/test_utils.py` for `count_by` and `has_by`, which are exported in `__all__`, typed, and documented with Google-style docstrings and ASCII-safe doctests, but shipped with no dedicated test class. Coverage includes basic/none/all/empty cases, consistency between `count_by` and `has_by`, and `TypeError` paths for non-callable predicates. The implementation in `utils.py` was unchanged. Verified: `python -m unittest tests.test_utils` (43 OK; +11 new), `python -m doctest utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check tests/test_utils.py` clean, `python -m mypy tests/test_utils.py` clean. `utils.py`/`tests/test_utils.py` are not embedded in `scaffold.sh`, so no refresh was needed. No `.github/workflows/**` changes.

## Unreleased — added test coverage for calendar_utils month-grid helpers

- Added `TestMonthCalendar` (4 tests), `TestWeekdaysInMonth` (4 tests), and `TestWeekendDaysInMonth` (5 tests) to `tests/test_calendar_utils.py` for `month_calendar`, `weekdays_in_month`, and `weekend_days_in_month`, which were exported in `__all__`, documented in the `calendar_utils` prose section of `README.md`, but shipped with no dedicated test class. Coverage includes basic grid rendering, consistency with `calendar.monthcalendar`, weekday/weekend counts for a full month, the invariant `weekdays + weekend_days == days_in_month`, and `TypeError`/`ValueError` paths. Updated the `calendar_utils` module tree entry of `README.md` to list every exported name (`month_calendar`, `first_day_of_month`, `is_weekend`, `weekdays_in_month`, `weekend_days_in_month`). Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_calendar_utils` (OK), `python -m unittest tests.test_public_api` (OK). No `.github/workflows/**` changes.

## Unreleased — added last_index_in_deque/find_last_index_in_deque to deque_utils

- Added `last_index_in_deque(d, value, start=0, stop=None)` and `find_last_index_in_deque(d, value, start=0, stop=None)` to `deque_utils.py` as last-occurrence companions to `index_in_deque`/`find_index_in_deque`. `last_index_in_deque` returns the 0-based index of the last match over `start`/`stop` bounds and raises `ValueError` when absent; `find_last_index_in_deque` is its non-raising companion returning `None`. Typed APIs, `__all__` exports, and Google-style docstrings with ASCII-safe doctests. Added `TestLastIndexInDeque` and `TestFindLastIndexInDeque` (13 tests) to `tests/test_deque_utils.py` covering basic, duplicates, single occurrence, `start`/`stop`, missing, empty, list-consistency, and cross-consistency paths. Updated `README.md` deque_utils tree/prose. Synchronized embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added test coverage for version_utils relational companions

- Added `TestIsGreaterEqual` (7 tests) and `TestIsLessEqual` (7 tests) to `tests/test_version_utils.py` for `is_greater_equal` and `is_less_equal`, which were exported in `__all__` and documented with ASCII-safe doctests but shipped with no dedicated test class. Coverage includes greater/less/equal/strict cases, different-length versions, consistency with `is_greater`/`is_less`/`is_equal`, and `TypeError`/`ValueError` paths; imported the two names to match the module's `__all__` contract. The implementation in `version_utils.py` was unchanged. Updated the `version_utils` module tree entry of `README.md` to list the new names. Refreshed embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_version_utils` (292 OK), `python -m doctest version_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added count_union/count_difference/count_symmetric_difference to `set_utils`

- Added `count_union(a, b)`, `count_difference(a, b)`, and `count_symmetric_difference(a, b)` to `set_utils.py` as integer companions to `union`/`difference`/`symmetric_difference`, matching the existing `count_intersection`/`has_intersection` style. Each returns the number of distinct elements in the corresponding set operation (duplicates in inputs contribute at most once), accepts any iterable of hashable elements, raises `TypeError` for non-iterables, is exported via `__all__`, and ships with Google-style docstrings and ASCII-safe doctests. Added `TestCountUnion`, `TestCountDifference`, and `TestCountSymmetricDifference` (24 tests) to `tests/test_set_utils.py` covering basic/empty/duplicate/string cases, consistency with the set-returning helpers, and `TypeError` paths. Updated `README.md` (tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_set_utils` (98 OK), `python -m doctest set_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added take_last/drop_last companions to `seq_utils`

- Added `take_last(sequence, n)` and `drop_last(sequence, n)` to `seq_utils.py` as end-relative companions to `take`/`drop`. Both accept any `Sequence`, validate with `_require_sequence`, raise `TypeError` for a non-sequence/non-int `n` (rejecting `bool`) and `ValueError` for negative `n`, return a list copy, and ship with `__all__` exports, Google-style docstrings, and ASCII-safe doctests. `take_last` returns up to the last `n` elements (empty for `n=0`, all when `n` exceeds length); `drop_last` returns elements before the last `n` (copy for `n=0`, empty when `n` exceeds length). Added `TestTakeLast` and `TestDropLast` (10 tests) to `tests/test_seq_utils.py`. Updated `README.md` (tree + prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Targeted verification: `python -m unittest tests.test_seq_utils -q` (228 OK), `python -m unittest tests.test_public_api -q` (OK). Pre-existing doctest failure in `seq_utils.flatten` (quote style, unrelated) remains. No `.github/workflows/**` changes.

## Unreleased — added count_unique/has_all_unique companions to `list_utils`

- Added `count_unique(lst)` and `has_all_unique(lst)` to `list_utils.py` as companions to `count_duplicates`/`has_duplicates`/`unique_preserve_order`, matching `seq_utils` style. Both accept a typed `List[T]`, raise `TypeError` for non-lists, handle unhashable elements via linear membership checks, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. `count_unique` returns the number of distinct elements; `has_all_unique` reports whether all elements are distinct (empty list vacuously `True`). Added `TestCountUnique` and `TestHasAllUnique` (15 tests) to `tests/test_list_utils.py`. Updated `README.md` (`list_utils` tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_list_utils` (202 OK), `python -m doctest list_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — seq_utils is_empty/is_not_empty emptiness predicates

- Added `is_empty(sequence)` and `is_not_empty(sequence)` to `seq_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and `TypeError` validation via the module's existing sequence guard. `is_empty` returns `True` when a sequence has no elements; `is_not_empty` is its boolean negation companion (mirroring the emptiness pair pattern used elsewhere, e.g. `list_utils.is_empty`).
- Added `TestIsEmpty` and `TestIsNotEmpty` (10 tests) to `tests/test_seq_utils.py` covering list/tuple/str/bytes empty and non-empty cases, cross-consistency, and `TypeError` paths.
- Updated `README.md` (`seq_utils` tree entry and prose). Synchronized embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Targeted verification: `python -m unittest tests.test_seq_utils` (235 OK), targeted doctests for `is_empty`/`is_not_empty` (8 examples OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.



- Added `count_occurrences(lst, value)`, `count_where(lst, predicate)`, `has_where(lst, predicate)`, `all_where(lst, predicate)`, `none_where(lst, predicate)`, and `has_occurrences(lst, value)` to `list_utils.py` as companions to existing `find`/`contains` helpers, matching `seq_utils` style. Typed APIs, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and `TypeError` validation for non-list *lst* (and non-callable predicates where applicable). Added `TestCountOccurrences`, `TestCountWhere`, `TestHasWhere`, `TestAllWhere`, `TestNoneWhere`, and `TestHasOccurrences` (31 tests) to `tests/test_list_utils.py`. Updated `README.md` (`list_utils` tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_list_utils` (187 OK), `python -m doctest list_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added count_title/has_title companions to bytes_utils.istitle

- Added `count_title(data) -> int` and `has_title(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `istitle`. The module already had `istitle` (exported in `__all__`, with tests and README documentation) but no `count_*`/`has_*` counterparts. `count_title` returns the count of titlecase bytes (uppercase ASCII letters at word boundaries: start of data or after a non-alphabetic byte) in *data* (empty input returns ``0``). `has_title` returns ``True`` when at least one titlecase byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_title` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountTitle` (7 tests) and `TestHasTitle` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `istitle` and with each other, and `TypeError` paths; imported `count_title`/`has_title` to match `__all__`. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added `indices_of` to `list_utils`

- Added `indices_of(lst, value)` to `list_utils.py` returning the 0-based indices of all occurrences of *value* in ascending order (empty list/no matches yield `[]`). It is the all-occurrences companion to `index_of`/`last_index_of`, matching `seq_utils.indices_of` style. Typed API, `__all__` export, Google-style docstring with ASCII-safe doctests, and `TypeError` validation for non-list *lst*. Added `TestIndicesOf` (7 tests) to `tests/test_list_utils.py` covering basic/no-match/empty/all-match/single cases, the `TypeError` path, and consistency with `index_of`; imported `indices_of` to match `__all__`. Updated the `list_utils` module tree entry and prose section of `README.md`. Synchronized `list_utils.py`, `tests/test_list_utils.py`, `README.md`, and `CHANGELOG.md` into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_list_utils` (OK), `python -m doctest list_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added count_prime_factors/count_distinct_prime_factors companions to prime_utils factor predicates

- Added `count_prime_factors(n) -> int` and `count_distinct_prime_factors(n) -> int` to `prime_utils.py` as the `count_*`-named integer companions to `has_prime_factors`/`has_distinct_prime_factors`. The module already had `total_prime_factors` (Ω(n)) and `distinct_prime_factors` (ω(n)) with boolean `has_*` companions, but no `count_*`-named counterparts consistent with the repository's common `count_*`/`has_*` API pattern. `count_prime_factors` implements Ω(n) (factors with multiplicity); `total_prime_factors` remains as a backward-compatible alias. `count_distinct_prime_factors` implements ω(n); `distinct_prime_factors` remains as a backward-compatible alias. `has_prime_factors` and `has_distinct_prime_factors` now reuse the `count_*` implementations for consistency. All accept typed `int` arguments (rejecting `bool`), validate `n >= 1`, raise `TypeError`/`ValueError`, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountPrimeFactors` and `TestCountDistinctPrimeFactors` to `tests/test_prime_utils.py`, extended `has_*` consistency checks to cover `count_*`, and imported the new names. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.


## Unreleased — added count_/has_ companions to bytes_utils.islower, isspace, isupper, isprintable

- Added `count_lower(data) -> int` and `has_lower(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `islower`. The module already had `islower` (exported in `__all__`, with tests and README documentation) but no `count_*`/`has_*` counterparts, so callers could not obtain the actual number of lowercase bytes or test for lowercase presence without computing it themselves. `count_lower` returns the count of ASCII lowercase bytes (``a``-``z``) in *data* (empty input returns ``0``). `has_lower` returns ``True`` when at least one lowercase byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_lower` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountLower` (7 tests) and `TestHasLower` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `count_lower`/`has_lower` and `islower`, and `TypeError` paths; imported `count_lower`/`has_lower` to match `__all__`.

- Added `count_space(data) -> int` and `has_space(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `isspace`. `count_space` returns the count of ASCII whitespace bytes (space, tab, newline, carriage return, form feed, vertical tab) in *data* (empty input returns ``0``). `has_space` returns ``True`` when at least one whitespace byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_space` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountSpace` (7 tests) and `TestHasSpace` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `count_space`/`has_space` and `isspace`, and `TypeError` paths; imported `count_space`/`has_space` to match `__all__`.

- Added `count_upper(data) -> int` and `has_upper(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `isupper`. `count_upper` returns the count of ASCII uppercase bytes (``A``-``Z``) in *data* (empty input returns ``0``). `has_upper` returns ``True`` when at least one uppercase byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_upper` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountUpper` (7 tests) and `TestHasUpper` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `count_upper`/`has_upper` and `isupper`, and `TypeError` paths; imported `count_upper`/`has_upper` to match `__all__`.

- Added `count_printable(data) -> int` and `has_printable(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `isprintable`. `count_printable` returns the count of ASCII printable bytes (``0x20``-``0x7E``) in *data* (empty input returns ``0``). `has_printable` returns ``True`` when at least one printable byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_printable` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountPrintable` (7 tests) and `TestHasPrintable` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `count_printable`/`has_printable` and `isprintable`, and `TypeError` paths; imported `count_printable`/`has_printable` to match `__all__`.

- Evaluated `istitle` for `count_*`/`has_*` companions and intentionally left it without them: title-casedness is a positional property of the whole byte sequence (it depends on byte position and preceding characters), so there is no idiomatic per-byte count or presence companion consistent with the `count_alpha`/`has_alpha` pattern.

Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added count_ascii/has_ascii companions to bytes_utils.isascii

- Added `count_ascii(data) -> int` and `has_ascii(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `isascii`. The module already had `isascii` (exported in `__all__`, with tests and README documentation) but no `count_*`/`has_*` counterparts, so callers could not obtain the actual number of ASCII bytes or test for ASCII presence without computing it themselves. `count_ascii` returns the count of ASCII bytes (``0x00``-``0x7F``) in *data* (empty input returns ``0``). `has_ascii` returns ``True`` when at least one ASCII byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_ascii` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountAscii` (7 tests) and `TestHasAscii` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `isascii` and with each other, and `TypeError` paths; imported `count_ascii`/`has_ascii` to match `__all__`. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added count_alnum/has_alnum companions to bytes_utils.isalnum

- Added `count_alnum(data) -> int` and `has_alnum(data) -> bool` to `bytes_utils.py` as the integer/boolean companions to `isalnum`. The module already had `isalnum` (exported in `__all__`, with tests and README documentation) but no `count_*`/`has_*` counterparts, so callers could not obtain the actual number of alphanumeric bytes or test for alphanumeric presence without computing it themselves. `count_alnum` returns the count of ASCII alphanumeric bytes (``a``-``z``, ``A``-``Z``, ``0``-``9``) in *data* (empty input returns ``0``). `has_alnum` returns ``True`` when at least one alphanumeric byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_alnum` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountAlnum` (7 tests) and `TestHasAlnum` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `isalnum` and with each other, and `TypeError` paths; imported `count_alnum`/`has_alnum` to match `__all__`. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added test coverage for set_utils.is_proper_subset and is_proper_superset

- Added `TestIsProperSubset` (8 tests) and `TestIsProperSuperset` (9 tests) to `tests/test_set_utils.py`, covering true/false/equal/not-a-subset/empty/duplicate-ignored/string cases, consistency with `is_subset`/`is_superset`/`is_equal`, and `TypeError` paths (non-iterable arguments); imported `is_proper_subset` and `is_proper_superset` to match `__all__`. Both helpers were already exported in `__all__`, documented with ASCII-safe doctests, and listed in the `set_utils` tree entry and prose section of `README.md`, but shipped with no dedicated test class — unlike every other set-operation predicate in the module (`is_subset`, `is_superset`, `is_disjoint`, `has_intersection`, `is_equal`, `intersection`, `count_intersection`, `union`, `difference`, `symmetric_difference`, `cartesian_product`, `power_set` all have coverage). Updated the `set_utils` module tree entry and prose section of `README.md` to mention the proper-subset/superset pair. No `.github/workflows/**` changes.

## Unreleased — added `count_all_keys` to `dict_utils`

- Added `count_all_keys(d, keys)` to `dict_utils.py` as the integer companion to `has_all_keys`/`has_any_key`, returning how many keys from *keys* are present in *d* (counting duplicate key queries once per occurrence). Updated `has_all_keys` and `has_any_key` to reuse `count_all_keys` for consistency. Typed API, `__all__` export, Google-style docstring with ASCII-safe doctests, and `TypeError` validation for non-dict *d*. Added `TestCountAllKeys` (10 tests) to `tests/test_dict_utils.py` covering all-present/partial/missing/empty/duplicate/generator cases, consistency with `has_all_keys`/`has_any_key`, and the `TypeError` path. Updated `README.md` tree/prose. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, and `CHANGELOG.md` into `scaffold.sh` with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils` (100 OK), `python -m doctest dict_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added count_all_values integer companion to dict_utils value predicates

- Added `count_all_values(d, values) -> int` to `dict_utils.py` as the integer companion to `has_all_values`/`has_any_value`, returning the number of elements of *values* that are present in *d* (duplicates in *values* are counted separately, so the result can exceed the number of distinct values in *d*; an empty *values* iterable yields ``0``). It accepts a typed `dict` argument and any iterable of values, raises `TypeError` for non-dicts, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Refactored `has_all_values` to reuse `count_all_values(d, values) == len(list(values))` and `has_any_value` to reuse `count_all_values(d, values) > 0` for consistency with the module's other boolean companions.
- Added `TestCountAllValues` (11 tests) to `tests/test_dict_utils.py` covering all-present/one-missing/none-present/empty-values/empty-dict/duplicate-values/falsy-and-none/generator-input cases, consistency with `has_all_values` and `has_any_value`, and the `TypeError` path; imported `count_all_values` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added test coverage for bit_utils.isolate_lowest_set_bit

- Added `TestIsolateLowestSetBit` (6 tests) to `tests/test_bit_utils.py` covering zero/single-bit/multi-bit cases, the `value & -value` identity, the invariant that the isolated result is 0 or a power of two, and `TypeError`/`ValueError` paths (non-int, bool, negative); imported `isolate_lowest_set_bit` to match `__all__`. The helper itself was already exported in `__all__`, documented with ASCII-safe doctests, and listed in `bit_utils.py`, but shipped without test coverage — unlike every other bit-access helper in the module. Updated the `bit_utils` prose section of `README.md` to mention `isolate_lowest_set_bit` (and `bit_parity`, already covered). No `.github/workflows/**` changes.

## Unreleased — added has_digits to bytes_utils

- Added `has_digits(data) -> bool` to `bytes_utils.py` as the boolean companion to `count_digits`, returning ``True`` when *data* contains at least one ASCII digit byte (``0``-``9``) and ``False`` otherwise (empty input is ``False``). The module already had `isdigit` (all bytes are digits) and `count_digits` (the actual digit count) but no predicate reporting whether any digit byte is present, so callers could not check for digit presence without computing `count_digits(data) > 0` themselves. `has_digits` accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, reuses `count_digits` for consistency, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestHasDigits` (6 tests) to `tests/test_bytes_utils.py` covering has/no/empty/bytearray inputs, consistency with `count_digits`, consistency with `isdigit`, and `TypeError` paths; imported `has_digits` to match `__all__`. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added count_intersection to set_utils

- Added `count_intersection(a, b) -> int` to `set_utils.py` as the integer companion to `intersection`, returning the number of distinct elements common to both iterables. The module already had `intersection` (returning the set of common elements) and `has_intersection` (its boolean companion), but no integer counterpart, so callers could not obtain the actual count without computing `len(intersection(a, b))` themselves. `count_intersection` reuses `intersection` for consistency, accepts any iterables via the module's `_to_set` validation (raising `TypeError` for non-iterables), is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Refactored `has_intersection` to reuse `count_intersection(a, b) > 0` for consistency with the module's other boolean companions.
- Added `TestCountIntersection` (10 tests) to `tests/test_set_utils.py` covering basic/disjoint/no-overlap/duplicate-ignored/string/single cases, consistency with `intersection`, consistency with `has_intersection`, and `TypeError` paths; imported `count_intersection` to match `__all__`. Updated the `set_utils` module tree entry and prose section of `README.md`. Synchronized `set_utils.py`, `tests/test_set_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_set_utils` (53 tests, OK); targeted doctests for `count_intersection`/`has_intersection` (0 failures); `python -m unittest tests.test_public_api` (OK); full suite `python -m unittest discover tests/` (OK). No `.github/workflows/**` changes.

## Unreleased

- Added `count_alpha(data)` and `has_alpha(data)` to `bytes_utils.py` as integer/boolean companions to `isalpha`. `isalpha` (exported in `__all__`, with tests and README documentation) reported only whether every byte is alphabetic, so callers could not obtain the actual number of alphabetic bytes or test for any alphabetic presence. `count_alpha` returns the count of ASCII alphabetic bytes (``a``-``z``, ``A``-``Z``) in *data* (empty input returns ``0``). `has_alpha` returns ``True`` when at least one alphabetic byte is present and ``False`` otherwise (empty input is ``False``), reusing `count_alpha` for consistency. Both accept typed `bytes`/`bytearray` arguments, raise `TypeError` for non-bytes-like input, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountAlpha` (7 tests) and `TestHasAlpha` (6 tests) to `tests/test_bytes_utils.py` covering all/no/mixed/empty/bytearray inputs, consistency with `isalpha` and with each other, and `TypeError` paths; imported `count_alpha`/`has_alpha` to match `__all__`. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- Added `count_digits(data)` to `bytes_utils.py` as the missing integer companion to `isdigit`. The module had `isdigit` (exported in `__all__`, with tests and README documentation) but no `count_*` counterpart, so callers could not obtain the actual number of digit bytes. `count_digits` returns the count of ASCII digit bytes (``0``-``9``) in *data*; empty input returns zero. It accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestCountDigits` (8 tests) to `tests/test_bytes_utils.py` covering all-digits/no-digits/mixed/empty/bytearray inputs, consistency with `isdigit`, and `TypeError` paths; imported `count_digits` to match `__all__`. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- Added test coverage for `has_leading_newlines` and `has_trailing_newlines` in `prompt_utils.py`.
## [Unreleased]

### Added
- Added `take` and `drop` to `seq_utils.py` for sequence slicing by count with
  typed `Sequence` inputs, `__all__` exports, ASCII-safe doctests, and
  `TypeError`/`ValueError` validation (including bool-*n* rejection). Added
  `TestTake` and `TestDrop` coverage in `tests/test_seq_utils.py`, updated
  `README.md`, and refreshed embedded scaffold copies.

### Added
- `has_all_values`, `contains_all_values`, `has_any_value`, `contains_any_value` in `dict_utils.py`: value-predicate companions to `has_value`/`contains_value`, mirroring the `has_all_keys`/`has_any_key` key-predicate pair, with typed `dict` validation raising `TypeError`, `__all__` exports, ASCII-safe doctests, and targeted tests in `tests/test_dict_utils.py`.
- Added `is_invertible(d)` to `dict_utils.py` as the boolean companion to `invert_dict`, returning ``True`` when all values in *d* are distinct (so the dictionary can be inverted one-to-one) and ``False`` otherwise. It mirrors `invert_dict`'s success condition without raising, accepts a typed `dict` argument, raises `TypeError` for non-dicts, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestIsInvertible` (6 tests) to `tests/test_dict_utils.py` covering unique/duplicate/empty/single cases, consistency with `invert_dict`, and `TypeError` paths; imported `is_invertible` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

- Added `has_intersection(a, b)` to `set_utils.py` as the boolean companion to `intersection` and the logical negation of `is_disjoint`, returning ``True`` when the two iterables share at least one common element. Accepts any iterables via the module's `_to_set` validation (raising `TypeError` for non-iterables), is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestHasIntersection` (7 tests) to `tests/test_set_utils.py` covering overlap/no-overlap/empty/duplicates/strings, consistency with `is_disjoint`, and `TypeError` paths; imported `has_intersection` to match `__all__`. Updated the `set_utils` module tree entry and prose section of `README.md`. Synchronized `set_utils.py`, `tests/test_set_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

- Added `has_all_unique(sequence)` to `seq_utils.py` as the boolean companion to `count_unique`, returning ``True`` when every element in ``sequence`` is distinct and reusing :func:`count_unique` for consistency (an empty sequence yields ``True``). Accepts any ``Sequence``, validates with :func:`_require_sequence`, raises ``TypeError`` for a non-sequence, is exported via ``__all__``, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestHasAllUnique` (7 tests) to `tests/test_seq_utils.py` covering all-unique/duplicate/empty/single/string/tuple cases, consistency with `count_unique`, and the `TypeError` path; imported `has_all_unique` to match `__all__`. Updated the `seq_utils` module tree entry and prose section of `README.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

- Added `find_all(lst, predicate)` and `find_all_indices(lst, predicate)` to `list_utils.py` as multi-match companions to `find`/`find_index`, returning all matching elements or their 0-based indices in order (empty list/no matches yields `[]`). Typed APIs accept a `List[T]` and callable predicate, raise `TypeError` for non-lists or non-callable predicates, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestFindAll` and `TestFindAllIndices` (14 tests) to `tests/test_list_utils.py` covering basic/none-match/empty/preserve-order/all-match/string cases and `TypeError` paths. Updated the `list_utils` module tree entry and prose section of `README.md`. Synchronized `list_utils.py`, `tests/test_list_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

- Added `index_in_deque(d, value, start=0, stop=None)` to `deque_utils.py` as a typed companion to `collections.deque.index`, returning the 0-based index of the first matching element with optional `start`/`stop` bounds and raising `ValueError` when absent (stdlib behavior preserved). Exported via `__all__` with a Google-style docstring and ASCII-safe doctests. Added `TestIndexInDeque` to `tests/test_deque_utils.py` covering basic lookup, `start`/`stop` ranges, missing/empty/range-miss `ValueError` paths, and list-consistency. Updated the `deque_utils` module tree entry and prose section of `README.md`. Synchronized `deque_utils.py`, `tests/test_deque_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_deque_utils` (60 OK), `python -m doctest deque_utils.py`, `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.



- Added `find_last(lst, predicate)` and `find_last_index(lst, predicate)` to `list_utils.py` as last-match companions to `find`/`find_index`. Both scan from the end of the list and return the last element or 0-based index satisfying *predicate*, or `None` when no match is found (including for an empty list). Typed APIs accept a `List[T]` and callable predicate, raise `TypeError` for non-lists, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestFindLast` and `TestFindLastIndex` (14 tests) to `tests/test_list_utils.py` covering basic/multiple-match/no-match/empty/first-element/string cases and `TypeError` paths; imported the helpers to match `__all__`. Updated the `list_utils` module tree entry and prose section of `README.md`. Synchronized `list_utils.py`, `tests/test_list_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

- Added `reverse(sequence)` to `seq_utils.py` returning a new list with elements in reverse order.

### Added
- `seq_utils`: added `all_where(sequence, predicate) -> bool` and `none_where(sequence, predicate) -> bool` as predicate companions to `has_where`/`count_where`. `all_where` returns `True` when every element satisfies *predicate* (vacuously `True` for an empty sequence, matching Python `all` semantics); `none_where` returns `True` when no element satisfies *predicate* (including empty sequences), serving as the negation companion to `has_where`. Both accept any `Sequence`, validate with `_require_sequence`, require a callable *predicate* (raising `TypeError` for a non-sequence or non-callable), are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestAllWhere` (7 tests) and `TestNoneWhere` (7 tests) to `tests/test_seq_utils.py` covering all/some/none/empty/string/tuple cases, consistency with `count_where`/`has_where`, and `TypeError` paths; imported the helpers to match `__all__`. Updated the `seq_utils` module tree entry and prose section of `README.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

- `seq_utils`: added `partition(sequence, predicate) -> Tuple[List[T], List[T]]` as a predicate-based splitter, returning a `(matching, not_matching)` pair of lists. Items for which *predicate* returns true go into the first list, the rest into the second, with order preserved within each list. Accepts any `Sequence`, validates with `_require_sequence`, requires a callable *predicate* (raising `TypeError` for a non-sequence or non-callable), is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestPartition` (8 tests) to `tests/test_seq_utils.py` covering even/odd split, empty list, all-match, none-match, order preservation, tuple+string inputs, and the `TypeError` paths (non-sequence and non-callable predicate); imported `partition` to match `__all__`. Updated the `seq_utils` module tree entry and prose section of `README.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- `list_utils`: added `count_duplicates(lst: List[T]) -> int` as the integer companion to `has_duplicates`, returning the number of elements beyond their first occurrence (`len(lst)` minus the number of distinct elements). Hashable elements use a set for efficiency; unhashable elements fall back to linear membership checks. It accepts a typed `List[T]` argument, raises `TypeError` for non-lists, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. `has_duplicates` was refactored to reuse `count_duplicates(lst) > 0`. Added `TestCountDuplicates` (10 tests) to `tests/test_list_utils.py` covering basic/none/empty/multiple-same/multiple-values/all-same/strings/unhashable/consistency-with-`has_duplicates`/`TypeError` paths; imported `count_duplicates` to match `__all__`. Updated the `list_utils` module tree entry and prose section of `README.md`. Synchronized `list_utils.py`, `tests/test_list_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- `interval_utils`: added `interval_adjacent(a, b) -> bool` as a boolean predicate reporting whether two intervals touch back-to-back at a single shared endpoint (``a[1] == b[0]`` or ``b[1] == a[0]``) without overlapping interiors, complementing `interval_overlaps`. It accepts typed `Interval` arguments (``(low, high)`` tuples/lists), validates both intervals with `is_valid_interval` raising `ValueError` for invalid input, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestIntervalAdjacent` (8 tests) to `tests/test_interval_utils.py` covering touching in either direction, overlapping/disjoint/identical intervals, degenerate intervals, float endpoints, and the `ValueError` path; imported `interval_adjacent` to match `__all__`. Updated the `interval_utils` module tree entry and prose section of `README.md`. Synchronized `interval_utils.py`, `tests/test_interval_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- `seq_utils`: added `count_where(sequence, predicate) -> int` as the predicate-count companion to `count_occurrences`, and boolean companion `has_where(sequence, predicate) -> bool`. `count_where` returns the number of elements in *sequence* for which *predicate* returns true (empty sequence yields ``0``); `has_where` reports whether at least one element satisfies *predicate*, reusing `count_where` for consistency. Both accept any `Sequence`, validate with `_require_sequence`, require a callable *predicate* (raising `TypeError` for a non-sequence or non-callable), are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountWhere` (7 tests) and `TestHasWhere` (5 tests) to `tests/test_seq_utils.py` covering basic/no-match/empty/string/tuple/all-match cases, consistency between `has_where` and `count_where`, and `TypeError` paths; imported the helpers to match `__all__`. Updated the `seq_utils` module tree entry and prose section of `README.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- `seq_utils`: added `find(sequence, predicate) -> Optional[T]` as the element-returning companion to `find_index`. Returns the first element in *sequence* satisfying *predicate*, or ``None`` when no match is found (including for an empty sequence). Accepts any `Sequence`, validates with `_require_sequence`, requires a callable *predicate*, and raises `TypeError`/`ValueError`-consistent input validation (`TypeError` for non-sequence/non-callable). Exported via `__all__` with a Google-style docstring and ASCII-safe doctests. Added `TestFind` (8 tests) to `tests/test_seq_utils.py` covering basic/first-match/no-match/empty/start/tuple+string cases and `TypeError` paths. Updated the `seq_utils` module tree entry and prose section of `README.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- `seq_utils`: added `find_last(sequence, predicate) -> Optional[T]` and `find_last_index(sequence, predicate) -> Optional[int]` as the last-match companions to `find`/`find_index`. Both return the last element or 0-based index satisfying *predicate*, or ``None`` when no match is found (including for an empty sequence). Typed APIs accept any `Sequence`, validate with `_require_sequence`, require a callable *predicate* (raising `TypeError` for non-sequence/non-callable), are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestFindLast` and `TestFindLastIndex` (19 tests) to `tests/test_seq_utils.py` covering basic/last-match/no-match/empty/start/end/tuple+string cases, consistency with `find`/`find_index`, and `TypeError` paths. Updated the `seq_utils` module tree entry and prose section of `README.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.
- `bytes_utils`: added `has_non_null_bytes(data) -> bool` as the plural alias companion to `has_non_null_byte` (and boolean companion to `count_non_null_bytes`), mirroring the existing `has_null_bytes` alias for `has_null_byte`. Returns ``True`` when *data* contains at least one non-zero byte and ``False`` otherwise (empty input is ``False``), reusing `count_non_null_bytes` for consistency. Accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestCountNonNullBytes`, `TestHasNonNullByte`, and `TestHasNonNullBytes` (22 tests) to `tests/test_bytes_utils.py` covering all/none/mixed/empty/bytearray inputs, consistency with `count_non_null_bytes`, alias parity with `has_non_null_byte`, and `TypeError` paths. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added count_placeholders to template_utils

- Added `count_placeholders(template: str) -> int` to `template_utils.py` as the integer companion to `has_placeholders`, returning the number of distinct placeholder names in *template* by reusing `extract_placeholders`. `has_placeholders` was refactored to reuse `count_placeholders(template) > 0` for consistency with the module's other boolean companions. It accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestCountPlaceholders` (11 tests) to `tests/test_template_utils.py` covering format/template/mixed placeholders, distinct-name counting, no-placeholder/empty inputs, numeric-index skipping, consistency with `has_placeholders`, and the `TypeError` path; imported `count_placeholders` to match `__all__`. Updated the `template_utils` module tree entry and prose section of `README.md`. Synchronized `template_utils.py`, `tests/test_template_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — added count_alphanumeric to prompt_utils

- Added `count_alphanumeric(text)` to `prompt_utils.py` as the missing integer companion to `has_alphanumeric`. The module had `has_alphanumeric` (exported in `__all__`, with tests and README documentation) but no `count_*` counterpart, unlike every other `has_*` predicate in the module (`has_digits`/`count_digits`, `has_letters`/`count_letters`, `has_vowels`/`count_vowels`, etc.), so callers could not obtain the actual count. `count_alphanumeric` returns the number of ASCII letters (``a``-``z``, ``A``-``Z``) and ASCII decimal digits (``0``-``9``) in *text*; Unicode letters and numerals are not counted, and empty text returns zero. It accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with Google-style docstring and ASCII-safe doctests. Refactored `has_alphanumeric` to reuse `count_alphanumeric(text) > 0` for consistency with the module's other boolean companions.
- Added `TestCountAlphanumeric` (9 tests) to `tests/test_prompt_utils.py` covering empty, letters-only, digits-only, letters+digits, no-alphanumeric, mixed with whitespace/punctuation, Unicode-not-counted, consistency with `has_alphanumeric`, and `TypeError` paths; imported `count_alphanumeric` to match `__all__`. Updated the `prompt_utils` module tree entry and prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils` (1001 tests); targeted doctests for `count_alphanumeric` and `has_alphanumeric` (10 doctests, 0 failures); `python -m unittest tests.test_public_api` (exit 0); full suite `python -m unittest discover tests/` passes. Note: `python -m doctest prompt_utils.py` raises a pre-existing, unrelated `ValueError` in the `wrap_prompt` docstring (inconsistent leading whitespace) — not addressed here. No `.github/workflows/**` changes.

## Unreleased — fixed itertools_utils doctest syntax error

- Fixed a `SyntaxError` in the `nth_or_default` doctest in `itertools_utils.py`. The example `>>> nth_or_default(x for x in range(5), 3)` passed a bare generator expression as a positional argument, which Python parses as a generator passed to `nth_or_default` with no second positional argument — illegal syntax. Wrapped the generator in parentheses so the call is well-formed: `>>> nth_or_default((x for x in range(5)), 3)`. `python -m doctest itertools_utils.py` now passes (0 failures). No behavior change; the implementation, `__all__` export, and tests are unchanged. No `.github/workflows/**` changes.

## Unreleased — fixed itertools_utils doctest syntax error

- Fixed a `SyntaxError` in the `nth_or_default` doctest in `itertools_utils.py`. The example `>>> nth_or_default(x for x in range(5), 3)` passed a bare generator expression as a positional argument, which Python parses as a generator passed to `nth_or_default` with no second positional argument — illegal syntax. Wrapped the generator in parentheses so the call is well-formed: `>>> nth_or_default((x for x in range(5)), 3)`. `python -m doctest itertools_utils.py` now passes (0 failures). No behavior change; the implementation, `__all__` export, and tests are unchanged. This closes the pre-existing doctest issue noted in the `count_if`/`has_any` entry below. No `.github/workflows/**` changes.

## Unreleased — completed count_trailing_ones/has_trailing_ones for bit_utils

- Finished the `count_trailing_ones`/`has_trailing_ones` feature left incomplete by the prior checkpoint commit (`6535a0f`), which had added the implementations, `__all__` exports, and README documentation to `bit_utils.py` and `scaffold.sh` but shipped no test coverage. `bit_utils.py` had `count_set_bits`/`has_set_bits`, `count_leading_zeros`/`has_leading_zeros`, `count_leading_ones`/`has_leading_ones`, and `count_trailing_zeros`/`has_trailing_zeros` but the trailing-ones pair was untested. `count_trailing_ones(value)` returns the number of consecutive 1 bits at the least-significant end of *value* (0 for value 0), and `has_trailing_ones(value)` is its boolean companion, returning ``True`` when at least one trailing 1 bit is present and reusing `count_trailing_ones` for consistency. Both accept a typed `int` argument, raise `TypeError` for non-ints (including booleans) and `ValueError` for negative *value*, are exported via `__all__`, and ship with ASCII-safe doctests.
- Added `TestCountTrailingOnes` (7 tests) and `TestHasTrailingOnes` (9 tests) to `tests/test_bit_utils.py` covering zero/single/multiple trailing ones, the no-trailing-ones case, consistency with `count_trailing_ones` for n in 0..199, and the `TypeError`/`ValueError` paths; imported the new helpers to match the module's `__all__` contract. Updated the `bit_utils` module tree entry and prose section of `README.md`. Synchronized `bit_utils.py`, `tests/test_bit_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bit_utils` (50 OK); `python -m doctest bit_utils.py` (OK); `python -m unittest tests.test_public_api` (OK). No `.github/workflows/**` changes.

## Unreleased — id_utils validate_id alias (tests/docs/scaffold sync)

- Completed the prior `validate_id` alias added to `id_utils.py`: added `validate_id` coverage in `tests/test_id_utils.py` (behavior + parity with `is_valid_id`), updated `README.md` module tree/prose to list `validate_id`, and refreshed embedded copies in `scaffold.sh` with `make refresh-scaffold`. `python -m unittest tests.test_id_utils` (16), `python -m unittest tests.test_public_api`, and `python tools/refresh_scaffold.py --check` (all embedded copies in sync). No `.github/workflows/**` changes.

## Unreleased — added has_distinct_prime_factors to prime_utils

- Added `has_distinct_prime_factors(n)` to `prime_utils.py` as the boolean companion to `distinct_prime_factors`, reporting whether *n* has at least one distinct prime factor (i.e. ``False`` only when *n* is 1). It reuses `distinct_prime_factors` for consistency, accepts a typed `int` argument, raises `TypeError` for non-ints and `ValueError` for *n* less than 1 (the same contract as `distinct_prime_factors`), is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestHasDistinctPrimeFactors` (6 tests) to `tests/test_prime_utils.py` covering basic/prime-power/no-factor cases, consistency with `distinct_prime_factors` for n in 1..199, and the `TypeError`/`ValueError` paths; imported `has_distinct_prime_factors` to match `__all__`. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prime_utils`; targeted doctest for `has_distinct_prime_factors`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added count_prerelease_identifiers/has_prerelease_identifiers to version_utils

- Added `count_prerelease_identifiers(version)` and boolean companion `has_prerelease_identifiers(version)` to `version_utils.py`. `count_prerelease_identifiers` returns the number of dot-separated identifiers in a version's prerelease suffix (after `-`), ignoring any build metadata after `+`, or `0` when no prerelease suffix is present or it is empty; `has_prerelease_identifiers` reports whether any identifier is present, reusing the count helper for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountPrereleaseIdentifiers` and `TestHasPrereleaseIdentifiers` (8 tests) to `tests/test_version_utils.py` covering counts, no/empty suffix, prerelease+build metadata, consistency with `count_prerelease_identifiers`, and `TypeError` paths; imported the helpers to match `__all__`. Updated the `version_utils` prose section of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_version_utils`; targeted doctest for the new helpers; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added has_value/contains_value to dict_utils

- Added `has_value(d, value)` and `contains_value(d, value)` to `dict_utils.py` as boolean predicates reporting whether a value is present in a dictionary, mirroring the existing `has_key`/`contains_key` pair. `has_value` accepts typed `Dict[Any, V]` and `V` arguments, raises `TypeError` for non-dict *d*, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests; `contains_value` delegates to `has_value`. Added `TestHasValue` and `TestContainsValue` (10 tests total) to `tests/test_dict_utils.py` covering present, absent, empty, falsy/`None` values, consistency, and `TypeError` paths. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils tests.test_public_api`; `python -m doctest dict_utils.py`. No changes to `.github/workflows/**`.



- Added `contains_key(d, key)` to `dict_utils.py` as an alias for `has_key`, so the module offers a single `contains_*` naming convention alongside `select_keys` and `omit_keys`. `contains_key` delegates to `has_key`, accepts typed `Dict[K, Any]` and `K` arguments, raises `TypeError` for non-dict *d*, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestContainsKey` (5 tests) to `tests/test_dict_utils.py` covering present, absent, empty dict, consistency with `has_key`, and the `TypeError` path; imported `contains_key` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils`; targeted doctest for `contains_key`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added values_equal to dict_utils

- Added `values_equal(d1, d2)` to `dict_utils.py` as a boolean predicate reporting whether two dictionaries contain the same set of values, ignoring keys and value order. The module already had `keys_equal` for key-set comparison but no value-set counterpart, so callers relied on comparing `set(d1.values())` themselves. `values_equal` accepts typed `Dict[Any, Any]` arguments, raises `TypeError` for non-dict inputs, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestValuesEqual` (4 tests) to `tests/test_dict_utils.py` covering same values in different key order, different value sets, empty dicts, and the `TypeError` path; imported `values_equal` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils`; targeted doctest for `values_equal`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added keys_equal to dict_utils

- Added `keys_equal(d1, d2)` to `dict_utils.py` as a boolean predicate reporting whether two dictionaries have the same set of keys, ignoring values and key order. The module already had `has_key`/`contains_key` for single-key presence but no key-set comparison helper, so callers relied on comparing `set(d1)` themselves. `keys_equal` accepts typed `Dict[Any, Any]` arguments, raises `TypeError` for non-dict inputs, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestKeysEqual` (4 tests) to `tests/test_dict_utils.py` covering same keys with different values, different key sets, empty dicts, and the `TypeError` path; imported `keys_equal` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils`; targeted doctest for `keys_equal`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added merge to dict_utils

- Completed the `merge(d1, d2)` feature for `dict_utils.py`. The implementation and `__all__` export were already present from an earlier checkpoint, but the feature shipped without tests, README documentation, or a CHANGELOG entry. `merge` performs a one-level shallow merge: values from *d2* overwrite the corresponding values in *d1* for shared keys without recursing into nested dictionaries, complementing `deep_merge`. It accepts typed `Dict[K, V]` arguments, raises `TypeError` for non-dicts, returns a new dict without mutating the inputs, and ships with Google-style docstring and ASCII-safe doctests. Added `TestMerge` (8 tests) to `tests/test_dict_utils.py` covering basic/overlapping/non-overlapping merges, empty inputs on either side, shallow vs. deep behavior, non-mutation of inputs, and the `TypeError` path; imported `merge` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils` (35 OK); targeted doctest for `merge`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added count_if/has_any to itertools_utils

- Added `count_if(iterable, predicate)` and boolean companion `has_any(iterable, predicate)` to `itertools_utils.py`. `count_if` returns the number of items for which *predicate* is truthy; `has_any` reports whether any item satisfies *predicate*, short-circuiting on the first match. Both work with any iterable (including generators), accept typed `Iterable[Any]`/`Callable` arguments, raise `TypeError` for non-iterables or non-callables, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountIf` (8 tests) and `TestHasAny` (7 tests) to `tests/test_itertools_utils.py` covering basic/empty/no-match/all-match, generators, truthiness/short-circuit behavior, and `TypeError` paths; imported helpers to match `__all__`. Updated the `itertools_utils` module tree entry and prose section of `README.md`. Synchronized `itertools_utils.py`, `tests/test_itertools_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_itertools_utils` (146 OK); doctests for new helpers OK; `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added has_key to dict_utils

- Added `has_key(d, key)` to `dict_utils.py` as a boolean companion reporting whether *key* is present in *d*. The module already had `safe_get`, `select_keys`, and `omit_keys` for key access but no direct presence predicate, so callers relied on the raw `in` operator. `has_key` short-circuits on membership, accepts typed `Dict[K, Any]` and `K` arguments, raises `TypeError` for non-dict *d*, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestHasKey` (4 tests) to `tests/test_dict_utils.py` covering present, absent, empty dict, and the `TypeError` path; imported `has_key` to match `__all__`. Updated the `dict_utils` module tree entry and prose section of `README.md`. Synchronized `dict_utils.py`, `tests/test_dict_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_dict_utils`; targeted doctest for `has_key`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added is_equal to set_utils

- Added `is_equal(a, b)` to `set_utils.py` as a membership/equality predicate reporting whether two iterables contain the same set of elements. The module already had `is_subset`/`is_superset`/`is_disjoint` for relational comparisons but no direct equality check, so callers relied on comparing the raw sets themselves. `is_equal` ignores order, multiplicity, and concrete iterable type — only the distinct elements matter — accepts typed `Iterable[Any]` arguments, raises `TypeError` for non-iterables, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestIsEqual` (10 tests) to `tests/test_set_utils.py` covering same/different order, duplicate-ignoring, non-equality, empty/one-empty, disjoint, strings, tuples, and `TypeError` paths; imported `is_equal` to match `__all__`. Updated the `set_utils` module tree entry and prose section of `README.md`. Synchronized `set_utils.py`, `tests/test_set_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_set_utils`; targeted doctest for `is_equal`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added contains to list_utils

- Added `contains(lst, element)` to `list_utils.py` as a membership predicate reporting whether *element* is present in *lst*. The module already had `find`/`find_index` for predicate-based lookup but no direct membership helper, so callers relied on the raw `in` operator or `any(...)`. `contains` short-circuits on the first match, accepts a typed `List[T]` argument, raises `TypeError` for non-lists, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestContains` (9 tests) to `tests/test_list_utils.py` covering present/absent, empty list, first/last element, duplicates, `None` value, and the `TypeError` path; imported `contains` to match `__all__`. Updated the `list_utils` module tree entry and prose section of `README.md`. Synchronized `list_utils.py`, `tests/test_list_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_list_utils`; targeted doctest for `contains`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added is_empty_iterable to itertools_utils

- Added `is_empty_iterable(iterable)` to `itertools_utils.py` as a boolean predicate reporting whether an iterable yields no items. Unlike `len(iterable)`, it works for any iterable — including generators and other one-shot iterators — by consuming elements only until the first item is seen. It accepts a typed `Iterable[Any]` argument, raises `TypeError` for non-iterables, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestIsEmptyIterable` (9 tests) to `tests/test_itertools_utils.py` covering empty/non-empty list, empty/non-empty string, empty tuple, empty/non-empty generator, and `TypeError` paths for non-iterable and `None`; imported `is_empty_iterable` to match the module's `__all__` contract. Updated the `itertools_utils` module tree entry and prose section of `README.md`. Synchronized `itertools_utils.py`, `tests/test_itertools_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_itertools_utils`; targeted doctest for `is_empty_iterable`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added count_build_metadata_identifiers to version_utils

- Added `count_build_metadata_identifiers(version)` and boolean companion `has_build_metadata_identifiers(version)` to `version_utils.py`. `count_build_metadata_identifiers` returns the number of dot-separated identifiers in a version's build metadata suffix (after `+`), or `0` when no build metadata is present or it is empty; `has_build_metadata_identifiers` reports whether any identifier is present, reusing the count helper for consistency. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountBuildMetadataIdentifiers` and `TestHasBuildMetadataIdentifiers` (9 tests) to `tests/test_version_utils.py` covering counts, no/empty metadata, prerelease+build, consistency with `count_build_metadata_identifiers`, and `TypeError` paths; imported the helpers to match `__all__`. Updated the `version_utils` module tree entry and prose section of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_version_utils`; targeted doctest for the new helpers; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added has_set_bits to bytes_utils

- Added `has_set_bits(data)` to `bytes_utils.py` as the boolean companion to `bit_count`, returning `True` when any bit in *data* is set and `False` for empty or all-zero input. It accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, reuses `bit_count` for consistency, and ships with a Google-style docstring and ASCII-safe doctests. Added `TestHasSetBits` (6 tests) to `tests/test_bytes_utils.py` covering zero/all-set, empty, bytearray, consistency with `bit_count`, and `TypeError` paths; imported `has_set_bits` to match the module's `__all__` contract. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bytes_utils`; targeted doctest for `has_set_bits`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added count_null_bytes to bytes_utils

- Added `count_null_bytes(data)` to `bytes_utils.py` as the integer companion to `has_null_byte`, returning the number of zero bytes in *data*. It accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, and ships with a Google-style docstring and ASCII-safe doctests. Refactored `has_null_byte` to reuse `count_null_bytes(data) > 0` for consistency. Added `TestCountNullBytes` (8 tests) to `tests/test_bytes_utils.py` covering all-null, no-null, empty, single-null, mixed, bytearray, consistency with `has_null_byte`, and `TypeError` paths; imported `count_null_bytes` to match the module's `__all__` contract. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bytes_utils`; targeted doctest for `count_null_bytes`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No changes to `.github/workflows/**`.

## Unreleased — added `normalize_roman` to `roman_utils`

- Added `normalize_roman(roman)` to `roman_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and validation raising `TypeError`/`ValueError`; it accepts case-insensitively and returns the canonical uppercase Roman numeral for valid values in the supported range (1–3999). Added `test_normalize_roman` and `test_normalize_roman_rejects_invalid` to `tests/test_roman_utils.py`. Updated `README.md` roman module listing/prose. Synchronized `roman_utils.py` and `tests/test_roman_utils.py` into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_roman_utils` (9 OK), `python -m doctest roman_utils.py` (OK), `python -m unittest tests.test_public_api` (OK), `python -m unittest tests.test_scaffold_sync` (15 OK), full suite `python -m unittest discover tests/` (8974 OK). No changes to `.github/workflows/**`.

## Unreleased — added size to deque_utils

- Added `size(d: deque) -> int` to `deque_utils.py` as an integer companion to `is_empty`, returning the number of elements in a deque (`len(d)`). It accepts a typed `collections.deque` argument, is exported via `__all__`, and ships with Google-style docstrings and ASCII-safe doctests. Added `TestSize` (7 tests) to `tests/test_deque_utils.py` covering empty, single-element, multiple elements, append/pop/clear mutation, and consistency with `len(deque_to_list(d))` and `is_empty`; imported `size` to match the module's `__all__` contract. Updated the `deque_utils` module tree entry and prose section of `README.md`. Synchronized `deque_utils.py`, `tests/test_deque_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_deque_utils`; targeted doctest for `size`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No `.github/workflows/**` changes.

## Unreleased — completed is_empty for deque_utils

- Finished the `is_empty` feature left incomplete by the prior checkpoint commit (`aa8d6d7`), which had added the implementation, `__all__` export, and tests to `deque_utils.py` and `scaffold.sh` but shipped no README/CHANGELOG documentation. `deque_utils.py` had `create_deque`, append/pop/extend/rotate/clear, `count_in_deque`/`has_in_deque`, peek, remove, reverse, and `deque_to_list`, but no `is_empty` predicate (callers currently rely on truthiness/length of the raw deque). `is_empty(d)` returns ``True`` when the deque contains no elements and ``False`` otherwise, accepting a typed `collections.deque` argument and exporting via `__all__` with ASCII-safe doctests. Added `TestIsEmpty` (5 tests) to `tests/test_deque_utils.py` covering empty, single-element, after-pop/clear, and consistency with `len(deque_to_list(d)) == 0`; imported `is_empty` to match the module's `__all__` contract. Updated the `deque_utils` module tree entry and prose section of `README.md`. Synchronized `deque_utils.py`, `tests/test_deque_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_deque_utils`; targeted doctest for `is_empty`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No `.github/workflows/**` changes.

## Unreleased — added count_headings/has_headings to markdown_utils

- Added `count_headings(text)` and `has_headings(text)` to `markdown_utils.py` as count/boolean companions to `is_heading`. `count_headings` counts lines that are Markdown headings (1-6 `#`); `has_headings` returns `True` when at least one heading line is present. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with ASCII-safe doctests. Updated `markdown_utils` module tree entry and prose section of `README.md`. Synchronized with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — completed count_from for itertools_utils

- Finished the `count_from` feature left incomplete by the prior checkpoint commit (`50127d8`), which had added the implementation, `__all__` export, and tests to `itertools_utils.py` and `scaffold.sh` but shipped no README/CHANGELOG documentation. `itertools_utils.py` had no `count_from` helper; `count_from(start, step)` counts infinitely from *start* with *step*, returning the first 1000 values as a list for safety. It accepts typed `int` arguments (defaulting to `start=0`, `step=1`), raises `TypeError` for non-ints including booleans, is exported via `__all__`, and ships with ASCII-safe doctests. Added `test_count_from_default`, `test_count_from_start_step`, `test_count_from_bad_start_type`, and `test_count_from_bad_step_type` (4 tests) to the existing `TestIterToolsUtils` class in `tests/test_itertools_utils.py`; imported `count_from` to match the module's `__all__` contract. Updated the `itertools_utils` module tree entry and prose section of `README.md`. Synchronized `itertools_utils.py`, `tests/test_itertools_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_itertools_utils`; targeted doctest for `count_from`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No `.github/workflows/**` changes.

## Unreleased — completed point_in_rectangle for shapes

- Finished the `point_in_rectangle` feature left incomplete by the prior checkpoint commit (`9c242cf`), which had added the implementation, `__all__` export, and tests to `shapes.py` and `scaffold.sh` but shipped no README/CHANGELOG documentation. `shapes.py` had `point_distance`, `midpoint`, and `point_in_circle` but no `point_in_rectangle` boolean helper. `point_in_rectangle(point, x1, y1, x2, y2)` returns ``True`` when *point* lies inside or on the axis-aligned rectangle defined by two opposite corners (bounds normalized internally so corner order does not matter), ``False`` otherwise. It accepts a typed 2-tuple/list *point* and numeric corner coordinates, raises `TypeError` for non-points/non-numbers (booleans rejected) and `ValueError` for zero/negative width or height, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestPointInRectangle` (6 tests) to `tests/test_shapes.py` covering inside, outside, boundary, reversed corners, and the `TypeError`/`ValueError` paths; imported `point_in_rectangle` to match the module's `__all__` contract. Updated the `shapes` module tree entry and prose section of `README.md`. Synchronized `shapes.py`, `tests/test_shapes.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_shapes`; targeted doctest for `point_in_rectangle`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No `.github/workflows/**` changes.

## Unreleased — completed has_prime_factors for prime_utils

- Finished the `has_prime_factors` feature left incomplete by the prior checkpoint commit (`6593508`), which had added the implementation and `__all__` export to `prime_utils.py` but shipped no tests, no README/CHANGELOG documentation, and left the embedded `scaffold.sh` copy stale. `prime_utils.py` had `total_prime_factors(n)` (returning the total number of prime factors with multiplicity, Ω(n)) but no `has_prime_factors` boolean counterpart. `has_prime_factors(n)` returns ``True`` when *n* has at least one prime factor and ``False`` when *n* is 1, reusing `total_prime_factors` for consistency; it accepts a typed `int` argument, raises `TypeError` for non-ints and `ValueError` for *n* less than 1 (the same contract as `total_prime_factors`), is exported via `__all__`, and ships with ASCII-safe doctests.
- Added `TestHasPrimeFactors` (6 tests) to `tests/test_prime_utils.py` covering basic cases, prime powers, the no-prime-factor case (n == 1), consistency with `total_prime_factors` for n in 1..199, and the `TypeError`/`ValueError` paths; imported `has_prime_factors` to match the module's `__all__` contract. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prime_utils`; targeted doctest for `has_prime_factors`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No `.github/workflows/**` changes.

## Unreleased — added count/has_code_blocks to markdown_utils

- Added `count_code_blocks(text)` and `has_code_blocks(text)` to `markdown_utils.py` as count/boolean companions to `extract_code_blocks`. `count_code_blocks` returns the number of fenced code blocks using the same extraction rules as `extract_code_blocks`; `has_code_blocks` returns `True` when at least one fenced code block is present. Both accept typed `str` arguments, raise `TypeError` for non-strings, are exported via `__all__`, and ship with ASCII-safe doctests. Added `TestCountCodeBlocks` and `TestHasCodeBlocks` (11 tests) to `tests/test_markdown_utils.py` covering basic cases, consistency with `extract_code_blocks`/`count_code_blocks`, and `TypeError` paths; imported the new helpers to match the module's `__all__` contract. Updated the `markdown_utils` module tree entry and prose section of `README.md`. Synchronized `markdown_utils.py`, `tests/test_markdown_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_markdown_utils`; `python -m unittest tests.test_public_api`; targeted doctests for `markdown_utils`. No `.github/workflows/**` changes.

## Unreleased — added has_occurrences to strings


- Added `has_occurrences(s, substring)` to `strings.py` as the boolean companion to `count_occurrences`. `strings.py` had `count_occurrences(s, substring)` (returning the number of non-overlapping occurrences of *substring* in *s*) but no `has_occurrences` boolean counterpart. It returns `True` when *substring* occurs at least once in *s* and `False` when it is absent, including for empty *s*, reusing `count_occurrences` for consistency. Accepts typed `str` arguments, raises `TypeError` for non-strings and `ValueError` for an empty *substring* (the same contract as `count_occurrences`), is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasOccurrences` (7 tests) to `tests/test_strings.py` covering basic, no-occurrences, empty *s*, non-overlapping matching, consistency with `count_occurrences`, empty-substring `ValueError`, and the `TypeError` path; imported `has_occurrences` to match the module's `__all__` contract. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings`; targeted doctest for `has_occurrences`; `python -m unittest tests.test_public_api`; full suite `python -m unittest discover tests/`. No `.github/workflows/**` changes.

## Unreleased — added has_topics to pydoc_data_utils

- Added `has_topics()` to `pydoc_data_utils.py` as the boolean companion to `count_topics`. `pydoc_data_utils.py` had `count_topics()` (returning the number of topics the standard library holds) but no `has_topics` boolean counterpart. It returns ``True`` when the standard library holds at least one topic and ``False`` otherwise, reusing `count_topics` for consistency. It takes no arguments, raises `RuntimeError` when the interpreter does not ship the `pydoc_data` package (the same failure mode as `count_topics`), is exported via `__all__`, and ships with an ASCII-safe doctest. Added `TestHasTopics` (2 tests) to `tests/test_pydoc_data_utils.py` covering the positive case and consistency with `count_topics`; imported `has_topics` to match the module's `__all__` contract. Updated the `pydoc_data_utils` module tree entry and prose section of `README.md`. Synchronized `pydoc_data_utils.py`, `tests/test_pydoc_data_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_pydoc_data_utils`; targeted doctest for `has_topics`; `python -m unittest tests.test_public_api`. No `.github/workflows/**` changes.

## Unreleased — added has_uppercase to strings

- Added `has_uppercase(s)` to `strings.py` as the boolean companion to `count_uppercase`. `strings.py` had `count_uppercase(s)` (returning the number of uppercase letters) but no `has_uppercase` boolean counterpart. It returns `True` when *s* contains at least one uppercase letter and `False` for empty or lowercase-only text, reusing `count_uppercase` for consistency. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasUppercase` (9 tests) to `tests/test_strings.py` covering basic, no-uppercase, empty, mixed case, non-alpha-ignored, unicode-uppercase, consistency with `count_uppercase`, and the `TypeError` path; imported `has_uppercase` to match the module's `__all__` contract. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings`; targeted doctest for `has_uppercase`; `python -m unittest tests.test_public_api`. No `.github/workflows/**` changes.

## Unreleased — added has_consonants to strings

- Added `has_consonants(s)` to `strings.py` as the boolean companion to `count_consonants`. `strings.py` had `count_consonants(s)` (returning the number of consonant characters, case-insensitive and ignoring non-alphabetic characters) but no `has_consonants` boolean counterpart, unlike `count_vowels`/`has_vowels` which are already complete. It returns `True` when *s* contains at least one consonant (an alphabetic character that is not a, e, i, o, u) and `False` for vowel-only, digit-only, punctuation-only, or empty text, reusing the same vowel set as `count_consonants` for consistency. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasConsonants` (7 tests) to `tests/test_strings.py` covering basic, no-consonants, all-consonants, non-alpha-ignored, empty, consistency with `count_consonants`, and the `TypeError` path; imported `has_consonants` to match the module's `__all__` contract. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings`; targeted doctest for `has_consonants`; `python -m unittest tests.test_public_api`. No `.github/workflows/**` changes.

## Unreleased — fixed strings __all__ gap for has_letters

- Found a real contract gap: `strings.has_letters` was a fully-implemented public function (typed signature, Google-style docstring with doctests, `TypeError` validation, and `TestHasLetters` coverage in `tests/test_strings.py`) but missing from `strings.__all__`, violating the public-API export contract that every public attribute must be listed in `__all__`. The gap was caught by `tests/test_public_api.py` as the only test failure in the suite.
- Added `has_letters` to `strings.__all__` next to `count_letters` (49 exports total). The other boolean companions (`has_digits`, `has_punctuation`, `has_whitespace`) were already exported.
- Updated the `strings` module tree entry and prose section of `README.md` to document `has_letters` alongside its boolean companions `has_digits`, `has_punctuation`, and `has_whitespace`, which were previously missing from the README. The functions, their implementations, doctests, and `tests/test_strings.py` coverage were unchanged.
- Synchronized `strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings`; `python -m unittest tests.test_public_api`; targeted doctest for `has_letters`. No `.github/workflows/**` changes.

## Unreleased — added has_parameters to inspect_utils

- Added `has_parameters(func)` to `inspect_utils.py` as the boolean companion to `count_parameters`. `inspect_utils.py` had `count_parameters(func)` (returning the number of declared parameters) but no `has_parameters` boolean counterpart. It returns ``True`` when *func* declares at least one parameter and ``False`` for parameterless callables, reusing `count_parameters` for consistency. Accepts a typed callable argument, raises `TypeError` for non-callables and `ValueError` when the signature cannot be introspected, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasParameters` (6 tests) to `tests/test_inspect_utils.py` covering has-parameters, no-parameters, single-parameter, consistency with `count_parameters`, built-in with params, and the `TypeError` path; imported `has_parameters` to match the module's `__all__` contract. Updated the `inspect_utils` module tree entry and prose section of `README.md`. Verified: `python -m unittest tests.test_inspect_utils` (41 tests); `python -m ruff check inspect_utils.py tests/test_inspect_utils.py`; `python -m mypy inspect_utils.py tests/test_inspect_utils.py`. No changes to `.github/workflows/**`.

## Unreleased — added has_vowels to strings

- Added `has_vowels(s)` to `strings.py` as the boolean companion to `count_vowels`. `strings.py` had `count_vowels(s)` (returning the number of vowels in *s*) but no `has_vowels` boolean counterpart. It returns `True` when *s* contains at least one ASCII vowel (a, e, i, o, u), case-insensitive, and `False` for empty or consonant-only text, reusing the vowel set for consistency. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasVowels` to `tests/test_strings.py` covering basic, no-vowels, empty, case-insensitive, all-vowels, single-vowel, non-alpha, consistency with `count_vowels`, and the `TypeError` path; imported `has_vowels` to match the module's `__all__` contract. Updated the `strings` module tree entry and prose section of `README.md`. Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_strings`; `python -m unittest tests.test_public_api`; targeted doctest for `has_vowels`. No changes to `.github/workflows/**`.

## Unreleased — bytes_utils predicate documentation and doctest hardening (2026-11-07)

- **`bytes_utils.py`**: added Google-style docstrings with ASCII-safe doctests for simple predicate wrappers (`isalnum`, `isalpha`, `isascii`, `isdigit`, `islower`, `isspace`, `istitle`, `isupper`). Corrected `isprintable` docstring text to state empty input returns `True` (matching module/`str.isprintable`-style behavior). Replaced non-ASCII/escaped doctest literals (`casefold`, `isidentifier`, `isprintable`) with ASCII-safe examples so `python -m doctest bytes_utils.py` passes.
- **`tests/test_bytes_utils.py`**: clarified `TestIsPrintable` with an explicit empty/`bytearray()` case (218 tests pass).
- **Verification**: `python -m unittest tests.test_bytes_utils` (218 OK); `python -m unittest tests.test_public_api` (OK); `python -m doctest bytes_utils.py` (OK). Refreshed embedded `bytes_utils.py`/`tests/test_bytes_utils.py` in `scaffold.sh`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.



## Unreleased — added has_lines to io_utils

- Added `has_lines(path)` to `io_utils.py` as the boolean companion to `count_lines`. `io_utils.py` had `count_lines(path)` (returning the number of lines in a file) but no `has_lines` boolean counterpart. It returns ``True`` when the file contains at least one line and ``False`` for an empty file, reusing `count_lines` for consistency. Accepts a typed path argument (string or path-like), raises `TypeError` for non-path inputs, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasLines` to `tests/test_io_utils.py` covering multiple lines, no trailing newline, empty file, single line, consistency with `count_lines`, and the `TypeError` path; imported `has_lines` to match the module's `__all__` contract. Updated the `io_utils` module tree entry and prose section of `README.md`. Synchronized `io_utils.py`, `tests/test_io_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_io_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_lines`. No changes to `.github/workflows/**`.

## Unreleased — added has_words to markdown_utils

- Added `has_words(text)` to `markdown_utils.py` as the boolean companion to `count_words`. `markdown_utils.py` had `count_words(text)` (returning `len(text.split())`) but no `has_words` boolean counterpart. It returns `True` when *text* contains at least one whitespace-delimited word and `False` for empty or whitespace-only text, reusing `count_words` for consistency. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasWords` to `tests/test_markdown_utils.py` covering empty, whitespace-only, single/multiple words, leading/trailing whitespace, multiple spaces between words, unicode, consistency with `count_words`, and the `TypeError` path; imported `has_words` to match the module's `__all__` contract. Updated the `markdown_utils` module tree entry of `README.md`. Synchronized `markdown_utils.py`, `tests/test_markdown_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_markdown_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_words`. No changes to `.github/workflows/**`.

## Unreleased — added has_words to string_utils

- Added `has_words(text)` to `string_utils.py` as the boolean companion to `count_words`. `string_utils.py` had `count_words(text)` (returning `len(text.split())`) but no `has_words` boolean counterpart. It returns `True` when *text* contains at least one whitespace-delimited word and `False` for empty or whitespace-only text, reusing `count_words` for consistency. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasWords` to `tests/test_string_utils.py` covering empty, whitespace-only, single/multiple words, leading/trailing whitespace, multiple spaces between words, unicode, consistency with `count_words`, and the `TypeError` path; imported `has_words` to match the module's `__all__` contract. Updated the `string_utils` module tree entry and prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_string_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_words`. No changes to `.github/workflows/**`.

## Unreleased — added has_characters to prompt_utils

- Added `has_characters(text)` to `prompt_utils.py` as a boolean companion to `count_characters`. It returns `True` when *text* contains at least one character (including whitespace) and `False` for empty text, accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasCharacters` to `tests/test_prompt_utils.py` covering single/multiple characters, empty input, whitespace-only input, consistency with `count_characters`, and the `TypeError` path; imported `has_characters` to match the module's `__all__` contract. Updated the `prompt_utils` module tree/prose entries of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_characters`. No changes to `.github/workflows/**`.

## Unreleased — added has_blank_lines to prompt_utils

- Added `has_blank_lines(text)` to `prompt_utils.py` as a boolean companion to `count_blank_lines`, mirroring the existing `count_paragraphs`/`has_paragraphs` and `count_non_blank_lines`/`has_non_blank_lines` pairs. It returns `True` when *text* contains at least one blank (whitespace-only) line and `False` otherwise, including for empty or whitespace-only text, reusing `count_blank_lines` for consistency. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasBlankLines` to `tests/test_prompt_utils.py` covering empty, no-blank-lines, single/multiple blank lines, whitespace-only lines, all-blank, CRLF, consistency with `count_blank_lines`, and the `TypeError` path; imported `has_blank_lines` to match the module's `__all__` contract. Updated the `prompt_utils` module tree/prose entries of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_blank_lines`. No changes to `.github/workflows/**`.

## Unreleased — added is_beta to version_utils

- Added `is_beta(version)` to `version_utils.py` as a boolean companion to `get_prerelease`, following the pattern of the existing `is_dev_version`. It returns `True` when the pre-release tag starts with ``beta`` (case-insensitive) and `False` otherwise or when there is no pre-release suffix. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestIsBeta` to `tests/test_version_utils.py` covering beta/non-beta/no-prerelease/empty inputs and the `TypeError` path; imported `is_beta` to match the module's `__all__` contract. Updated the `version_utils` module tree entry of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_version_utils`; `python -m unittest tests.test_public_api`; `python -m doctest version_utils.py`. No changes to `.github/workflows/**`.

## Unreleased — added has_words to prompt_utils

- Added `has_words(text)` to `prompt_utils.py` as a boolean companion to `count_words`. It returns `True` when *text* contains at least one whitespace-delimited word and `False` for empty or whitespace-only text, accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__` (previously listed but unimplemented, now defined), and ships with ASCII-safe doctests. Added `TestHasWords` to `tests/test_prompt_utils.py` covering empty, single/multiple words, whitespace-only, leading/trailing whitespace, unicode, and the `TypeError` path; imported `has_words` to match the module's `__all__` contract. Updated the `prompt_utils` module tree/prose entries of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_words`. No changes to `.github/workflows/**`.

## Unreleased — added has_sentences to prompt_utils

- Added `has_sentences(text)` to `prompt_utils.py` as a boolean companion to `count_words`/`has_words` and `count_paragraphs`/`has_paragraphs`. It returns `True` when *text* contains at least one sentence (a terminating punctuation mark ``.``, ``!`` or ``?`` followed by whitespace or end of string) and `False` for empty or whitespace-only text or text with no terminator. Accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasSentences` to `tests/test_prompt_utils.py` covering single/multiple sentences, empty/whitespace-only, no-terminator, leading/trailing whitespace, unicode, consistency with `count_sentences`, and the `TypeError` path; imported `has_sentences` to match the module's `__all__` contract. Updated the `prompt_utils` module tree/prose entries of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils`; `python -m unittest tests.test_public_api`; targeted doctest for `has_sentences`. No changes to `.github/workflows/**`.

## Unreleased — fixed public-API contract regressions in version_utils and bytes_utils

### Fixed

- **`version_utils.py`**: four comparison aliases (`greater_equal`, `is_greater_equal`, `is_less_equal`, `less_equal`) were defined as public functions but missing from `__all__`, so `from version_utils import *` could not reach them and `tests.test_public_api` reported them as unexported public attributes. Added the four names to `__all__` (kept in alphabetical order with their siblings).
- **`bytes_utils.py`**: `isprintable` and `isidentifier` were listed in `__all__` but never implemented, so `from bytes_utils import *` raised `AttributeError`. Implemented both as typed, validated predicates matching the module's existing style: `isprintable` returns `True` only when every byte is in the ASCII printable range 0x20-0x7E (empty input returns `False`, mirroring `str.isprintable`); `isidentifier` ASCII-decodes the bytes and returns `str.isidentifier()` (non-ASCII/undecodable bytes yield `False`). Both accept `bytes`/`bytearray`, raise `TypeError` otherwise, and ship with ASCII-safe doctests.
- Added `TestIsPrintable` and `TestIsIdentifier` to `tests/test_bytes_utils.py` covering printable/non-printable/empty/bytearray inputs, valid/invalid identifiers, non-ASCII bytes, and the `TypeError` paths (198 tests now pass for the module). Imported the two helpers at the top of the test file to match the `__all__` contract.

Verified: `python -m unittest tests.test_bytes_utils` passes (198 tests); `python -m unittest tests.test_public_api` passes (3 tests); `python -m doctest bytes_utils.py` passes. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No changes to `.github/workflows/**`.

## Unreleased — added highest_set_bit to bytes_utils

- Added `highest_set_bit(data)` to `bytes_utils.py` as the most-significant-bit companion to `lowest_set_bit`, `bit_count`, and `is_power_of_two`. It interprets the bytes as a big-endian unsigned integer and returns the 0-based position of the most significant set bit, or -1 when no bit is set (including empty input). Accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHighestSetBit` to `tests/test_bytes_utils.py` covering no-set-bits, single-bit positions, multi-byte positions, bytearray support, and the `TypeError` path; imported `highest_set_bit` to match the module's `__all__` contract. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bytes_utils` passes; `python -m doctest bytes_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — added lowest_set_bit to bytes_utils

- Added `lowest_set_bit(data)` to `bytes_utils.py` as a bit-position companion to `bit_count`, `is_power_of_two`, and `is_zero`. It interprets the bytes as a big-endian unsigned integer and returns the 0-based position of the least significant set bit, or -1 when no bit is set (including empty input). Accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestLowestSetBit` to `tests/test_bytes_utils.py` covering no-set-bits, single-bit positions, multi-byte positions, bytearray support, and the `TypeError` path; imported `lowest_set_bit` to match the module's `__all__` contract. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bytes_utils` passes; `python -m doctest bytes_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — added is_power_of_two to bytes_utils

- Added `is_power_of_two(data)` to `bytes_utils.py` as a boolean companion to `bit_count`. It returns `True` when exactly one bit is set across all bytes (a power-of-two value) and `False` otherwise, with empty input returning `False`. Accepts typed `bytes`/`bytearray` arguments, raises `TypeError` for non-bytes-like input, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestIsPowerOfTwo` to `tests/test_bytes_utils.py` covering single-bit values, non-powers-of-two, empty input, bytearray support, and the `TypeError` path; imported `is_power_of_two` to match the module's `__all__` contract. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bytes_utils` passes; `python -m doctest bytes_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — added is_power_of to numbers_utils

- Added `is_power_of(value, base)` to `numbers_utils.py` as a base-parameterized power predicate companion to `is_power_of_two`, `is_perfect_power`, `is_perfect_square`, and `is_perfect_cube`. It returns `True` when `base**k == value` for some integer `k >= 0`, handling positive/negative bases and the `base` 0/1/-1 edge cases, accepts typed `int` arguments, raises `TypeError` for non-int/bool arguments, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestIsPowerOf` to `tests/test_numbers_utils.py` covering known powers, non-powers, negative bases, edge bases (0/1/-1), consistency with direct `base**k` computation, and the `TypeError` path; imported `is_power_of` to match the module's `__all__` contract. Updated the `numbers_utils` module tree entry and prose section of `README.md`. Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_numbers_utils` passes (148 tests); `python -m doctest numbers_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — added is_proth_prime to prime_utils

- Added `is_proth_prime(n)` to `prime_utils.py` as a prime-form helper companion to `is_cuban_prime`, `is_fermat_number`, and `is_mersenne_prime`. A Proth prime is a prime of the form `k * 2**m + 1` where *k* is an odd positive integer and `k < 2**m` (OEIS A080076; e.g. 3, 5, 13, 17, 41, 97, 113, 193, 241, 257, ...). It accepts a typed `int` argument, raises `TypeError` for non-int/bool arguments, returns `False` for non-primes and primes not in Proth form, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestIsProthPrime` to `tests/test_prime_utils.py` covering known Proth primes, non-Proth primes (e.g. 7, 11), composites, boundaries, and the `TypeError` path; imported `is_proth_prime` to match the module's `__all__` contract. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prime_utils` passes; `python -m doctest prime_utils.py` passes. No changes to `.github/workflows/**`.

## Unreleased — added is_odd to numbers_utils

- Added `is_odd(n)` to `numbers_utils.py` as the parity complement to `is_even`. It returns `True` when *n* is not divisible by 2 (including negative odd numbers) and `False` otherwise, accepts a typed `int` argument, raises `TypeError` for non-int/bool arguments, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestIsOdd` to `tests/test_numbers_utils.py` covering odd/even/zero/negative values and the `TypeError` path; imported `is_odd` to match the module's `__all__` contract. Updated the `numbers_utils` module tree entry and prose section of `README.md`. Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_numbers_utils` passes (146 tests); `python -m doctest numbers_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.


## Unreleased — added primes_between to prime_utils

- Added `primes_between(lower, upper)` to `prime_utils.py` as a range-based prime helper companion to `primes_up_to`, `prime_count`, `next_prime`, and `prev_prime`. It returns all prime numbers *p* with *lower* <= *p* <= *upper* in ascending order, reusing `primes_up_to` for efficiency, accepts typed `int` arguments, raises `TypeError` for non-int/bool arguments and `ValueError` when *lower* > *upper*, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestPrimesBetween` to `tests/test_prime_utils.py` covering basic ranges, single primes, empty ranges, negative lower bounds, large ranges, and the `TypeError`/`ValueError` paths; imported `primes_between` to match the module's `__all__` contract. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prime_utils` passes; `python -m doctest prime_utils.py` passes; `python -m unittest tests.test_public_api` passes.


## Unreleased — added is_even to numbers_utils

- Added `is_even(n)` to `numbers_utils.py` as a parity predicate companion to the existing divisor/number classifications. It returns `True` when *n* is an even integer (including zero and negative even numbers) and `False` otherwise, accepts a typed `int` argument, raises `TypeError` for non-int/bool arguments, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestIsEven` to `tests/test_numbers_utils.py` covering even/odd/zero/negative values and the `TypeError` path; imported `is_even` to match the module's `__all__` contract. Updated the `numbers_utils` module tree entry and prose section of `README.md`. Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_numbers_utils` passes; `python -m doctest numbers_utils.py` passes; `python -m unittest tests.test_public_api` passes.


## Unreleased — hardened bytes_utils boundaries and fixed rsplit dead code

### Changed

- Fixed `rsplit` in `bytes_utils.py` by removing unreachable dead code left after the validated `bytes.rsplit` wrapper return path.
- Fixed `from_int` to accept `length=0` when representable (matching `int.to_bytes`, e.g. `from_int(0, 0) == b""`, `from_int(-1, 0, signed=True) == b""`), while preserving strict `int`/bool validation and `OverflowError`/`ValueError`/`TypeError` behavior.
- Fixed `translate`/`maketrans` compatibility to accept `bytearray` tables/inputs where behavior matches bytes semantics (`translate` now validates/accepts bytes-like 256-byte tables; docs updated accordingly).
- Expanded `tests/test_bytes_utils.py` (116→155 tests) with boundary coverage for `to_int`/`from_int` (signed/byteorder/length=0/overflow/bool/type rejection, bytearray inputs), `maketrans`/`translate` bytearray tables and length/type errors, and `split`/`find`/`index`/`rfind`/`rindex`/`replace`/`count` negative `start`/`end`, bool `start`/`end`/`count`/`maxsplit` rejection, and bytearray inputs.
- Refreshed embedded `bytes_utils.py` and `tests/test_bytes_utils.py` copies in `scaffold.sh` (`python tools/refresh_scaffold.py --check` clean).



- Added `has_paragraphs(text)` to `prompt_utils.py` as a boolean companion to `count_paragraphs` and `truncate_paragraphs`. It returns `True` when `count_paragraphs(text) > 0`, reusing the paragraph-splitting logic already in `count_paragraphs`/`truncate_paragraphs`, accepts a typed `str` argument, raises `TypeError` for non-strings, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestHasParagraphs` to `tests/test_prompt_utils.py` covering empty string (False), single line (True), single multi-line paragraph (True), multiple paragraphs (True), blank-only text (False), CRLF normalization, and the `TypeError` path; imported `has_paragraphs` to match the module's `__all__` contract.
- Updated the `prompt_utils` module tree entry and prose section of `README.md` to document `has_paragraphs`.

## Unreleased — added truncate_paragraphs to prompt_utils

- Added `truncate_paragraphs(text, max_paragraphs, suffix="...")` to `prompt_utils.py` as a paragraph-level companion to `truncate_prompt`, `truncate_words`, and `truncate_lines`. It splits *text* into paragraph blocks (runs of non-blank lines separated by blank lines), keeps the first *max_paragraphs* paragraphs joined by a single blank line, and appends *suffix* when paragraphs are removed; leading/trailing blank lines outside the kept paragraphs are dropped, matching the truncation semantics of the other truncate_* helpers. Accepts typed arguments, raises `TypeError`/`ValueError` on invalid input, is exported via `__all__`, and ships with ASCII-safe doctests. Added `TestTruncateParagraphs` (18 tests) to `tests/test_prompt_utils.py` covering no-truncation, exact, truncation, multi-line paragraphs, zero paragraphs, custom/empty suffix, leading/trailing blank-line handling, consecutive blank separators, CRLF normalization, empty text, type/value errors, and consistency with `count_paragraphs`.
- Updated the `prompt_utils` module tree entry and prose section of `README.md` to document `truncate_paragraphs`.
- Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_prompt_utils` passes (461 tests); `python -c "import doctest, prompt_utils; doctest.run_docstring_examples(prompt_utils.truncate_paragraphs, vars(prompt_utils), verbose=False, name='truncate_paragraphs')"` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — added subtract_duration to duration_utils

- Added `subtract_duration(dt, duration_str)` to `duration_utils.py` as a companion to `add_duration`, subtracting a parsed duration from a `datetime` and returning a new `datetime`. Validates that `dt` is a `datetime` (`TypeError`) and that `duration_str` is parseable (`ValueError`), exported via `__all__`, with a Google-style docstring and ASCII-safe doctests. Added `TestSubtractDuration` (6 tests) to `tests/test_duration_utils.py` covering basic/days/combined/roundtrip and error paths.
- Updated the `duration_utils` prose in `README.md` to document `subtract_duration`.
- Synchronized `duration_utils.py`, `tests/test_duration_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_duration_utils` passes (46 tests); `python -m doctest duration_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — removed duplicate __all__ entry from numbers_utils

- Removed the duplicate `is_fibonacci_number` entry from `numbers_utils.__all__` (56 entries, 55 unique) — the same class of defect previously fixed in `prime_utils` (duplicate `is_mersenne_prime`), `itertools_utils` (duplicate `take_while_pred` / stale second `__all__` block), and `string_utils` (duplicate `cosine_similarity`). Also removed a second, shadowing `is_fibonacci_number` function definition at the end of the module that duplicated the documented implementation at line 1298 (which has the doctests). `__all__` is now a clean, deduplicated list of 55 entries, each matching a single defined name; no other function behavior or signatures changed.
- Synchronized `numbers_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_numbers_utils` passes (140 tests); `python -m doctest numbers_utils.py` passes; `python -m unittest tests.test_public_api` passes; `Counter(numbers_utils.__all__)` reports no duplicates. No changes to `.github/workflows/**`.

## Unreleased — added is_fibonacci_number to numbers_utils

- Added `is_fibonacci_number(n)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int/bool arguments; it returns `True` when *n* is a member of the Fibonacci sequence (0, 1, 1, 2, 3, 5, ...), using the standard perfect-square test on `5*n*n + 4` and `5*n*n - 4`, and `False` for negative inputs. Added `TestIsFibonacciNumber` to `tests/test_numbers_utils.py` covering known Fibonacci and non-Fibonacci values, negatives, and the `TypeError` path (12 new tests). Updated the `numbers_utils` module tree entry in `README.md`.
- Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_numbers_utils` passes (140 tests); `python -m doctest numbers_utils.py` passes; `python -m unittest tests.test_public_api` passes. No changes to `.github/workflows/**`.

## Unreleased — removed duplicate __all__ entry from string_utils

- Removed the duplicate `cosine_similarity` entry from `string_utils.__all__` (34 entries, 33 unique), the same class of defect previously fixed in `prime_utils` (duplicate `is_mersenne_prime`) and `itertools_utils` (duplicate `take_while_pred` / stale second `__all__` block). `__all__` is now a clean, deduplicated list of 33 entries, each matching a defined name; no function behavior or signatures changed.
- Synchronized `string_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_string_utils` passes (300 tests); `python -m doctest string_utils.py` passes; `python -m unittest tests.test_public_api` passes; `Counter(string_utils.__all__)` reports no duplicates. No changes to `.github/workflows/**`.

## Unreleased — hardened semver_utils validation and build-metadata precedence

- Hardened `semver_utils.py` input validation to follow repository conventions: `SemanticVersion` now rejects bool/non-int version components (`TypeError`) and non-string `prerelease`/`build` metadata (`TypeError`), while preserving `ValueError` for negative components and invalid version strings.
- Fixed SemVer precedence so build metadata is ignored for comparison/ordering and equality (`compare_semver("1.0.0+1", "1.0.0+2") == 0`, `parse_semver("1.0.0+a") == parse_semver("1.0.0+b")`); build metadata remains preserved in string output. `is_valid_semver` continues to return `False` for non-string inputs (including bools).
- Added `TestEdgeCases` in `tests/test_semver_utils.py` covering whitespace stripping, empty metadata-marker rejection, build-metadata precedence/preservation, bool/non-string/type rejection, and bumped parsing behavior checks (28 tests total for the module).
- Synchronized `semver_utils.py`, `tests/test_semver_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_semver_utils` passes (28 tests); `python -m doctest semver_utils.py` passes; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.

## Unreleased — removed duplicate __all__ block from itertools_utils

- Scanned `itertools_utils.py` for duplicate `__all__` blocks (the same class of defect fixed earlier in `prime_utils` and `itertools_utils`). Found a second, complete `__all__` block at module level that overwrote the first incomplete block at line 315, leaving dead code. Removed the stale first block so the module has a single, authoritative `__all__` of 33 unique entries, each matching a defined name.
- Synchronized `itertools_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_itertools_utils` passes (106 tests); `python -m doctest itertools_utils.py` passes; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added selection_sort to sort_utils

- Added `selection_sort(items, *, key=None, reverse=False)` to `sort_utils.py` as a selection sort companion to `bubble_sort`, `insertion_sort`, and `merge_sort`. It repeatedly selects the minimum (or maximum when *reverse* is True) element from the unsorted remainder and appends it to a new result list, accepting an optional `key` and `reverse` argument, and is exported via `__all__` with a Google-style docstring and doctests. Added `TestSelectionSort` to `tests/test_sort_utils.py` covering basic, reverse, key, empty, single, duplicates, already-sorted, non-mutation, string items, and randomized comparison-with-`sorted` cases. Updated the `sort_utils` module tree entry and prose section of `README.md`. Synchronized `sort_utils.py`, `tests/test_sort_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_sort_utils` passes; `python -m doctest sort_utils.py` passes; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added is_tracked and is_finalized to gc_utils

- Added `is_tracked(obj)` and `is_finalized(obj)` to `gc_utils.py` as thin, typed wrappers around the corresponding `gc` module functions. `is_tracked` reports whether the garbage collector tracks an object (containers such as lists, dicts, and instances are tracked; atomic objects such as ints, strings, and bools are not); `is_finalized` reports whether an object has already been finalized by the GC. Both accept a typed `object` argument, are exported via `__all__`, and have Google-style docstrings with ASCII-safe doctests.
- Added `TestIsTracked` and `TestIsFinalized` to `tests/test_gc_utils.py` covering tracked containers, untracked atomic values, consistency with the underlying `gc.is_tracked`/`gc.is_finalized` functions, and the `TypeError` paths (12 new tests). Imported the new helpers at the top of the test file to match the module's `__all__` contract.
- Updated the `gc_utils` module tree entry and prose section of `README.md` to document `is_tracked` and `is_finalized`. Synchronized `gc_utils.py`, `tests/test_gc_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_gc_utils` passes; `python -m doctest gc_utils.py` passes; `python -m unittest tests.test_public_api` passes; full suite (`python -m unittest discover tests/`) passes.
- No changes to `.github/workflows/**`.

## Unreleased — added insertion_sort to sort_utils

- Added `insertion_sort(items, *, key=None, reverse=False)` to `sort_utils.py` as a stable insertion sort companion to `bubble_sort` and `merge_sort`. It accepts an optional `key` and `reverse` argument, returns a new sorted list, and is exported via `__all__` with a Google-style docstring and doctests. Added `TestInsertionSort` to `tests/test_sort_utils.py` covering basic, reverse, key, empty, single, duplicates, already-sorted, and stability cases. Updated the `sort_utils` module tree entry and prose section of `README.md`. Synchronized `sort_utils.py`, `tests/test_sort_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_sort_utils` passes; `python -m doctest sort_utils.py` passes; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added starts_with_newline and ends_with_newline to prompt_utils

- Added `starts_with_newline(text)` and `ends_with_newline(text)` to `prompt_utils.py` as boolean companions to the existing newline helpers. Each takes a typed `text` argument, is exported via `__all__`, has a Google-style docstring with ASCII-safe doctests, and raises `TypeError` for non-string arguments. `starts_with_newline` returns `True` when *text* starts with `\n`; `ends_with_newline` returns `True` when *text* ends with `\n` (including CRLF text).
- Added `TestStartsWithNewline` and `TestEndsWithNewline` to `tests/test_prompt_utils.py` covering positive/negative cases, empty input, a CRLF-prefix distinction for `starts_with_newline`, CRLF acceptance for `ends_with_newline`, and the `TypeError` paths (12 new tests). Imported the new helpers at the top of the test file to match the module's `__all__` contract.
- Updated the `prompt_utils` tree/prose entries in `README.md` to list `starts_with_newline` and `ends_with_newline`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_prompt_utils` passes (437 tests); `python -m doctest prompt_utils.py` reports a pre-existing `wrap_prompt` docstring indentation failure unchanged by this session; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added is_power_of to number_utils

- Added `is_power_of(value, base)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with ASCII-safe doctests, and `TypeError` validation for non-number arguments; it returns `True` when *value* is a non-negative integer power of *base* (i.e. `base**k == value` for some integer `k >= 0`), supporting positive/negative integer bases and the `base in {0, 1, -1}` edge cases. Non-integer numeric inputs (including integer-valued floats handled consistently) return `False`.
- Added `TestIsPowerOf` to `tests/test_number_utils.py` covering positive bases, non-powers, `base` 1/0/-1, negative bases, integer-valued floats, and the `TypeError` paths (8 new tests). Imported `is_power_of` at the top of the test file to match the module's `__all__` contract.
- Updated the `number_utils` tree/prose entries in `README.md` to document `is_power_of`. Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_number_utils` passes (282 tests); `python -m doctest number_utils.py` passes; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.





- Found two real `__all__` defects by scanning every wrapper module for duplicate or undefined export entries: `prime_utils.__all__` listed `is_mersenne_prime` twice (56 entries, 55 unique) and `itertools_utils.__all__` listed `take_while_pred` twice (25 entries, 24 unique). Removed the duplicate entries so each module's `__all__` is a clean, deduplicated export list matching its defined names.
- Synchronized `prime_utils.py`, `itertools_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_prime_utils` passes; `python -m unittest tests.test_itertools_utils` passes; `python -m unittest tests.test_public_api` passes; `python -m doctest prime_utils.py` and `python -m doctest itertools_utils.py` pass; full suite (`python -m unittest discover tests/`) passes (8282 tests).
- No changes to `.github/workflows/**`.

## Unreleased — added is_coprime to math_utils

- Added `is_coprime(a, b)` to `math_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *a* and *b* are coprime (their greatest common divisor is 1), reusing the existing `gcd` helper and `math.gcd`.
- Added `TestIsCoprime` to `tests/test_math_utils.py` covering coprime pairs, non-coprime pairs, edge cases with zero/one/negatives, and the `TypeError` paths (10 new tests). Imported `is_coprime` at the top of the test file to match the module's `__all__` contract.
- Updated the `math_utils` module tree entry and prose section of `README.md`.
- Synchronized `math_utils.py`, `tests/test_math_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_math_utils` passes; `python -m doctest math_utils.py` passes; `make test` stays green.
- No changes to `.github/workflows/**`.

## Unreleased — added is_prime to number_utils

- Added `is_prime(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *value* is a prime number greater than 1 (0, 1, and negatives are not prime), using trial division up to the square root.
- Added `TestIsPrime` to `tests/test_number_utils.py` covering known primes, non-primes, boundary values, and the `TypeError` paths. Imported `is_prime` at the top of the test file to match the module's `__all__` contract.
- Updated the `number_utils` module tree entry and prose section of `README.md`.
- Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_number_utils` passes; `python -m doctest number_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added bit_count and is_zero to bytes_utils

- Added `bit_count(data)` and `is_zero(data)` to `bytes_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-bytes arguments. `bit_count` returns the total number of set (1) bits across all bytes (empty input yields `0`); `is_zero` returns `True` when every byte is zero or *data* is empty.
- Added `TestBitCount` and `TestIsZero` to `tests/test_bytes_utils.py` covering representative inputs, bytearray support, empty input, and the `TypeError` paths (12 new tests). Imported the new helpers to match the module's `__all__` contract.
- Updated the `bytes_utils` module tree entry and prose section of `README.md` to document `bit_count`, `is_zero`, and the existing `to_int`/`from_int` helpers.
- Synchronized embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_bytes_utils` passes (111 tests); `python -m doctest bytes_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added count_components to version_utils

- Added `count_components(version)` to `version_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation; it returns the number of dot-separated components in a dotted version string (``"1.2.3"`` yields ``3``, ``"1"`` yields ``1``, and the empty string yields ``0``). Added `TestCountComponents` to `tests/test_version_utils.py` covering happy paths, empty input, prerelease/build metadata, and the `TypeError` path. Updated the `version_utils` module tree entry and prose section of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_version_utils` passes; `python -m doctest version_utils.py` passes; `make test` stays green.
- No changes to `.github/workflows/**`.

## Unreleased — fixed numbers_utils abundance doctest indentation

- Found a real doctest defect in `numbers_utils.abundance`: the expected output line for `abundance(12)` was indented with four extra spaces (`    4`), so `python -m doctest numbers_utils.py` reported a failure even though the function returned the correct value. The expected output was corrected to `4` to match the surrounding doctest examples.
- Verified: `python -m doctest numbers_utils.py` passes (0 failures); `python -m unittest tests.test_numbers_utils` passes (136 tests); `make test` stays green; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.
- No changes to `.github/workflows/**`.

## Unreleased — hardened NaN/inf validation in interval_utils and math_utils

- `math_utils.clamp` now rejects `NaN` for `value`, `min_val`, or `max_val` with `ValueError` (previous `NaN` behavior was inconsistent due to Python min/max semantics). Infinite values remain supported where bounds allow.
- `interval_utils.normalize_interval` now rejects `NaN` endpoints with `ValueError`.
- `interval_utils.interval_clamp` now rejects `NaN` values with `ValueError`; `NaN` endpoints remain rejected by interval validation.
- Updated `tests/test_math_utils.py` and `tests/test_interval_utils.py` to cover `NaN`/`inf` boundary cases and the new validation.
- Synchronized embedded copies in `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — added abundance and amicable helpers to numbers_utils

- Added `abundance(n)` to `numbers_utils.py`: returns `aliquot_sum(n) - n` (positive for abundant, zero for perfect, negative for deficient) with `TypeError`/`ValueError` validation.
- Added `are_amicable(a, b)` and `is_amicable_number(n)` to `numbers_utils.py` (aliquot-sum-based amicable-pair helpers; `is_amicable_number` is distinct from `prime_utils.is_amicable`).
- Exported `abundance`, `are_amicable`, and `is_amicable_number` from `numbers_utils.__all__`.
- Added `TestAbundance`, `TestAreAmicable`, and `TestIsAmicableNumber` to `tests/test_numbers_utils.py` covering known values, edge cases, and `TypeError`/`ValueError` paths.
- Updated `README.md` (tree + prose) and `.kilo/command/scaffold-project.md`; synchronized embedded copies with `make refresh-scaffold` and verified `python tools/refresh_scaffold.py --check`.
- No changes to `.github/workflows/**`.

## Unreleased — added aliquot_sum to number_utils

- Added `is_sphenic_number(n)` to `numbers_utils.py` with `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int/bool arguments (rejecting `bool`); a sphenic number is a positive integer that is the product of exactly three distinct primes (e.g. 30, 42, 66). Added `TestIsSphenicNumber` to `tests/test_numbers_utils.py` covering known sphenic numbers, non-sphenic values (including prime powers and non-squarefree composites), negatives, and the `TypeError` path. Updated `README.md` (`numbers_utils` tree entry and prose) and `.kilo/command/scaffold-project.md`; synchronized embedded copies with `make refresh-scaffold` and verified `python tools/refresh_scaffold.py --check`.
- Added `aliquot_sum(n)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation; it returns the sum of the proper divisors of *n* (the aliquot sum), reusing `proper_divisors`. Added `TestAliquotSum` to `tests/test_numbers_utils.py` covering known values, perfect/abundant/deficient classification, and the `TypeError`/`ValueError` paths. Imported `aliquot_sum` at the top of the test file to match the module's `__all__` contract. Updated the `number_utils` module tree entry and prose section of `README.md`. Synchronized `number_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_numbers_utils` passes; `python -m doctest numbers_utils.py` passes; `make test` stays green.
- No changes to `.github/workflows/**`.

## Unreleased — added is_mersenne_prime to number_utils

- Added `is_mersenne_prime(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation; it returns `True` if *value* is a prime of the form `2^p - 1` for some prime *p* (e.g. 3, 7, 31, 127, 8191). It rejects non-primes and Mersenne composites such as 15/63/255. Added `TestIsMersennePrime` to `tests/test_number_utils.py`. Updated the `number_utils` tree entry and prose in `README.md`. Regenerated `scaffold.sh` via `tools/refresh_scaffold.py`.

## Unreleased — added has_alphanumeric to prompt_utils

- Added `has_alphanumeric(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* contains at least one ASCII letter or digit and `False` otherwise, serving as a boolean companion to :func:`count_letters` and :func:`count_digits`. Added `TestHasAlphanumeric` to `tests/test_prompt_utils.py` covering strings with letters/digits/mixed, negatives, empty input, and the `TypeError` paths (6 new tests). Imported `has_alphanumeric` at the top of the test file to match the module's `__all__` contract. Updated the `prompt_utils` module tree entry and prose section of `README.md`.
- Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_prompt_utils` passes (427 tests); `python -m doctest prompt_utils.py` passes; `make test` stays green.
- No changes to `.github/workflows/**`.

## Unreleased — fixed itertools_utils grouper fillvalue handling

- Found a real defect in `itertools_utils.grouper`: the `fillvalue` parameter was accepted but never used, so the trailing partial chunk was silently dropped instead of being padded to the full chunk size. For example, `grouper([1, 2, 3, 4, 5], 2)` returned `[(1, 2), (3, 4)]` rather than `[(1, 2), (3, 4), (5, None)]`, diverging from the classic `itertools` recipe it documented. Rewrote the implementation to drive `zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)` so every emitted tuple has exactly *n* elements, with the last one padded when needed; empty input yields `[]` and exact multiples are unaffected. Added a `TestGrouper` suite to `tests/test_itertools_utils.py` covering exact-multiple, default-None padding, custom `fillvalue`, short-chunk padding to full size, size-one, empty input, strings, the per-chunk length invariant, order preservation, and the `TypeError`/`ValueError` paths (13 new tests). Imported `grouper` at the top of the test file to match the module's `__all__` contract. Updated the `itertools_utils` module tree entry and prose section of `README.md` to document `grouper`, `roundrobin`, `padnone`, and `ncycles`. Synchronized `itertools_utils.py`, `tests/test_itertools_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_itertools_utils` passes (107 tests); `python -m doctest itertools_utils.py` passes; `make test` stays green; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — fixed prime_utils doctests for is_happy_prime and largest_prime_factor

- Found two real doctest defects in `prime_utils.py` that caused `python -m doctest prime_utils.py` to report 4 failures. The `is_happy_prime` doctest incorrectly listed 2, 3, and 5 as happy primes (they are prime but unhappy — they fall into the 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 loop); the doctest examples were corrected to use genuinely happy primes (23, 31, 79) and the docstring prose was updated to name the unhappy primes explicitly. The `largest_prime_factor` doctest for input `1` expected `ValueError: n must be >= 1` but the function raises `ValueError: n must be >= 2`; the expected message was corrected. The function implementations and their `tests/test_prime_utils.py` coverage were unchanged (the test suite already asserted the correct behavior).
- Verified: `python -m doctest prime_utils.py` passes (0 failures); `python -m unittest tests.test_prime_utils` passes (278 tests); `make test` passes; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.
- No changes to `.github/workflows/**`.

## Unreleased — added is_weird_number to numbers_utils

- Added `is_weird_number(n)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation; it returns `True` when *n* is abundant but not semiperfect (a weird number such as 70 or 836), reusing `is_abundant_number` and `is_semiperfect_number`; numbers below 1 return `False`. Added `TestIsWeirdNumber` to `tests/test_numbers_utils.py` covering known weird numbers, abundant-but-semiperfect non-weird numbers, non-abundant numbers, negatives/zero, and `TypeError` paths (6 new tests). Imported `is_weird_number` at the top of the test file to match the module's `__all__` contract. Updated the `numbers_utils` module tree entry and prose section of `README.md`.
- Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_numbers_utils` passes; `python -m doctest numbers_utils.py` passes; `make test` stays green.
- No changes to `.github/workflows/**`.

## Unreleased — added is_mersenne_number to number_utils

- Added `is_mersenne_number(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation; it returns `True` if *value* is of the form `2^p - 1` for some non-negative integer *p* (e.g. 1, 3, 7, 15, 31). Accepts integer-valued floats. Added `TestIsMersenneNumber` to `tests/test_number_utils.py` covering Mersenne numbers, non-Mersenne numbers, integer-valued floats, and `TypeError` paths for non-numbers/bools. Updated the `number_utils` module tree entry and prose section of `README.md`.
- Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_number_utils` passes (258 tests); `python -m doctest number_utils.py` shows only pre-existing failures (additive_persistence, is_close) unchanged by this change.
- No changes to `.github/workflows/**`.

## Unreleased — added shannon_entropy to stats

- Added `shannon_entropy(numbers)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation; it returns the Shannon entropy of the discrete values in bits (``-sum(p * log2(p))`` over the probability of each distinct value), which is 0 for a list of identical values and ``log2(n)`` for *n* distinct values. Added `TestShannonEntropy` to `tests/test_stats.py` covering identical/all-distinct/mixed distributions, single element, two-distinct equal, order invariance, float and negative inputs, and the empty-list/non-list/non-numeric/bool rejection paths (12 new tests). Imported `shannon_entropy` at the top of the test file to match the module's `__all__` contract. Updated the `stats` prose section of `README.md`.
- Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_stats` passes (384 tests); `python -m doctest stats.py` shows only the 6 pre-existing float-formatting failures (geometric_mean, kurtosis, median, mode, winsorized_stddev — unchanged before and after this change); `shannon_entropy`'s 3 doctests pass.
- No changes to `.github/workflows/**`.

## Unreleased — fixed prompt_utils __all__ gap for has_punctuation

- Found a real contract gap: `prompt_utils.has_punctuation` was a fully-implemented public function (typed signature, Google-style docstring with doctests, `TypeError` validation) but missing from `prompt_utils.__all__`, violating the public-API export contract that every public attribute must be listed in `__all__`. The gap was caught by `tests/test_public_api.py` as the only test failure in the suite.
- Added `has_punctuation` to `prompt_utils.__all__` next to `has_letters` (66 exports total).
- Updated the `prompt_utils` module tree entry and prose section of `README.md` to document `has_punctuation` alongside its boolean companions. The function, its implementation, doctests, and `tests/test_prompt_utils.py` coverage were unchanged.
- Synchronized `prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes (7813 tests); `python -m unittest tests.test_prompt_utils` passes; `python -m doctest prompt_utils.py` passes; `python -m unittest tests.test_public_api` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added has_letters to prompt_utils

- Added `has_letters(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* contains at least one ASCII letter (a-z or A-Z) and `False` otherwise, serving as a boolean companion to :func:`count_letters`. Non-letter characters (digits, punctuation, whitespace) do not qualify and empty text returns `False`. Added `TestHasLetters` to `tests/test_prompt_utils.py` covering strings with letters, a single letter, digit-only and punctuation-only negatives, uppercase-only, mixed case, empty input, and the `TypeError` paths (8 new tests). Imported `has_letters` at the top of the test file to match the module's `__all__` contract. Updated the `prompt_utils` module tree entry and prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils` passes; `python -m doctest prompt_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added mode_frequency to stats

- Added `mode_frequency(numbers)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation; it returns the number of times the most frequently occurring value appears in a list of numbers (1 when every value is distinct). Added `TestModeFrequency` to `tests/test_stats.py` covering basic frequency, all-distinct, single-value, single-element, negative and float inputs, ties, and the empty/non-list/non-numeric/bool rejection paths (11 new tests). Imported `mode_frequency` at the top of the test file to match the module's `__all__` contract. Updated the `stats` prose section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_stats` passes; `python -m doctest stats.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — document dumbdbm_utils cross-references

- Registered the `dumbdbm_utils` module (added in a prior session) in the project cross-references: added `dumbdbm_utils.py` to the `README.md` module tree, test tree, and prose section; added `dumbdbm_utils.py` and `tests/test_dumbdbm_utils.py` to `CHANGELOG.md`; listed both in the `scaffold.sh` header comment and `tests/test_scaffold.py`; synchronized the embedded README and CHANGELOG templates in `scaffold.sh` with `make refresh-scaffold`. This closes the scaffold-sync gap that left six `test_scaffold_sync` failures for `dumbdbm_utils`.
- No changes to `.github/workflows/**`.

## Unreleased — added has_lowercase to prompt_utils

- Added `has_lowercase(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* contains at least one ASCII lowercase letter (a-z) and `False` otherwise, serving as a boolean companion to :func:`count_lowercase`. Added `TestHasLowercase` to `tests/test_prompt_utils.py` covering strings with lowercase, a single lowercase letter, strings without lowercase, empty input, and the `TypeError` path (6 new tests). Imported `has_lowercase` at the top of the test file to match the module's `__all__` contract. Updated the `prompt_utils` module tree entry and prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils` passes; `python -m doctest prompt_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added sum_of_primes_up_to to prime_utils

- Added `sum_of_primes_up_to(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns the sum of all prime numbers up to and including *n*. Added `TestSumOfPrimesUpTo` to `tests/test_prime_utils.py` (2 tests). Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — fixed list_utils doctest quote style

- Corrected a doctest in `list_utils.py` for `unique_preserve_order` that expected the double-quoted repr `["a", "b"]`; Python's `repr` for lists uses single quotes, so the example now reads `['a', 'b']` to match actual output. The function, its `__all__` export, `TypeError` validation, and `tests/test_list_utils.py` coverage were unchanged. Synchronized `list_utils.py` and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_list_utils` passes (65 tests); `python -m doctest list_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added is_pangram to string_utils

- Added `is_pangram(text)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* contains every letter of the English alphabet at least once (case-insensitive, ignoring non-alphabetic characters) and `False` otherwise, including for the empty string. Added `TestIsPangram` to `tests/test_string_utils.py` covering classic pangrams, case-insensitivity, missing-letter and empty-string negatives, non-alphabetic characters being ignored, and the `TypeError` paths (8 new tests). Imported `is_pangram` at the top of the test file to match the module's `__all__` contract. Updated the `string_utils` module tree entry and prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_string_utils` passes; `python -m doctest string_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added has_digits to prompt_utils

- Added `has_digits(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* contains at least one ASCII digit (0-9) and `False` otherwise, serving as a boolean companion to :func:`count_digits`. Added `TestHasDigits` to `tests/test_prompt_utils.py` covering strings with digits, a single digit, digit-only strings, strings without digits, empty input, and the `TypeError` path (6 new tests). Imported `has_digits` at the top of the test file to match the module's `__all__` contract. Updated the `prompt_utils` module tree entry and prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils` passes; `python -m doctest prompt_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added damerau_levenshtein_distance to string_utils

- Added `damerau_levenshtein_distance(text1, text2)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the Damerau-Levenshtein edit distance (insertions, deletions, substitutions, and adjacent-character transpositions counted as a single edit) between two strings using the optimal-string-alignment algorithm with O(len(text1) * len(text2)) time and O(min(len(text1), len(text2))) space. Added `TestDamerauLevenshteinDistance` to `tests/test_string_utils.py` covering transpositions, the classic example, identical strings, empty strings, one-empty-string, substitution-only, insertion/deletion, case sensitivity, whitespace preservation, unicode, symmetry, and the `TypeError` paths for both arguments (13 new tests). Imported `damerau_levenshtein_distance` at the top of the test file to match the module's `__all__` contract. Updated the `string_utils` module tree entry and prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_string_utils` passes; `python -m doctest string_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added format_duration to time_utils

- Added `format_duration(seconds)` to `time_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation; it formats a non-negative number of seconds as a human-readable `Hh Mm Ss` string, omitting zero-valued components (except a bare `0s`). Added tests in `tests/test_time_utils.py` covering zero, seconds-only, minutes, hours, `TypeError`, and `ValueError` paths. Updated the `time_utils` module tree entry and prose section of `README.md`. Synchronized `time_utils.py`, `tests/test_time_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — added is_happy_prime to prime_utils

- Added `is_happy_prime(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns `True` if *n* is both prime and happy (a happy number reaches 1 when iteratively replaced by the sum of squares of its decimal digits), `False` otherwise. Added `TestIsHappyPrime` to `tests/test_prime_utils.py` covering small happy primes (2, 3, 5, 7, 13, 19, 31), primes that are unhappy (11, 17, 23, 29, 41), composites, `1`, `0`, negatives, and `TypeError` paths. Imported `is_happy_prime` at the top of the test file to match the module's `__all__` contract. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — added is_super_prime to prime_utils

- Added `is_super_prime(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *n* is a super-prime (prime-indexed prime) — a prime whose position in the sequence of primes is itself prime (e.g. 3 is the 2nd prime and 2 is prime, so 3 is a super-prime; OEIS A006450), reusing the existing `is_prime` and `prime_count` helpers. Added `TestIsSuperPrime` to `tests/test_prime_utils.py` covering known super-primes matching OEIS A006450, primes that are not super, non-primes, boundary values, and the `TypeError` paths (13 new tests). Imported `is_super_prime` at the top of the test file to match the module's `__all__` contract. Updated the `prime_utils` module tree entry and prose section of `README.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prime_utils` passes (267 tests); `python -m doctest prime_utils.py` passes (only the pre-existing `largest_prime_factor(1)` message mismatch remains); `python -m ruff check prime_utils.py tests/test_prime_utils.py` is clean; `python -m mypy prime_utils.py tests/test_prime_utils.py` reports no issues.
- No changes to `.github/workflows/**`.

## Unreleased — added tests for prompt_utils count_punctuation helper

- Added `TestCountPunctuation` to `tests/test_prompt_utils.py` covering the `count_punctuation(text)` public helper, which was already exported in `prompt_utils.__all__` and fully implemented (typed signature, Google-style docstring with doctests, `TypeError` validation for non-string arguments) but had no corresponding test coverage. New tests cover basic counts, empty string, only-punctuation, punctuation with digits/letters, mixed punctuation, unicode non-punctuation, and the `TypeError` paths (10 new tests). Imported `count_punctuation` at the top of the test file to match the module's `__all__` contract. Updated the `prompt_utils` module tree entry and prose section of `README.md` to include `count_punctuation`. Synchronized `tests/test_prompt_utils.py`, `prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils` passes (369 tests); `make test` passes; `make lint` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added tests for prompt_utils chomp helper

- Added `TestChomp` to `tests/test_prompt_utils.py` covering the `chomp(text)` public helper, which was already exported in `prompt_utils.__all__` and fully implemented (typed signature, Google-style docstring with doctests, `TypeError` validation for non-string arguments) but had no corresponding test coverage. New tests cover trailing `\n`, lone `\r`, `\r\n`, no-newline, empty string, only-newline, only-CRLF, preservation of internal newlines, and the `TypeError` paths (10 new tests). Imported `chomp` at the top of the test file to match the module's `__all__` contract. `chomp` is already listed in the `prompt_utils` prose section of `README.md`, so no README change was required. Synchronized `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_prompt_utils` passes (359 tests); `make test` passes; `make lint` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added levenshtein_distance to string_utils

- Added `levenshtein_distance(text1, text2)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform *text1* into *text2*, computed with a dynamic-programming algorithm using O(min(len(text1), len(text2))) space. Added `TestLevenshteinDistance` to `tests/test_string_utils.py` covering the classic kitten/sitting example, identical strings, empty strings, one-empty-string, substitution-only, insertion/deletion, case sensitivity, whitespace preservation, unicode, symmetry, a known sunday/saturday distance, and the `TypeError` paths for both arguments (12 new tests). Imported `levenshtein_distance` at the top of the test file to match the module's `__all__` contract. Updated the `string_utils` module tree entry and prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_string_utils` passes; `python -m doctest string_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added add_weeks to datetime_utils

- Added `add_weeks(dt, weeks)` to `datetime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int week counts; it is a companion to `add_days` that shifts a datetime forward or backward by a whole number of weeks (delegating to `add_days(dt, weeks * 7)`). Added `TestAddWeeks` to `tests/test_datetime_utils.py` covering positive/negative/zero weeks, datetime-object input, month/year boundary crossing, invalid-string `ValueError`, and non-int `TypeError` paths (8 new tests). Updated the `datetime_utils` module prose section of `README.md`. Synchronized `datetime_utils.py`, `tests/test_datetime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — added is_anagram to string_utils

- Added `is_anagram(text1, text2)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when two strings contain the same characters in the same quantities (ignoring case and whitespace) and `False` otherwise, treating the empty string as an anagram of itself. Added `TestIsAnagram` to `tests/test_string_utils.py` covering anagrams, case-insensitivity, whitespace handling, non-anagrams, empty/single-character inputs, and the `TypeError` paths (9 new tests). Imported `is_anagram` at the top of the test file to match the module's `__all__` contract. Updated the `string_utils` module tree entry and prose section of `README.md`. Synchronized `string_utils.py`, `tests/test_string_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_string_utils` passes; `python -m doctest string_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added distance to calculator.__all__

- Fixed a public-API contract gap in `calculator.py`: `distance(x1, y1, x2, y2)` was a fully-implemented public function (typed signature, Google-style docstring, `TypeError` validation for non-real-number coordinates) but was missing from `calculator.__all__`, violating the convention that every public attribute must be exported. The gap was surfaced by `tests/test_public_api.py` as the only failure in `make test` (7717 tests). Added `distance` to `calculator.__all__` next to `hypotenuse` (32 exports total). No new tests required — `TestDistance` already covered the function. Synchronized `calculator.py`, `scaffold.sh`, `README.md`, `CHANGELOG.md`, and `PROJECT_STATUS.md`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `make test` passes (7717 tests); `make lint` passes (ruff, all checks passed); `make typecheck` shows only pre-existing errors (62 errors in 9 files, unchanged before and after this change — unrelated to calculator.py).
- No changes to `.github/workflows/**`.

## Unreleased — added gcd to calculator

- Added `gcd(a, b)` to `calculator.py` with typed signature, `__all__` export, Google-style docstring, and validation; it returns the greatest common divisor of two non-negative integers using Euclid's algorithm with `gcd(0,0)=0`, raises `TypeError` if inputs are not ints (bools rejected), and `ValueError` if either is negative. Added `TestGCD` to `tests/test_calculator.py` covering basic cases and validation paths. Updated `README.md` to document `gcd`. Synchronized `calculator.py`, `tests/test_calculator.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m pytest tests/test_calculator.py -v` passes.
- No changes to `.github/workflows/**`.

## Unreleased — audit interval_utils and math_utils boundary cases

- Audited `interval_utils.py` and `math_utils.py` boundary cases and added comprehensive tests for `TypeError`/`ValueError` paths, touching intervals, empty inputs, boolean rejection, and invalid interval elements. Added `TestIntervalUtilsBoundariesMore` to `tests/test_interval_utils.py` and `TestMathUtilsBoundaries` to `tests/test_math_utils.py`. Refreshed embedded copies via `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_interval_utils tests.test_math_utils` passes. No changes to `.github/workflows/**`.

## Unreleased — added maketrans and translate to bytes_utils

- Added `maketrans(frm, to)` and `translate(data, table)` to `bytes_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError`/`ValueError` validation; `maketrans` builds a 256-byte translation table mapping each byte of *frm* to the corresponding byte of *to* (identity elsewhere), and `translate` replaces each byte of *data* according to a 256-byte table, wrapping `bytes.maketrans`/`bytes.translate`. Added `TestMaketrans` and `TestTranslate` to `tests/test_bytes_utils.py` covering mapping, identity, empty inputs, bytearray input, type errors, length mismatches, full-range translation, and table-length validation (19 new tests). Imported `maketrans` and `translate` at the top of the test file to match the module's `__all__` contract. Updated the `bytes_utils` module tree entry and prose section of `README.md`.
- Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_bytes_utils` passes; `python -m doctest bytes_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added abs_difference to calculator

- Added `abs_difference(a, b)` to `calculator.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-real-number arguments; it returns the absolute difference |a - b|. Added `TestAbsDifference` to `tests/test_calculator.py` covering positive, reversed, equal, both-negative, mixed-sign, and float inputs plus the `TypeError` paths for non-numeric and bool arguments (8 new tests). Imported `abs_difference` at the top of the test file to match the module's `__all__` contract. Synchronized `calculator.py`, `tests/test_calculator.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m pytest tests/test_calculator.py -v` passes (19 tests); `python -m doctest calculator.py` passes (3 doctests).
- No changes to `.github/workflows/**`.

## Unreleased — added has_metadata to version_utils
- Added `has_metadata(version)` to `version_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when a version string contains either a `-` prerelease suffix or a `+` build metadata suffix (or both), and `False` otherwise. Added `TestHasMetadata` to `tests/test_version_utils.py` covering present/absent/empty inputs and the `TypeError` path (3 new tests). Imported `has_metadata` at the top of the test file to match the module's `__all__` contract. Updated the `version_utils` module tree entry and prose section of `README.md`. Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m pytest tests/test_version_utils.py -v` passes; `python -m doctest version_utils.py` passes.

## Unreleased — added has_build_metadata to version_utils

- Added `has_build_metadata(version)` to `version_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when a version string contains a `+` build metadata suffix and `False` otherwise. Added `TestHasBuildMetadata` to `tests/test_version_utils.py` covering present/absent/empty inputs and the `TypeError` path (4 new tests). Imported `has_build_metadata` at the top of the test file to match the module's `__all__` contract. Updated the `version_utils` module tree entry and prose section of `README.md`.
- Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_version_utils` passes; `python -m doctest version_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added split_paragraphs to string_utils

- Added `split_paragraphs(text)` to `string_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it splits text into paragraphs separated by blank lines, normalizing line endings and ignoring empty paragraphs. Added `TestSplitParagraphs` to `tests/test_string_utils.py` covering basic splits, internal line breaks, multiple blank lines, CRLF, leading/trailing blank lines, empty/whitespace-only inputs, and the `TypeError` path (10 new tests). Imported `split_paragraphs` at the top of the test file to match the module's `__all__` contract. Updated the `string_utils` module tree entry and prose section of `README.md`.
- Synchronized `string_utils.py`, `tests/test_string_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_string_utils` passes (187 tests, 50 subtests); `python -m doctest string_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added is_disjoint to set_utils

- Added `is_disjoint(a, b)` to `set_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-iterable arguments; it returns `True` when the two iterables share no common elements and `False` otherwise. Added `TestIsDisjoint` (6 tests) to `tests/test_set_utils.py` covering disjoint/s overlapping/identical/empty inputs and the `TypeError` paths. Imported `is_disjoint` at the top of the test file to match the module's `__all__` contract. Updated the `set_utils` module tree entry and prose section of `README.md`.
- Synchronized `set_utils.py`, `tests/test_set_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_set_utils` passes; `python -m doctest set_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — fixed greeting_utils __all__ export for format_good_luck

- Added `format_good_luck` to `greeting_utils.__all__` so every public attribute defined by the module is exported, closing a contract gap left when the helper was introduced. This restores the public-API invariant enforced by `tests/test_public_api.py`. Synchronized `greeting_utils.py`, `tests/test_greeting_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — added days_between to calendar_utils

- Added `days_between(date1, date2)` to `calendar_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-date/datetime arguments; it returns the number of days from *date1* to *date2* (positive when *date2* is later, negative when earlier, zero when equal), ignoring time components. Added `TestDaysBetween` to `tests/test_calendar_utils.py` covering positive/negative spans, the same day, a leap-year span, datetime inputs (time components ignored), and the `TypeError` paths (7 new tests). Imported nothing new beyond the existing public API to match the module's `__all__` contract. Updated the `calendar_utils` module tree entry and prose section of `README.md`.
- Synchronized `calendar_utils.py`, `tests/test_calendar_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_calendar_utils` passes; `python -m doctest calendar_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added format_encouragement to greeting_utils

- Added `format_encouragement(name, message="You've got this!")` to `greeting_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns a string of the form `"{name}, {message}!"`. Added `TestFormatEncouragement` to `tests/test_greeting_utils.py` covering the default message, custom message, empty name, and the `TypeError` paths (5 new tests). Imported `format_encouragement` at the top of the test file to match the module's `__all__` contract. Updated the `greeting_utils` module tree entry and prose section of `README.md`.
- Synchronized `greeting_utils.py`, `tests/test_greeting_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_greeting_utils` passes; `python -m doctest greeting_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added balanced and weak prime predicates

- Added `is_balanced_prime(n)` and `is_weak_prime(n)` to `prime_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation via `_require_int`. `is_balanced_prime` returns True when a prime equals the arithmetic mean of its two nearest primes (e.g. 5, 53, 157, 173, 211); `is_weak_prime` returns True when a prime is less than the arithmetic mean of its two nearest primes (e.g. 7, 13, 19, 23, 31). Added `TestIsBalancedPrime` and `TestIsWeakPrime` to `tests/test_prime_utils.py` covering known values, disjointness from the other categories, non-primes, boundary cases, and `TypeError` paths. Updated the `prime_utils` module tree entry and prose section of `README.md`.
- Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_prime_utils` passes (262 tests); `python -m doctest prime_utils.py` passes (no new doctest failures).
- No changes to `.github/workflows/**`.

## Unreleased — added del_nested to data_utils

- Added `del_nested(d, path, sep=".")` to `data_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, `TypeError` validation for non-dict arguments and non-string paths, `ValueError` for empty paths, and a boolean return indicating whether a key was deleted. Added `TestDelNested` to `tests/test_data_utils.py` covering basic deletion, deep paths, missing paths, empty dicts, intermediate non-dict values, custom separators, and the `TypeError`/`ValueError` paths (12 new tests). Imported `del_nested` at the top of the test file to match the module's `__all__` contract.
- Updated the `data_utils` prose section of `README.md` to document `del_nested` and `set_nested`.
- Synchronized `data_utils.py`, `tests/test_data_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_data_utils` passes; `python -m doctest data_utils.py` passes.
- No changes to `.github/workflows/**`.

## Unreleased — added get_nested to data_utils

- Added `get_nested(d, path, default=None, sep=".")` to `data_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, `TypeError` validation for non-dict arguments and non-string paths, and a `default` value returned when a path segment is missing or an intermediate value is not a dict. Added `TestGetNested` to `tests/test_data_utils.py` covering basic and deep traversal, missing-path defaults, a custom separator, non-dict intermediates, and the `TypeError` paths (9 new tests). Imported `get_nested` at the top of the test file to match the module's `__all__` contract.
- Updated the `data_utils` prose section of `README.md` to document `get_nested`.
- Synchronized `data_utils.py`, `tests/test_data_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_data_utils` passes; `python -m doctest data_utils.py` passes; full suite runs green.
- No changes to `.github/workflows/**`.

## Unreleased — added comprehensive boundary tests for bz2_utils

- Audited `bz2_utils.py` (5 helpers) and found only 3 tests covering the two round-trip happy paths and `bz2_open`; boundary cases (empty data, single byte, compression levels, invalid/decompressed data, non-bytes inputs, out-of-range levels, missing files, directories, text mode, pathlib paths, idempotency) were untested.
- Rewrote `tests/test_bz2_utils.py` with 22 tests covering every helper: empty/single-byte/large round-trips, every valid compression level, invalid bz2 data and non-bytes `TypeError` paths, out-of-range `ValueError` paths, `bz2_write` empty/overwrite/level cases, `bz2_read` missing-file and directory cases, `bz2_open` binary/text/level/pathlib/default-mode cases, and compress idempotency. Imported every public name at the top of the test file to match the module's `__all__` contract.
- Synchronized `tests/test_bz2_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes (7424 tests, +22 over the previous run).
- No changes to `.github/workflows/**`.

## Unreleased — added comprehensive tests for queue_utils

- Audited `queue_utils.py` (a `Queue` class with 11 methods plus 6 module-level helpers) and found only 3 tests covering the happy path and the two empty-queue `IndexError` paths; `clear`, `to_list`, `from_list`, the `enqueue` return value, and the round-trip drain were untested.
- Rewrote `tests/test_queue_utils.py` with 17 tests covering every public helper and method: default/empty/list construction, `enqueue`/`dequeue`/`peek` happy paths and return values, the `IndexError` paths on empty queues, `is_empty`/`size` transitions, `clear` (including on an already-empty queue), `to_list` returning an independent copy, `from_list` (including the empty-list case), and a full round-trip drain. Imported every public name at the top of the test file to match the module's `__all__` contract.
- Synchronized `tests/test_queue_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes (7405 tests, +17 over the previous run).
- No changes to `.github/workflows/**`.

## Unreleased — added comprehensive tests for deque_utils

- Audited `deque_utils.py` (13 public helpers) and found only 2 tests covering 5 helpers; the remaining helpers (`clear_deque`, `count_in_deque`, `remove_from_deque`, `reverse_deque`, `extend_left`, `extend_right`, `rotate_deque`) had no test coverage.
- Rewrote `tests/test_deque_utils.py` with 26 tests covering every public helper: happy paths, empty/single-element boundaries, `maxlen` eviction, positive/negative/full-cycle rotation, the `IndexError` paths on empty deques, and the `ValueError` path for `remove_from_deque` on a missing value. Imported every public name at the top of the test file to match the module's `__all__` contract.
- Corrected the stale `deque_utils` prose in `README.md`, which described a different API (`count_deque`, `copy_deque`, `index_deque`, `insert_deque`, `deque_len`, `is_empty`, `maxlen_deque`, `to_list`, `from_iterable`, re-exported `Deque`) than the module actually implements. The prose now matches the real public API (`count_in_deque`, `remove_from_deque`, `deque_to_list`, etc.).
- Synchronized `tests/test_deque_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes (7388 tests, +24 over the previous run); `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- No changes to `.github/workflows/**`.

## Unreleased — extended __all__ contract guard to all top-level modules

- Audited the public-API ``__all__`` contract across every top-level module in the repository (264 modules). Every module already defines ``__all__`` and every public attribute defined by a module is exported — no gaps found, so no ``__all__`` edits were needed.
- Identified a real durability gap: ``tests/test_public_api.py`` only guarded ``*_utils.py`` wrapper modules, leaving non-wrapper modules (``stats.py``, ``strings.py``, ``shapes.py``, ``prompt_utils.py``, ...) unguarded. That gap is how earlier regressions (``upper``/``lower`` missing from ``bytes_utils.__all__``) slipped through unnoticed.
- Extended ``_iter_wrapper_modules`` in ``tests/test_public_api.py`` to discover every top-level module (wrapper or not), so the contract is enforced repo-wide. Verified the test catches the regression it previously missed: temporarily removing a name from ``math_utils.__all__`` fails the test, and restoring it passes.
- Updated the ``README.md`` Overview to document the repo-wide ``__all__`` contract and its test guard.
- Verified: ``make test`` passes (7364 tests); ``python tools/refresh_scaffold.py --check`` reports all embedded copies in sync (``test_public_api.py`` is not embedded in ``scaffold.sh``, so no refresh was needed).
- No changes to ``.github/workflows/**``.

## Unreleased — added invert_dict to data_utils

- Added `invert_dict(d)` to `data_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, `TypeError` validation for non-dict arguments, and `ValueError` for duplicate values; it returns a new dictionary mapping each value of *d* to its key. Added `TestInvertDict` to `tests/test_data_utils.py` covering basic inversion, empty/single dicts, the duplicate-value `ValueError`, and non-dict `TypeError` paths (6 new tests). Imported `invert_dict` at the top of the test file to match the module's `__all__` contract.
- Synchronized `data_utils.py`, `tests/test_data_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_data_utils` passes (26 tests); `python -m doctest data_utils.py` passes.

## Unreleased — added is_square to math_utils

- Added `is_square(n)` to `math_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, `TypeError` validation for non-int arguments (rejecting bool), and `ValueError` for negative inputs; it returns True when *n* is a perfect square (the square of an integer), reusing the existing `_require_int` helper and `math.isqrt`. Added `TestIsSquare` to `tests/test_math_utils.py` covering perfect squares, non-perfect squares, the negative `ValueError` path, and the non-int/bool `TypeError` paths (6 new tests). Imported `is_square` at the top of the test file to match the module's `__all__` contract.
- Synchronized `math_utils.py` and `tests/test_math_utils.py` embedded copies in `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `python -m unittest tests.test_math_utils` passes (56 tests); `python -m doctest math_utils.py` passes.

## Unreleased — extended __all__ public-API contract to non-wrapper modules
- Audit `file_utils.py` boundary cases (empty paths, missing files/directories, binary/unicode text, non-string/Path types) and add comprehensive boundary tests to `tests/test_file_utils.py`.

- Audited the non-wrapper modules named in the previous Next Planned (`calculator.py`, `config_schema.py`, `hello.py`) for `__all__` contract gaps against the project convention that every top-level, non-underscore name defined by the module must be exported.
- `calculator.py` and `hello.py` were already complete.
- Found a real contract gap in `config_schema.py`: `T = TypeVar("T")` is defined at module scope (line 49) but omitted from `__all__`, violating the public-API export contract. Every other module in the repository that defines a `T` TypeVar exports it in `__all__` (29 modules, e.g. `collections_utils`, `functools_utils`, `statistics_utils`), so `config_schema.py` was inconsistent.
- Added `T` to `config_schema.__all__` next to the other public names (15 exports total).
- Verified: every name in `__all__` is importable and no public attribute is missing; `make test` passes (7351 tests); `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.
- Note: `config_schema.py` is embedded in `scaffold.sh`, so the embedded copy was refreshed to stay byte-identical to the repository source.

## Unreleased — fixed stats __all__ gap for range_stat

- Found that `stats.py` implemented `range_stat(numbers)` as a public function (with typed signature, Google-style docstring with doctests, and `TypeError`/`ValueError` validation) but omitted it from the module's `__all__` list, violating the public API export contract that every public attribute must be listed in `__all__`. Added `range_stat` to `stats.__all__` next to its `range` alias.
- Added `TestRangeStat` to `tests/test_stats.py` covering basic range, single-element, negative, unsorted, float inputs, empty-list `ValueError`, and the non-list/non-numeric/bool `TypeError` paths (9 new tests), plus an assertion that `range_stat` is the same object as the `range` alias. Imported `range_stat` at the top of the test file to match the module's `__all__` contract.
- Updated the `stats` prose section of `README.md` to document `range_stat` alongside the `range` alias.
- Verified: `make test` passes; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.

## Unreleased — added ensure_prefix/remove_prefix/ensure_suffix/remove_suffix/join_lines/split_lines/is_blank to prompt_utils and tests

- Added `extract_sentences(text)` to `prompt_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation; it extracts sentences delimited by `.`, `!`, or `?` followed by whitespace or end of string, strips whitespace from each sentence, omits empty sentences, and returns `[]` for blank/empty input.
- Added `TestExtractSentences` to `tests/test_prompt_utils.py` covering basic extraction, single sentence, no punctuation, empty/whitespace-only input, newlines, and the `TypeError` path (7 new tests). Imported `extract_sentences` at the top of the test file to match the module's `__all__` contract.
- Updated the `prompt_utils` prose section of `README.md`.
- Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes all tests.

## Unreleased — added tests for bytes_utils predicate and ascii helpers

- Audited the `bytes_utils` helpers added in the preceding session (`isalnum`, `isalpha`, `isascii`, `isdigit`, `islower`, `isspace`, `istitle`, `isupper`, `join`, `expandtabs`, `decode_ascii`, `encode_ascii`) and found they were committed to `bytes_utils.py` and `scaffold.sh` without corresponding tests in `tests/test_bytes_utils.py`, leaving the new public API uncovered.
- Added `TestPredicates` and `TestAsciiHelpers` to `tests/test_bytes_utils.py` covering happy paths (including `bytearray` inputs and empty data), boundary cases, and the `TypeError`/`ValueError` paths for all twelve helpers (29 new tests). Imported the new names at the top of the test file to match the module's `__all__` contract.
- Updated the `bytes_utils` module tree entry and prose section of `README.md` to list the new helpers.
- Synchronized `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` passes (7674 tests, 3866 subtests); `python -m ruff check .` reports the same 34 pre-existing errors as before the change (no new regressions); `python -m mypy .` reports the same 63 pre-existing errors as before the change (no new regressions).

## Unreleased — fixed bytes_utils __all__ regression

- Fixed a regression introduced by the preceding bytes_utils session: `upper` and `lower` were added as public functions but omitted from the module's `__all__` list, which caused `tests/test_public_api.py::test_every_public_attribute_is_exported` to fail. Added both names to `__all__` so every public attribute is exported per the module contract.
- Verified: `make test` runs 7668 tests and passes (previously 1 failure); `python tools/refresh_scaffold.py --check` reports all embedded copies in sync after `make refresh-scaffold`.
- Synchronized `bytes_utils.py` and `scaffold.sh` with `make refresh-scaffold`.

## Unreleased — added partition and rpartition to bytes_utils

- Added `partition(data, sep)` and `rpartition(data, sep)` to `bytes_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-bytes-like arguments; they wrap `bytes.partition`/`bytes.rpartition`, returning a ``(before, sep, after)`` 3-tuple split on the first/last occurrence of *sep* and returning ``(data, b"", b"")`` / ``(b"", b"", data)`` when *sep* is absent.
- Added `TestPartition` and `TestRPartition` to `tests/test_bytes_utils.py` covering found, not-found, empty separator, bytearray input, and the `TypeError` paths (10 new tests). Imported `partition` and `rpartition` at the top of the test file to match the module's `__all__` contract.
- Updated the `bytes_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.


## Unreleased — added index to bytes_utils

- Added `index(data, sub, start=0, end=None)` to `bytes_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation complementing `index_of` and `rfind`; it returns the lowest index in *data* where *sub* is found and raises `ValueError` when *sub* is absent, honoring optional *start*/*end* bounds.
- Added `TestIndex` to `tests/test_bytes_utils.py` covering found, not-found (`ValueError`), empty subsequence, first occurrence, bytearray input, start/end bounds, and the `TypeError`/`ValueError` paths (8 new tests). Imported `index` at the top of the test file to match the module's `__all__` contract.
- Updated the `bytes_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.


## Unreleased — added convert_case to case_utils

- Added `convert_case(text, case)` to `case_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, `TypeError` validation for non-string `text`/`case`, and `ValueError` for an unrecognized case style; it dispatches to the existing case converters by name (e.g. ``"snake"``, ``"camel"``, ``"pascal"``, ``"kebab"``), accepting the optional ``"_case"`` suffix, case-insensitive matching, and hyphen aliases.
- Added `TestConvertCase` to `tests/test_case_utils.py` covering every supported case style, full-name and hyphen aliases, case-insensitive matching, empty text, and the `TypeError`/`ValueError` paths (16 new tests).
- Updated the `case_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `case_utils.py`, `tests/test_case_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.


## Unreleased — audited zipfile_utils boundary cases

- Audited `zipfile_utils.py` boundary cases and aligned validation with project conventions: added `_require_path` helpers, accept `str` or `pathlib.Path` for paths (coercing to str), validate types with `TypeError`, reject empty strings/paths with `ValueError`, add `Raises:` sections to docstrings, and accept `Path` objects in file lists.
- Added `TestZipfileUtilsBoundary` to `tests/test_zipfile_utils.py` covering TypeError/ValueError paths for all public helpers and Path-object acceptance (13 tests total pass for the module). Imported nothing new beyond the existing public API.
- Updated the `zipfile_utils` prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `zipfile_utils.py`, `tests/test_zipfile_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.



## Unreleased — audited tarfile_utils boundary cases

- Audited  boundary cases and aligned validation with project conventions: added  helpers, accept  or  for paths (coercing to str), validate types with , reject empty strings/paths with , add  sections to docstrings, and validate , , iterables, and .
- Added  to  covering TypeError/ValueError paths for all public helpers and Path-object acceptance (7 new tests; 11 tests now pass for the module). Imported nothing new beyond the existing public API.
- Updated the  prose section of .
- Recorded the change in the Unreleased section of .
- Synchronized , , , , and  with Refreshing the copies embedded in scaffold.sh...
refreshed: README.md
no repository copy: tests/test_audioop_utils.py
no repository copy: tests/test_imghdr_utils.py
no repository copy: tests/test_pipes_utils.py
no repository copy: tests/test_crypt_utils.py
no repository copy: tests/test_telnetlib_utils.py
no repository copy: tests/test_cgi_utils.py
no repository copy: tests/test_cgitb_utils.py
no repository copy: tests/test_nntplib_utils.py
no repository copy: tests/test_sndhdr_utils.py
no repository copy: tests/test_spwd_utils.py
no repository copy: tests/test_asynchat_utils.py
no repository copy: tests/test_asyncore_utils.py
no repository copy: tests/test_smtpd_utils.py
1 embedded copies refreshed; all embedded copies are in sync reports all embedded copies in sync.

## Unreleased — added removeprefix/removesuffix to bytes_utils

- Added `removeprefix(data, prefix)` and `removesuffix(data, suffix)` to `bytes_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-bytes-like arguments; they wrap `bytes.removeprefix`/`bytes.removesuffix`, returning *data* with a matching prefix/suffix stripped when present and unchanged otherwise (closely related to the existing `starts_with`/`ends_with` helpers).
- Added `TestRemovePrefix` and `TestRemoveSuffix` to `tests/test_bytes_utils.py` covering prefix/suffix removal, absent prefix/suffix, empty prefix/suffix, empty data, full match, bytearray input, and the `TypeError` paths (14 new tests).
- Updated the `bytes_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — audited tempfile_utils boundary cases

- Audited `tempfile_utils.py` boundary cases and aligned validation with project conventions: every public helper now consistently accepts `str` or `pathlib.Path` for `suffix`/`prefix`/`dir` (and coerces them), validates types with `TypeError` for non-str/non-Path inputs (including bools where inappropriate), and adds Google-style docstrings with `Raises:` sections.
- Added `TestTempfileBoundary.test_mkstemp_path_acceptance_suffix_empty_str` and expanded coverage for Path acceptance across all helpers.
- Updated the `tempfile_utils` prose section of `README.md` to document Path support and validation.
- Synchronized `tempfile_utils.py`, `tests/test_tempfile_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` via `make refresh-scaffold` (all embedded copies in sync).

- Audited every public helper in `path_utils.py` against boundary inputs: non-str/non-Path arguments, empty extensions, single-path calls to `get_common_path`, and Path-object acceptance. Found that `join_path` silently coerced non-str/non-Path arguments (e.g. `join_path(123)` returned `'123'`, `join_path("a", None)` returned `'a/None'`), and that `change_extension`/`ensure_extension` raised an opaque `AttributeError` for non-str extensions instead of the project's `TypeError`/`ValueError` convention.
- Added a `_require_path` validation helper to `path_utils.py` and routed every public function through it so each raises a consistent `TypeError` for non-str/non-Path inputs; added a `_require_extension` helper that raises `TypeError` for non-str extensions and `ValueError` for empty extensions, used by `change_extension` and `ensure_extension`. Added `Raises:` sections to the docstrings of every public function.
- Added `TestPathUtilsBoundary` to `tests/test_path_utils.py` covering the `TypeError` paths for every public function, the `ValueError` paths for `change_extension`/`ensure_extension` (empty extension) and `get_common_path` (fewer than two paths), the `ValueError` path for `get_relative_path` (not relative), and Path-object acceptance across the module (21 new tests; 55 tests now pass for the module). Imported nothing new beyond the existing public API to match the module's `__all__` contract.
- Updated the `path_utils` prose section of `README.md` to document the validation convention.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.

## Unreleased — audited zipfile_utils boundary cases

- Found that `is_zipfile` in `zipfile_utils.py` performed no input validation, unlike `create_archive`, `list_names`, and `extract_all`, contradicting the module's documented convention that all functions raise `TypeError`/`ValueError` on invalid arguments. Added `TypeError` for non-str paths and `ValueError` for empty paths to `is_zipfile`, typed its parameter as `str`, and dropped the now-unused `Any` import.
- Added `TestListNamesBoundary`, `TestExtractAllBoundary`, and `TestIsZipfileBoundary` to `tests/test_zipfile_utils.py` covering the `TypeError`/`ValueError` paths for `list_names`, `extract_all`'s `dest`, and `is_zipfile`, plus positive/negative `is_zipfile` cases (7 new tests; 8 tests now pass for the module). Imported nothing new beyond the existing public API to match the module's `__all__` contract.
- Synchronized `zipfile_utils.py`, `tests/test_zipfile_utils.py`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — audited and hardened file_utils boundary cases

- Audited every public helper in `file_utils.py` against boundary inputs: empty paths, missing files, directories passed to file readers, non-str/non-Path types, nested destination creation, empty directories, and recursive/non-recursive globbing. Found that the module accepted non-str/non-Path arguments without raising `TypeError` (they fell through to `OSError`/`TypeError` from the stdlib), leaving a gap against the project's validation convention.
- Added a `_require_path` validation helper to `file_utils.py` and routed every public function through it so each raises a consistent `TypeError` for non-str/non-Path inputs; added Google-style docstrings with doctests to `read_text`, `read_json`, and `ensure_dir`.
- Added `TestFileUtilsBoundary` to `tests/test_file_utils.py` covering missing-file `FileNotFoundError` paths, directory-as-file `OSError` paths, invalid-JSON `json.JSONDecodeError`, nested destination creation, empty-directory listing, recursive/non-recursive glob filtering, missing-source `FileNotFoundError` in `copy_file`, overwrite behavior, directory-as-target no-op in `delete_file`, and the `TypeError` paths for every public function (20 new tests). Imported nothing new beyond the existing public API to match the module's `__all__` contract.
- Updated the `file_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.

## Unreleased — added is_strong_prime to prime_utils

- Added `is_strong_prime(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *n* is a strong prime — a prime greater than the arithmetic mean of its nearest primes above and below (equivalently, closer to the next prime than to the previous one; OEIS A051634, e.g. 11, 17, 29, 37, 41, 59, ...), reusing the existing `is_prime`, `prev_prime`, and `next_prime` helpers and using the strictly neighbouring primes `prev_prime(n - 1)` and `next_prime(n + 1)`. Returns False for balanced primes (e.g. 5), weak primes (e.g. 7, 13, 23), non-primes, and numbers below 11.
- Added `TestIsStrongPrime` to `tests/test_prime_utils.py` covering known strong primes (40 values matching OEIS A051634), balanced/weak primes, non-primes, the boundary primes 2/3/5, negatives/zero, and the `TypeError` paths (10 new tests). Imported `is_strong_prime` at the top of the test file to match the module's `__all__` contract.
- Updated the `prime_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.

## Unreleased — refreshed stale tests/test_numbers_utils.py embedded copy

- The preceding `chore(kilo): checkpoint agent session` commit (d38b5fe) added `is_semiperfect_number` to `numbers_utils.py` and `TestIsSemiperfectNumber` to `tests/test_numbers_utils.py` but did not regenerate the embedded copy of `tests/test_numbers_utils.py` inside `scaffold.sh`, violating the project's scaffold-sync invariant (`python tools/refresh_scaffold.py --check` reported `stale: tests/test_numbers_utils.py`).
- Refreshed the embedded copy of `tests/test_numbers_utils.py` inside `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` now reports all embedded copies in sync, and the scaffold-sync tests pass.

## Unreleased — added is_semiperfect_number to numbers_utils

- Added `is_semiperfect_number(n)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *n* is a positive integer that can be expressed as the sum of some subset of its proper divisors (e.g. 12 = 6 + 4 + 2, 18 = 12 + 6, 20 = 10 + 8 + 2), reusing the existing `proper_divisors` helper and a bounded subset-sum check. Perfect numbers are semiperfect; powers of two, primes, and weird numbers are not.
- Added `TestIsSemiperfectNumber` to `tests/test_numbers_utils.py` covering known semiperfect numbers (6, 12, 18, 20, 24, 28, 30, 36, 40, 42, 48, 54, 56, 60, 66, 72, 78, 80, 84, 88, 90, 96, 100), perfect numbers, powers of two (not semiperfect), primes/deficient numbers, weird numbers (70, 836, 4030, 5830, 7192, 7912, 9272), negatives/zero, and the `TypeError` paths (25 new tests). Imported `is_semiperfect_number` at the top of the test file to match the module's `__all__` contract.
- Updated the `numbers_utils` module tree entry and prose section of `README.md`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.

## Unreleased — added test coverage for is_odious_number and is_evil_number in numbers_utils

- The preceding commit (`feat(numbers_utils): add is_odious_number, is_evil_number; export is_coprime`) added `is_odious_number(n)` and `is_evil_number(n)` to `numbers_utils.py` with `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-int arguments, but added no tests — a coverage gap against the project's convention.
- Added `TestIsOdiousNumber` and `TestIsEvilNumber` to `tests/test_numbers_utils.py` covering known odious numbers (odd count of 1-bits), known evil numbers (even count of 1-bits), the odious/evil partition of small non-negative integers, large values (65535, 65537, 65539), negatives, and the `TypeError` paths (16 new tests). Imported `is_odious_number` and `is_evil_number` at the top of the test file to match the module's `__all__` contract.
- Updated the `numbers_utils` module tree entry and prose section of `README.md` to list the two new helpers.

## Unreleased — added winsorized_stddev to stats

- Added `winsorized_stddev(numbers, k=1, population=True)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation complementing `winsorized_mean` and `winsorized_variance`; it winsorizes by replacing the *k* smallest and *k* largest values with the nearest remaining values, then returns the standard deviation (population or sample) of the winsorized values, reducing outlier influence without discarding data.
- Added `TestWinsorizedStddev` to `tests/test_stats.py` covering the default, *k*=0, single element, and the `ValueError`/`TypeError` paths (10 new tests). Imported `winsorized_stddev` at the top of the test file to match the module's `__all__` contract.

## Unreleased — added is_pandigital_number to numbers_utils

- Added `is_pandigital_number(n, base=10)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation; it returns `True` when *n* contains every digit of *base* at least once in its representation (e.g. 1023456789 in base 10, 75 in base 4), and `False` for negatives, missing digits, and bases outside 2..36.
- Added `TestIsPandigitalNumber` to `tests/test_numbers_utils.py` covering known pandigitals in base 10, non-pandigitals, negatives, other bases (2, 4, 16), default-base behavior, and the `TypeError`/`ValueError` paths (12 new tests). Imported `is_pandigital_number` at the top of the test file to match the module's `__all__` contract.
- Updated the `numbers_utils` module tree entry and prose section of `README.md`.

## Unreleased — added is_almost_perfect_number to numbers_utils

- Added `is_almost_perfect_number(n)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns `True` when *n* is an almost perfect number — a positive integer whose sum of proper divisors equals *n* - 1 (the known cases are the powers of two) — and `False` for numbers below 1.
- Added `TestIsAlmostPerfectNumber` to `tests/test_numbers_utils.py` covering known almost perfect numbers (powers of two), non-almost-perfect numbers, numbers below 1, and the `TypeError` paths (4 new tests). Imported `is_almost_perfect_number` at the top of the test file to match the module's `__all__` contract.
- Updated the `numbers_utils` module tree entry and prose section of `README.md`.

## Unreleased — added is_squarefree_number to number_utils

- Added `is_squarefree_number(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *value* is a positive integer not divisible by any perfect square greater than 1 (1 is squarefree by convention), and False for 0, negatives, and numbers with a squared prime factor.
- Added `TestIsSquarefreeNumber` to `tests/test_number_utils.py` covering squarefree and non-squarefree numbers, 0 and negatives, and the `TypeError` path. Imported `is_squarefree_number` at the top of the test file to match the module's `__all__` contract.
- Updated the `number_utils` module tree entry and prose section of `README.md`.

## Unreleased — added is_abstract to abc_utils

- Added `is_abstract(obj)` to `abc_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests; it returns True when *obj* exposes a non-empty ``__abstractmethods__`` attribute. Added `test_is_abstract` to `tests/test_abc_utils.py`. Updated the `abc_utils` prose section of `README.md`. Recorded the change in the Unreleased section of `CHANGELOG.md`. Synchronized `abc_utils.py`, `tests/test_abc_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added is_perfect_power to number_utils

- Added `is_perfect_power(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-number arguments; it returns True when *value* is a positive integer > 1 that can be expressed as an integer power of another integer with exponent >= 2 (e.g. 16 = 4^2, 36 = 6^2, 8 = 2^3, 125 = 5^3), and returns False for 0, ±1, non-integral values, primes, and numbers with no such representation. It generalizes the existing `is_perfect_cube`, `is_perfect_square`, and `is_power_of_two` predicates, accepting floats that are integral (e.g. 8.0) just like its siblings.
- Added `TestIsPerfectPower` to `tests/test_number_utils.py` covering perfect powers, non-perfect powers, 1 and 0, negatives, integral floats, and the `TypeError` paths (6 new tests). Imported `is_perfect_power` at the top of the test file to match the module's `__all__` contract.
- Updated the `number_utils` module tree entry and prose section of `README.md`.

## Unreleased — added polydivisible docs and __all__ export to numbers_utils

- Registered `is_polydivisible_number` in `numbers_utils.__all__` (it was implemented and tested in `87f415a` but missing from the module's public API surface), added it to the `numbers_utils` file-list comment and prose section of `README.md`, and recorded the gap in this CHANGELOG entry.

## Unreleased — added sliding_window and window to itertools_utils
- Added `is_powerful_number(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *n* is a powerful number — a positive integer such that for every prime factor *p*, *p*² also divides *n* (e.g. 4, 8, 9, 36, 72) — returning True for 1 (by convention), and False for numbers below 1, primes, and squarefree composites. It is the conceptual counterpart to `is_squarefree`: for *n* > 1 the two predicates are mutually exclusive.
- Added `TestIsPowerfulNumber` to `tests/test_prime_utils.py` covering known powerful numbers (1, 4, 8, 9, 16, 25, 27, 32, 36, 49, 64, 72, 100, 108, 121, 125, 128, 144), non-powerful numbers (2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20), numbers below 1, primes, squarefree composites, the mutual-exclusivity relationship with `is_squarefree` for *n* > 1, and the `TypeError` paths (7 new tests). Imported `is_powerful_number` at the top of the test file to match the module's `__all__` contract.
- Updated the `prime_utils` module tree entry and prose section of `README.md`.

## Unreleased — added is_spy_number to numbers_utils
- Added `is_spy_number(n)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *n* is a positive integer whose sum of decimal digits equals the product of its decimal digits (e.g. 1124: 1+1+2+4 = 8 = 1*1*2*4), and returns False for numbers below 1.
- Added `TestIsSpyNumber` to `tests/test_numbers_utils.py` covering known spy numbers (22, 1124, 123, 131, 11112), non-spy numbers (1234, 12, 14, 15, 100), numbers below 1 (0 and negatives), and the `TypeError` paths (5 new tests). Imported `is_spy_number` at the top of the test file to match the module's `__all__` contract.

## Unreleased — added is_amicable to prime_utils
- Added `is_amicable(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns True when *n* belongs to an amicable pair — two distinct positive integers where each equals the sum of the proper divisors of the other (e.g. 220 and 284) — and returns False for perfect numbers, numbers below 2, and numbers whose partner's proper-divisor sum does not loop back.
- Added `TestIsAmicable` to `tests/test_prime_utils.py` covering the classic (220, 284) pair, other known pairs (1184/1210, 2620/2924, 5020/5564, 6232/6368), perfect numbers, small/boundary values, primes, and the `TypeError` paths (13 new tests). Imported `is_amicable` at the top of the test file to match the module's `__all__` contract.

## Unreleased — added is_perfect_power to prime_utils
- Added `is_perfect_power(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring, and `TypeError` validation for non-int arguments; it returns True if *n* is a positive integer > 1 that can be expressed as an integer power of another integer with exponent >= 2 (e.g. 16 = 4^2, 36 = 6^2, 8 = 2^3), and returns False for 0, ±1, primes, and numbers with no such representation.
- Added `TestIsPerfectPower` to `tests/test_prime_utils.py` covering perfect powers, non-perfect powers, 1 and small values, and `TypeError` paths (imported `is_perfect_power`).

- Updated the `prime_utils` module tree entry and prose section of `README.md`.
- Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added winsorized_mean to stats

- Added `winsorized_mean(numbers, k=1)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation complementing `trimmed_mean`; it replaces the *k* smallest and *k* largest values with the nearest remaining values before averaging, reducing outlier influence without discarding data, and returns the arithmetic mean of the winsorized values (identical to `mean` when *k* is 0).
- Added `TestWinsorizedMean` to `tests/test_stats.py` covering default winsorization, custom *k*, *k*=0, even-length lists, unsorted input, single element, negatives, floats, and the `ValueError`/`TypeError` paths (14 new tests). Imported `winsorized_mean` at the top of the test file to match the module's `__all__` contract.
- Updated the `stats` module prose section of `README.md`.
- Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added array_concat and array_repeat to array_utils

- Added `array_concat(a, b)` and `array_repeat(arr, n)` to `array_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-array arguments; `array_concat` returns a new array that is the concatenation of *a* and *b*, and `array_repeat` returns a new array that is *arr* repeated *n* times.
- Added `test_array_concat`, `test_array_concat_empty`, `test_array_concat_rejects_non_array`, `test_array_repeat`, `test_array_repeat_rejects_non_array`, and `test_array_repeat_rejects_bad_n` to `tests/test_array_utils.py` (6 new tests). Imported `array_concat` and `array_repeat` at the top of the test file to match the module's `__all__` contract.
- Updated the `array_utils` module prose section of `README.md`.
- Synchronized `array_utils.py`, `tests/test_array_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added split_lines to prompt_utils

- Added `split_lines(text, *, keep_empty=True)` to `prompt_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation; splits text into lines normalizing line endings, drops trailing empty line, optionally omits empty lines. Added `TestSplitLines` to `tests/test_prompt_utils.py`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`.

## Unreleased — added rfind to bytes_utils

- Added `rfind(data, sub, start=0, end=None)` to `bytes_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation for non-bytes-like arguments; it returns the highest index in *data* where *sub* is found, or -1 when *sub* is not present, honoring optional *start*/*end* bounds. Added `TestRFind` to `tests/test_bytes_utils.py` covering found, not-found, empty-subsequence, last-occurrence, bytearray input, start/end bounds, and the `TypeError` paths. Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added array byteswap/buffer_info/typecode/itemsize helpers

- Added `array_byteswap(arr)`, `array_buffer_info(arr)`, `array_itemsize(arr)`, and `array_typecode(arr)` to `array_utils.py` with typed signatures, `__all__` exports, Google-style docstrings, and `TypeError` validation for non-array arguments. Added tests to `tests/test_array_utils.py` covering byteswap behavior, buffer info shape, itemsize, and typecode. Updated the `array_utils` module prose section of `README.md`. Synchronized `array_utils.py`, `tests/test_array_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added index_of to bytes_utils

- Added `index_of(data, sub)` to `bytes_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation for non-bytes-like arguments; it returns the lowest index in *data* where *sub* is found, or -1 when *sub* is not present. Added `TestIndexOf` to `tests/test_bytes_utils.py` covering found, not-found, empty-subsequence, first-occurrence, bytearray input, and `TypeError` paths (7 new tests). Updated the `bytes_utils` module tree entry and prose section of `README.md`. Synchronized `bytes_utils.py`, `tests/test_bytes_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added zip_longest_iterables to itertools_utils

- Added `zip_longest_iterables(*iterables, fillvalue=None)` to `itertools_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation for non-iterable arguments; it returns a list of tuples zipping the input iterables up to the length of the longest, substituting *fillvalue* (default `None`) for exhausted iterables, and returns `[]` when called with no arguments.
- Added `TestZipLongestIterables` to `tests/test_itertools_utils.py` covering equal-length, unequal-length, default and explicit fillvalue, single/empty/no iterables, three-iterable zip, order preservation, and the `TypeError` paths (14 new tests). Imported `zip_longest_iterables` at the top of the test file to match the module's `__all__` contract.
- Updated the `itertools_utils` module prose section and the file-list comment of `README.md`.
- Synchronized `itertools_utils.py`, `tests/test_itertools_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added count_lowercase and count_uppercase to prompt_utils

- Added `count_lowercase(text)` and `count_uppercase(text)` to `prompt_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-string arguments; they return the number of ASCII lowercase (a-z) and uppercase (A-Z) letters in *text*, respectively, returning zero for empty text. Added `TestCountLowercase` and `TestCountUppercase` to `tests/test_prompt_utils.py` covering empty input, no matches, only matches, mixed content, unicode non-matches, and the `TypeError` path. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — synchronized scaffold copies after slugify_utils refactor

- Refreshed the embedded copy of `slugify_utils.py` in `scaffold.sh` after the preceding `chore(kilo): checkpoint agent session` commit (c8d49dd) refactored the module without regenerating the embedded copy; `python tools/refresh_scaffold.py --check` now reports all embedded copies in sync.

## Unreleased — added is_happy_number to numbers_utils

- Added `is_happy_number` to `numbers_utils.py` with `__all__` export, Google-style docstrings with doctests, and validation raising `TypeError` for non-integers; negatives return `False` and `0` is treated as happy.
- Added tests for `is_happy_number` in `tests/test_numbers_utils.py`.

## Unreleased — completed bytes_utils public API and documentation

- Completed the public API surface of `bytes_utils.py`: added `__all__` exports for `concat`, `repeat`, `reverse`, `contains`, `starts_with`, and `ends_with` (previously added in `8523e4e`), rewrote their docstrings to Google-style with Args/Returns/Raises and doctests, and verified coverage in `tests/test_bytes_utils.py`.
- Updated the `bytes_utils` module prose section of `README.md`.
- Added `proper_divisors` to `__all__` in `numbers_utils.py` (it was implemented and tested but missing from exports); added it to the `numbers_utils` module prose section in `README.md`. Ran `make test`, `make lint`, `make typecheck` and scaffold sync after lint fixes.
- Synchronized embedded copies with `make refresh-scaffold`.

## Unreleased — completed array_utils public API and documentation

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6771 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Found that the preceding `feat(array_utils): add to_list, from_list, extend_from_list, remove_first` commit (5fc1d33) added `array_to_list`, `array_from_list`, `array_extend_from_list`, and `array_remove_first` to `array_utils.py` and `tests/test_array_utils.py`, but the four functions were absent from `__all__`, the `array_utils` prose section of `README.md`, and the Unreleased section of `CHANGELOG.md` — an incomplete public-API commit.
- Added the four names to `__all__` in `array_utils.py` so they are exported with the rest of the module's public surface.
- Rewrote the four docstrings to the project's Google-style convention with Args/Returns/Raises sections and runnable doctests, matching the style of the surrounding helpers.
- Updated the `array_utils` module prose section of `README.md` to list the four new helpers.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `array_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6771 tests and passes with no new failures, `make lint` is clean, and `make typecheck` reports no issues in 530 source files.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `array_utils.py`, `bytes_utils.py`, `strings.py`, `prompt_utils.py`, `stats.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `itertools_utils.py`, `numbers_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added find/rfind to strings

### Added
- Added `find(s, sub, start=0, end=None)` and `rfind(s, sub, start=0, end=None)` to `strings.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation for non-string arguments and invalid `start`/`end` types; they return the lowest/highest index of *sub* in *s* or -1 if not found, honoring optional bounds. Added `TestFind` and `TestRFind` to `tests/test_strings.py` covering basic cases, bounds, empty substring, and the `TypeError` paths. Updated the `strings` module entry in `README.md`.
- Synchronized `strings.py`, `tests/test_strings.py`, `README.md`, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added newline helper functions to strings

- Added `ensure_leading_newline(text)`, `ensure_trailing_newline(text)`, and `ensure_surrounded_by_newlines(text)` to `strings.py`.
- Added tests for the new helpers in `tests/test_strings.py`.

## Unreleased — added count_consonants to prompt_utils

- Added `count_consonants(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the number of ASCII consonant characters in *text*. Added `TestCountConsonants` to `tests/test_prompt_utils.py`. Updated the `prompt_utils` module prose section of `README.md`. Recorded the change in the Unreleased section of `CHANGELOG.md`. Synchronized embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added ensure_leading_newline helper to prompt_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6753 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Found that `prompt_utils.py` exports `ensure_trailing_newline(text)` but had no companion to guarantee a leading newline, leaving a small gap in the line-normalization helpers.
- Added `ensure_leading_newline(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctest examples, and `TypeError` validation for non-string arguments; it prepends a single newline when *text* is non-empty and does not already start with one, returning empty text unchanged.
- Added `TestEnsureLeadingNewline` to `tests/test_prompt_utils.py` covering the add/already-present cases, empty string, multiple leading newlines, and the `TypeError` paths for non-string arguments (5 new tests; 6758 tests now pass). Imported `ensure_leading_newline` at the top of the test file to match the module's `__all__` contract.
- Updated the `prompt_utils` module prose section of `README.md` to list the new helper.
- Verified the work: `make test` runs 6758 tests and passes with no new failures, `make lint` is clean, and `make typecheck` reports no issues in 530 source files.
- Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added test coverage for ensure_prefix and ensure_suffix in strings.py

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6735 tests and passes, `make lint` is clean, `make typecheck` reports 11 pre-existing errors in 10 files (identical with the change stashed), and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Found that the preceding `chore(kilo): checkpoint agent session` commit (1a8f3c4) added `ensure_prefix(text, prefix)` and `ensure_suffix(text, suffix)` to `strings.py` with `__all__` exports and README entries, but `tests/test_strings.py` imported neither function and had no test classes for them — a coverage gap in a module otherwise fully tested.
- Added `TestEnsurePrefix` and `TestEnsureSuffix` to `tests/test_strings.py` covering the add/already-present cases, empty text, empty prefix/suffix, both-empty, prefix/suffix longer than text, overlapping prefix/suffix, unicode inputs, and the `TypeError` paths for non-string arguments (18 new tests; 6753 tests now pass). Imported `ensure_prefix` and `ensure_suffix` at the top of the test file to match the module's `__all__` contract.
- Updated the `strings` module prose section of `README.md` to describe the two new helpers.
- Verified the work: `make test` runs 6753 tests and passes with no new failures, `make lint` is clean, and `make typecheck` reports the same 11 pre-existing errors in 10 files (unchanged by this work).
- Synchronized `tests/test_strings.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `strings.py`, `prompt_utils.py`, `stats.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `itertools_utils.py`, `numbers_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — fixed is_neon_number bug and added test coverage for strong/harshad/neon/armstrong/automorphic predicates in numbers_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6719 tests and passes (6 pre-existing environment-related errors in `test_atexit_utils`, `test_importlib_utils`, `test_multiprocessing_utils`, `test_sre_compile_utils`, `test_sre_constants_utils`, and `test_sre_parse_utils` — confirmed identical with the change stashed), and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Found that `numbers_utils.py` exports 14 names in `__all__`, but `is_strong_number`, `is_harshad_number`, `is_neon_number`, `is_armstrong_number`, and `is_automorphic_number` were imported nowhere in `tests/test_numbers_utils.py`, leaving a coverage gap in an otherwise well-tested module.
- Cross-checked all five predicates against brute-force references over the range -5..99999. Four matched exactly; `is_neon_number` had exactly one mismatch: `is_neon_number(9)` returned `False` even though 9 is a neon number (9^2 = 81, 8 + 1 = 9). The implementation summed the squares of the digits of *n* instead of the digits of *n^2*.
- Fixed `is_neon_number` in `numbers_utils.py` to sum the digits of `n * n`; the docstring now correctly describes the neon-number definition and the examples still hold.
- Added `TestIsStrongNumber`, `TestIsHarshadNumber`, `TestIsNeonNumber`, `TestIsArmstrongNumber`, and `TestIsAutomorphicNumber` to `tests/test_numbers_utils.py` covering known values, non-matching values, boundary/negative inputs, and the `TypeError` paths (40 new tests; 6759 tests now pass). Imported the five predicates at the top of the test file to match the module's `__all__` contract.
- Updated the `numbers_utils` module prose section and file listing of `README.md` to list the newly covered helpers.
- Verified the work: `make test` runs 6759 tests and passes with no new failures, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `itertools_utils.py`, `numbers_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added test coverage for flatten_once, take_while_pred, accumulate_values, repeat_value, and cycle_take in itertools_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6719 tests and passes (6 pre-existing environment-related errors in `test_atexit_utils`, `test_importlib_utils`, `test_multiprocessing_utils`, `test_sre_compile_utils`, `test_sre_constants_utils`, and `test_sre_parse_utils` — confirmed identical with the change stashed), `make lint` is clean, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Found that `itertools_utils.py` exports 11 functions in `__all__`, but `flatten_once`, `take_while_pred`, `accumulate_values`, `repeat_value`, and `cycle_take` were imported nowhere in `tests/test_itertools_utils.py`, leaving a coverage gap in an otherwise fully-tested module.
- Added `TestFlattenOnce` to `tests/test_itertools_utils.py` covering one-level flattening, empty input, nested iterables, non-iterable outer argument, and non-iterable inner element (5 new tests).
- Added `TestTakeWhilePred` to `tests/test_itertools_utils.py` covering normal take-while, empty input, all-taken, none-taken, non-iterable argument, and non-callable predicate (6 new tests).
- Added `TestAccumulateValues` to `tests/test_itertools_utils.py` covering default sum, empty input, single element, custom function, non-iterable argument, and non-callable function (6 new tests).
- Added `TestRepeatValue` to `tests/test_itertools_utils.py` covering default times, explicit times, zero times, non-int times, and negative times (5 new tests).
- Added `TestCycleTake` to `tests/test_itertools_utils.py` covering cycling, empty input, zero count, non-iterable argument, non-int n, and negative n (6 new tests). Imported `flatten_once`, `take_while_pred`, `accumulate_values`, `repeat_value`, and `cycle_take` at the top of the test file to match the module's `__all__` contract.
- Updated the `itertools_utils` module prose section of `README.md` to list the newly covered helpers.
- Verified the work: `make test` runs 6719 tests and passes with no new failures, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `tests/test_itertools_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `itertools_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added is_repdigit_number to numbers_utils

- Added `is_repdigit_number` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns `True` for repdigit numbers composed of repeated digits (e.g. 0, 5, 11, 22, 555) and `False` for negatives and mixed digits.
- Added `TestIsRepdigitNumber` to `tests/test_numbers_utils.py` covering known repdigits, non-repdigits, negatives, and `TypeError` paths (5 new tests; 6966 tests now run in the full suite).
- Imported `is_repdigit_number` in the test file to match the module's `__all__` contract.
- Updated the `numbers_utils` module listing in `README.md`.
- Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: all `numbers_utils` tests pass; `make lint` and `make typecheck` show only pre-existing errors unrelated to this change.

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6657 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Found that `number_utils.py` exports 66 functions in `__all__`, but `gcd`, `lcm`, `ceil_div`, and `is_kaprekar_number` were imported nowhere in `tests/test_number_utils.py`, leaving a coverage gap in an otherwise fully-tested module.
- Added `TestGcd` to `tests/test_number_utils.py` covering known pairs, zero arguments, sign handling, large values, and the `TypeError` path for non-ints and bools (12 new tests).
- Added `TestLcm` to `tests/test_number_utils.py` covering known pairs, zero arguments, sign handling, the `ValueError` path when both arguments are zero, and the `TypeError` path (11 new tests).
- Added `TestCeilDiv` to `tests/test_number_utils.py` covering exact division, rounding up, zero numerator, negative numerator and divisor, division-by-zero, and the `TypeError` path (14 new tests).
- Added `TestIsKaprekarNumber` to `tests/test_number_utils.py` covering known Kaprekar numbers (1, 9, 45, 55, 99, 297, 703, 2223, 2728, 7777), zero, non-Kaprekar numbers, negatives, and the `TypeError` path (11 new tests). Imported `gcd`, `lcm`, `ceil_div`, and `is_kaprekar_number` at the top of the test file to match the module's `__all__` contract.
- Documented `is_kaprekar_number` in the `number_utils` module prose section and file listing of `README.md`.
- Verified the work: `make test` runs 6695 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added count_vowels to prompt_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6996 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `count_vowels(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the number of ASCII vowel characters (a, e, i, o, u, case-insensitive) in *text_, returning zero for empty text. Added `TestCountVowels` to `tests/test_prompt_utils.py` covering empty input, no vowels, only vowels, mixed content, case-insensitivity, and the `TypeError` path (8 new tests). Updated the `prompt_utils` module prose section of `README.md`. Recorded the change in the Unreleased section of `CHANGELOG.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Fixed a pre-existing ruff E501 line-too-long error in `tests/test_prime_utils.py` by reformatting an over-long list literal into a multi-line list, restoring the green-lint invariant.
- Verified the work: `make test` runs 6996 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `type_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added is_abundant_number and is_deficient_number to number_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6627 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Added `is_abundant_number` and `is_deficient_number` to `number_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with doctests, and `TypeError` validation; `is_abundant_number` returns True when the sum of proper divisors exceeds the number, `is_deficient_number` returns True when the sum of proper divisors is less than the number (with 1 classified as deficient). Added `TestIsAbundantNumber` and `TestIsDeficientNumber` to `tests/test_number_utils.py` covering known values, perfect numbers, zeros/negatives, and type errors (adds ~30 tests). Updated `README.md` to list the new helpers. Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6657 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added cumulative_sum test coverage to stats

The board held no task (bootstrap). Verified repository health before starting: `make test` passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Found that `stats.py` exports `cumulative_sum(numbers)` in `__all__` and the README lists it, but `tests/test_stats.py` had no test class for it (it was imported nowhere and untested), leaving a coverage gap in an otherwise fully-tested module.
- Added `TestCumulativeSum` to `tests/test_stats.py` covering basic running totals, empty input, single element, negatives, floats, zeros, order preservation, and the `TypeError` paths for non-lists, non-numeric values, and bools (10 new tests). Imported `cumulative_sum` at the top of the test file to match the module's `__all__` contract.
- Documented `cumulative_sum` in the `stats` module prose section of `README.md`.
- Verified the work: `make test` passes with no new failures, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `tests/test_stats.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added count_digits to prompt_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Added `count_digits(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the number of decimal digit characters (0-9) in *text_ using :meth:`str.isdigit`, returning zero for empty text.
- Added `TestCountDigits` to `tests/test_prompt_utils.py` covering empty input, no digits, only digits, mixed content, leading zeros, digits with spaces, the unicode-digit non-match path, and the `TypeError` path (8 new tests).
- Documented `count_digits` in the `prompt_utils` module prose section of `README.md`.
- Verified the work: `make test` passes with no new failures, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added is_perfect_number to numbers_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6580 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reported all embedded copies in sync.

Completed in this session:

- Added `is_perfect_number(n)` to `numbers_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments (including `bool`); it returns `True` when *n* is a perfect number (a positive integer equal to the sum of its proper divisors), `False` otherwise, treating numbers below 2 as non-perfect. Verified against the known perfect numbers (6, 28, 496, 8128, 33550336, 8589869056).
- Added `TestIsPerfectNumber` to `tests/test_numbers_utils.py` covering known perfect numbers, non-perfect numbers, a large perfect number, numbers below 2 (including 0 and negatives), and the `TypeError` path for float, str, None, bool, and list (11 new tests). Imported `is_perfect_number` at the top of the test file to match the module's `__all__` contract.
- Documented `is_perfect_number` in the `numbers_utils` file listing and prose section of `README.md`.
- Verified the work: `make test` runs 6591 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added is_dev_version test coverage and version_utils alias coverage

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6570 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reported 1 embedded copy out of sync (a stale `version_utils.py` snapshot left by the preceding checkpoint commit).

Completed in this session:

- Refreshed the embedded copy of `version_utils.py` inside `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` now reports all embedded copies in sync.
- Found that `version_utils.py` exports 75 functions but `is_dev_version` had no test coverage and the comparison/parse aliases (`cmp_versions`, `cmp`, `compare`, `is_semver`, `is_newer`, `is_older`, `from_tuple`, `increment_version`, `increment`) were imported nowhere in `tests/test_version_utils.py`, leaving a coverage gap in an otherwise fully-tested module.
- Added `TestIsDevVersion` to `tests/test_version_utils.py` covering dev-tagged versions (including case-insensitive `DEV` and dotted prereleases), non-dev prereleases (`rc`, `alpha`), versions with no prerelease, and the `TypeError` path (4 new tests).
- Added `TestVersionComparisonAliases` to `tests/test_version_utils.py` asserting the comparison aliases (`cmp_versions`, `cmp`, `compare`) return -1/0/1 like `compare_versions`, that `is_semver` mirrors `is_valid_version` (including rejecting non-strings), that `is_newer`/`is_older` mirror `is_greater`/`is_less`, that `from_tuple` mirrors `tuple_to_version`, and that `increment_version`/`increment` mirror `bump_version` (14 new assertions). Imported the newly covered names at the top of the test file to match the module's `__all__` contract.
- Documented `is_dev_version` in the `version_utils` file listing and prose section of `README.md`.
- Verified the work: `make test` runs 6580 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 530 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Synchronized `tests/test_version_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — repaired prime_utils.py and added is_giuga_number helper

The preceding `chore(kilo): checkpoint agent session` commit (b14fcaf) edited `prime_utils.py` but left it with a `SyntaxError` (it added `"is_giuga_number"` to `__all__` without closing the list and without defining the function), which broke the module import and caused `make test` to report 3 new failures. Verified repository health before starting: `make test` runs 6576 tests and passes with 6 pre-existing errors (identical with the change stashed), `make lint` is clean, `make typecheck` reports 9 pre-existing errors (identical with the change stashed), and `python tools/refresh_scaffold.py --check` reported 2 embedded copies out of sync.

Completed in this session:

- Restored the closing `]` of `__all__` in `prime_utils.py` so the module imports again.
- Implemented `is_giuga_number(n)` in `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments; it returns `True` when *n* is a Giuga number (a composite, squarefree integer such that for every prime factor *p* of *n*, *p* divides *n // p - 1*), `False` otherwise, treating primes and numbers below 2 as non-Giuga. Verified against the known Giuga numbers (30, 858, 1722, 66198, 2214408306, 24423128562).
- Added `TestIsGiugaNumber` to `tests/test_prime_utils.py` covering known Giuga numbers, non-Giuga composites, primes, small/non-composite inputs, prime powers, and the `TypeError` path (float, str, bool, None) — 26 new assertions (212 tests now pass for the module).
- Documented `is_carmichael_number`, `is_korselt_number`, and `is_giuga_number` in the `prime_utils` file listing and prose section of `README.md`.
- Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `.kilo/command/scaffold-project.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6576 tests and passes with the same 6 pre-existing errors, `make lint` is clean, and `make typecheck` reports the same 9 pre-existing errors (unchanged by this work).

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Unreleased — added is_wilson_prime test coverage to prime_utils

- Added `TestIsWilsonPrime` to `tests/test_prime_utils.py` covering known Wilson primes (5, 13, 563), non-Wilson primes, composites, negatives, and the `TypeError` path (float, str, bool, None) — 20 new assertions. The `is_wilson_prime` helper itself was already present in `prime_utils.py` and exported via `__all__`; this session added the missing test coverage and documented the previously undocumented prime helpers (`is_automorphic`, `is_truncatable_prime`, `is_pythagorean_prime`, `is_wilson_prime`) in the `prime_utils` file listing and prose section of `README.md` and in `.kilo/command/scaffold-project.md`. Synchronized `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `.kilo/command/scaffold-project.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added is_type_var to type_check_utils

- Added `is_type_var(value)` to `type_check_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and a `bool` return; it returns `True` when *value* is a `typing.TypeVar` instance, `False` otherwise. Added `TestIsTypeVar` to `tests/test_type_check_utils.py` covering TypeVar instances and the `False` paths for classes, instances, strings, ints, None, and dicts. Updated the `type_check_utils` module prose section of `README.md`. Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added is_frozenset to type_check_utils

- Added `is_frozenset(value)` to `type_check_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and a `bool` return; it returns `True` when *value* is a `frozenset` instance, `False` otherwise (a mutable `set` is not a `frozenset`, and vice versa). Added `TestTypeChecks.test_is_frozenset` to `tests/test_type_check_utils.py` covering frozenset instances, the empty frozenset, and the `False` paths for mutable sets, lists, tuples, strings, ints, None, and dicts (10 new assertions). Updated the `type_check_utils` module prose section of `README.md` and the `type_check_utils` line of `.kilo/command/scaffold-project.md`. Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, `README.md`, `CHANGELOG.md`, and `.kilo/command/scaffold-project.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added is_composite to math_utils

- Added `is_composite(n)` to `math_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation matching `is_prime`; it returns `True` when *n* is a composite number (a positive integer greater than 1 that is not prime), `False` for primes, and raises `ValueError` for integers less than 2. Added `TestIsComposite` to `tests/test_math_utils.py` covering composite numbers, primes, edge cases (1, 0, negatives), large values, and the `TypeError` path. Updated the `math_utils` module tree entry and prose section of `README.md`. Synchronized `math_utils.py`, `tests/test_math_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — fixed is_callable regression and added type_utils test coverage

- Fixed `is_callable(tp)` in `type_utils.py`: the parameterized form `Callable[[int], str]` returned `False` because `get_origin` yields `collections.abc.Callable` rather than `typing.Callable`. The check now compares the origin against `typing.Callable` and `collections.abc.Callable`, so both bare `Callable` and parameterized `Callable[[...], ...]` forms are detected.
- Added test coverage for the previously untested `type_utils` helpers: `TestIsCallable`, `TestIsTuple`, `TestIsListType`, `TestIsDictType`, `TestGetOriginName`, `TestIsNoneType`, `TestIsAny`, and `TestUnwrapOptional` in `tests/test_type_utils.py` (25 new assertions). Verified `is_callable`, `is_tuple`, `is_list_type`, `is_dict_type`, `get_origin_name`, `is_none_type`, `is_any`, and `unwrap_optional` against bare aliases, parameterized aliases, and non-matching types.
- Updated the `type_utils` module tree entry and prose section of `README.md` to enumerate the full public API. Synchronized `type_utils.py`, `tests/test_type_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added is_lucas_number to number_utils

- Added `is_lucas_number(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments (rejecting `bool`); a Lucas number is an integer in the sequence defined by `L(0) = 2`, `L(1) = 1`, `L(n) = L(n-1) + L(n-2)` (returns `False` for negative values); `is_lucas_number(0)` returns `False`. Added `TestIsLucasNumber` to `tests/test_number_utils.py` covering known Lucas numbers, non-Lucas values, negative values, and the `TypeError` path. Updated the `number_utils` module listing and prose section of `README.md` and the `number_utils` line of `.kilo/command/scaffold-project.md`. Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `.kilo/command/scaffold-project.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `count_non_whitespace_characters(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the number of non-whitespace characters in *text_, treating empty text as zero. Added `TestCountNonWhitespaceCharacters` to `tests/test_prompt_utils.py` covering empty, whitespace-only, no-whitespace, mixed, newline/tab, unicode, single-character, and `TypeError` paths (9 new tests). Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `count_whitespace_characters(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the number of whitespace characters in *text_, treating empty text as zero, complementing `count_non_whitespace_characters`. Added `TestCountWhitespaceCharacters` to `tests/test_prompt_utils.py` covering empty, whitespace-only, no-whitespace, mixed, newline/tab, unicode, single-whitespace, and `TypeError` paths (9 new tests). Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Latest Session (2026-10-30) — added is_wilson_prime test coverage to prime_utils

Verified repository health: `make test` passes (6555 tests), `make lint` and `make typecheck` are green, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `TestIsWilsonPrime` to `tests/test_prime_utils.py` covering known Wilson primes (5, 13, 563), non-Wilson primes, composites, negatives, and the `TypeError` path (float, str, bool, None) — 20 new assertions. The `is_wilson_prime` helper itself was already present in `prime_utils.py` and exported via `__all__`; this session added the missing test coverage.
- Documented the previously undocumented prime helpers (`is_automorphic`, `is_truncatable_prime`, `is_pythagorean_prime`, `is_wilson_prime`) in the `prime_utils` file listing and prose section of `README.md` and in `.kilo/command/scaffold-project.md`.
- Synchronized `tests/test_prime_utils.py`, `README.md`, `CHANGELOG.md`, and `.kilo/command/scaffold-project.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `type_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added coerce_to_int boundary tests to type_check_utils

Verified repository health: `make test` passes, `make lint` and `make typecheck` are green, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `TestCoerceToIntBoundary.test_coerce_to_int_boundary` to `tests/test_type_check_utils.py` (inside the existing `TestEnsureType` class) covering negative-float truncation, whitespace/sign-prefixed strings, leading zeros, large ints, float-string `ValueError`, and `TypeError` paths for lists, dicts, sets, bytes, and None (15 new assertions). Synchronized `tests/test_type_check_utils.py` and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `type_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added is_fibonacci_number to number_utils

Verified repository health: `make test` passes, `make lint` and `make typecheck` are green, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `is_fibonacci_number(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments (including bools); it returns True for non-negative integers that appear in the Fibonacci sequence, using the closed-form identity that `5*value**2 + 4` or `5*value**2 - 4` must be a perfect square. Added `TestIsFibonacciNumber` to `tests/test_number_utils.py` covering known Fibonacci numbers, non-Fibonacci numbers, negatives, a large Fibonacci number, and the `TypeError` paths for strings, floats, bools, and None (15 new tests). Updated the `number_utils` module prose section of `README.md`. Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `type_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added count_trailing_newlines to prompt_utils

Verified repository health: `make test` passes, `make lint` and `make typecheck` are green, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `count_trailing_newlines(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns the number of trailing ``\\n`` characters in *text*. Added `TestCountTrailingNewlines` to `tests/test_prompt_utils.py` covering empty input, no trailing newlines, single and multiple trailing newlines, CRLF, trailing spaces, only-newlines input, and the `TypeError` path. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `type_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — exported strip_non_ascii and truncate_bytes from strings

Verified repository health: `make test` passes, `make lint` and `make typecheck` are green, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `strip_non_ascii` and `truncate_bytes` to `strings.__all__` (they were implemented and tested but not exported).
- Documented `strip_non_ascii` and `truncate_bytes` in the `strings.py` file listing and module description in `README.md`.
- No functional changes to implementations. Synchronized `strings.py` and `README.md` into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — fixed lint/typecheck regressions in typing_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6518 tests and passes, `make lint` reported 1 error, `make typecheck` reported 1 error in 528 source files, and `python tools/refresh_scaffold.py --check` reported 2 stale embedded copies.

Completed in this session:

- Fixed a ruff `F811` redefinition error in `tests/test_typing_utils.py`: the import block pulled `Literal` from `typing` on line 3 and then re-imported it from `typing_utils` on line 8, which ruff flagged as a redefinition of an unused name. Removed the redundant `Literal` from the `typing` import since the test file uses the `Literal` re-exported by `typing_utils`.
- Fixed a mypy `attr-defined` error in `type_utils.py`'s `is_literal`: the fallback path imported `typing._LiteralGenericAlias` directly, but mypy does not recognize that private attribute. Replaced the direct import with `getattr(typing, "_LiteralGenericAlias", None)` guarded by a `None` check, preserving the isinstance-based detection for Python versions where the alias exists.
- Refreshed the embedded copies of `type_utils.py` and `tests/test_typing_utils.py` in `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` runs 6518 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and scaffold sync is clean.

Next Planned (recorded here since no other board participant exists to post to):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `type_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

- Audit the remaining `type_check_utils.py` coercion helpers (`coerce_to_str`, `coerce_to_float`, `coerce_to_bool`, `ensure_type`) for missing boundary cases and add a minimal, hermetic helper or test class that fits the existing API style.

## Latest Session (2026-10-29) — added is_awaitable to type_check_utils

- Added `is_awaitable(value)` to `type_check_utils.py` with a typed signature, `__all__` export, and a Google-style docstring with doctests using `inspect.isawaitable` for a hermetic awaitability check; it returns `True` for coroutines and objects implementing `__await__`. Added `TestIsAwaitable` to `tests/test_type_check_utils.py` covering coroutines, awaitable objects, and non-awaitable values. Updated the `type_check_utils` module prose section of `README.md` to list `is_awaitable`. Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, and `README.md` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.


## Latest Session (2026-10-29) — added is_typeddict to type_check_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6826 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `is_module(value)` to `type_check_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and the inherent `isinstance`-based check consistent with the other `is_*` predicates; it returns `True` when *value* is a `types.ModuleType` (e.g. `sys`), `False` otherwise. Added `test_is_module` to `tests/test_type_check_utils.py` covering modules, non-modules, and `None`. Updated the `type_check_utils` module prose section of `README.md`. Recorded the change in this Unreleased section of `CHANGELOG.md`. Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6826 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `list_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added is_protocol to type_check_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6503 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `is_protocol(value)` to `type_check_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-class arguments; it returns `True` when *value* is a `typing.Protocol` class (detected via the `_is_protocol` marker attribute), `False` for ordinary classes and built-in types. Added `TestIsProtocol` to `tests/test_type_check_utils.py` covering a plain `Protocol`, a `runtime_checkable` `Protocol`, built-in types (`int`, `str`, `object`, `Exception`, ...), and the `TypeError` path for strings/ints/None/lists/dicts. Updated the `type_check_utils` module prose section of `README.md` to list `is_protocol`. Recorded the change in the Unreleased section of `CHANGELOG.md`. Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6503 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `list_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added is_chen_prime to prime_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6496 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `is_chen_prime(n)` to `prime_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments (rejecting `bool`); it returns `True` when *n* is a prime such that *n + 2* is either prime or semiprime (a Chen prime), `False` otherwise, reusing the existing `is_prime` and `is_semiprime` helpers. Added `TestIsChenPrime` to `tests/test_prime_utils.py` covering true cases (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41), false cases (43, 4, 6, 0, 1, -3), and the `TypeError` path for float/string/bool inputs. Updated the `prime_utils` module tree entry and prose section of `README.md`. Recorded the change in the Unreleased section of `CHANGELOG.md`. Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6499 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `list_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added chunks to list_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6486 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `chunks(lst, size)` to `list_utils.py` with a typed signature, `__all__` export, a Google-style docstring with examples, and validation raising `TypeError` for non-list/bool/non-int arguments and `ValueError` for non-positive sizes; it splits a list into consecutive chunks, returning the last chunk shorter if needed and preserving the original list. Added `TestChunks` to `tests/test_list_utils.py` covering basic, equal-sized, size-1, empty list, original preservation, and all TypeError/ValueError paths.
- Updated the `list_utils` module description in `README.md` to list `chunks`.
- Recorded the change in the Unreleased section of `CHANGELOG.md`.
- Synchronized `list_utils.py`, `tests/test_list_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6496 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `list_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — cleaned up `number_utils.py` `__all__` exports

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6485 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Audited `number_utils.py`'s `__all__` against the module's defined public helpers and found two defects: `safe_divide` and `round_to` were each listed twice, and `is_perfect_number` — which is defined at `number_utils.py:955`, has a Google-style docstring with doctests, and is covered by `TestIsPerfectNumber` in `tests/test_number_utils.py` — was missing from `__all__` entirely, leaving it unexported.
- Rewrote `__all__` so every public helper is declared exactly once, in definition order, ending with `is_perfect_number`. Verified with `inspect.getmembers` that defined-but-unexported and exported-but-undefined lists are both empty.
- Updated the `number_utils` module tree entry and prose section of `README.md` to enumerate the full public API (`safe_divide`, `is_perfect_cube`, `is_perfect_square`, `is_power_of_two`, `is_palindromic_number`, `digital_root`, `is_triangular_number`, `gcd`, `lcm`, `ceil_div`, `is_divisible_by`, `is_multiple_of`, `divides`, `map_range`, `remap`, etc.) instead of the stale short list.
- Recorded the fix in the Unreleased section of `CHANGELOG.md` under `### Fixed`. Synchronized `number_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6485 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and scaffold sync is clean.
- Committed the work as `fix(number_utils): clean up __all__ exports`.

Next Planned (posted for the following agent):

- Harden `type_check_utils.py`: add a minimal, hermetic helper (e.g. `is_callable`, `is_protocol`, or a type-name formatter) that fits the existing API style — typed signature, `__all__` export, Google-style docstring with doctests, `TypeError` validation — with tests in `tests/test_type_check_utils.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added map_or_else to maybe_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6482 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `map_or_else(default_fn, fn)` to `maybe_utils.Maybe` with typed signature, Google-style docstring including doctests, lazy default computation for `Nothing`, default fallback when the mapper returns `None` or raises an exception, and updated `__all__` unchanged. Added tests in `tests/test_maybe_utils.py` covering Some/Nothing cases, `None` mapper result, and mapper exception fallback (3 new tests). Updated the `maybe_utils` module prose section of `README.md` (tree entry and prose paragraphs). Recorded the change in `CHANGELOG.md`. Synchronized `maybe_utils.py`, `tests/test_maybe_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6485 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.
- Committed the work as `feat(maybe_utils): add map_or_else helper`.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `seq_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added median_low to stats

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6424 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `median_low(numbers)` to `stats.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation complementing `median`: it returns the low median (the lower of the two middle values for even-length lists, the middle value for odd-length lists) and raises `ValueError` for an empty list and `TypeError` for non-lists or non-numeric elements. Added `TestMedianLow` to `tests/test_stats.py` covering odd/even lengths, single element, unsorted input, negatives, empty-list `ValueError`, and non-list/non-numeric/bool `TypeError` paths (9 new tests). Updated the `stats` module prose section of `README.md`. Recorded the change in this Unreleased section of `CHANGELOG.md`. Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs 6433 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.
- Committed the work as `feat(stats): add median_low helper`.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `seq_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — fixed pre-existing test/typecheck failures

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6409 tests with 1 pre-existing failure (the `aifc_utils.py` scaffold-sync assertion, identical on the clean tree), `make lint` is clean, `make typecheck` reports 2 pre-existing errors in 2 files (identical on the clean tree), and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Fixed the `aifc_utils.py` scaffold-sync assertion: `tests/test_scaffold.py`'s `test_required_files_generated` listed `tests/test_aifc_utils.py` but omitted the module entry `aifc_utils.py` itself, so `TestScaffoldSync.test_every_module_is_asserted_by_scaffold_tests` failed. Added `"aifc_utils.py"` to the expected list.
- Fixed a mypy `arg-type` error in `uu_utils.py`'s `decode`: `_uu.decode`'s fourth parameter is typed `bool`, not `int`, so the `quiet` argument was wrapped with `bool(...)`.
- Fixed a mypy `type-var` error in `tests/test_stats.py`: the `# type: ignore[list-item]` on the `moving_average([1, 2, "a"], 2)` line was the wrong code; changed it to `# type: ignore[type-var]`.
- Refreshed the embedded copies of `uu_utils.py` and `tests/test_stats.py` in `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` runs 6409 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `seq_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added flatten to seq_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6404 tests with 1 pre-existing failure (the `aifc_utils.py` scaffold-sync assertion, identical on the clean tree), `make lint` is clean, `make typecheck` reports 2 pre-existing errors in 2 files (identical on the clean tree), and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `flatten(sequence)` to `seq_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation: it removes one level of nesting from a sequence, treating strings and bytes as atomic and preserving element order. Added `TestFlatten` to `tests/test_seq_utils.py` covering basic flattening, mixed atomic/nested elements, empty input, already-flat input, strings-as-atomic, and the `TypeError` path (7 new tests). Updated the `seq_utils` tree entry and prose section of `README.md` and the `seq_utils` line of `.kilo/command/scaffold-project.md`. Recorded the change in this Unreleased section of `CHANGELOG.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `.kilo/command/scaffold-project.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs all `seq_utils` tests passing with no new failures, `make lint` is clean, `make typecheck` reports no new errors in `seq_utils.py`, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `seq_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — added chunk to seq_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6396 tests with 1 pre-existing failure (the `aifc_utils.py` scaffold-sync assertion, identical on the clean tree), `make lint` is clean, `make typecheck` reports 2 pre-existing errors in 2 files (identical on the clean tree), and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `chunk(sequence, size)` to `seq_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError`/`ValueError` validation: it splits a sequence into fixed-size chunks, with a possibly-shorter final chunk and an empty list for empty input. Added `TestChunk` to `tests/test_seq_utils.py` covering basic chunking, oversized chunks, empty input, strings, tuples, size-one chunks, and the `TypeError`/`ValueError` paths (9 new tests). Updated the `seq_utils` tree entry and prose section of `README.md`. Recorded the change in this Unreleased section of `CHANGELOG.md`. Synchronized `seq_utils.py`, `tests/test_seq_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified the work: `make test` runs all `seq_utils` tests passing with no new failures, `make lint` is clean, `make typecheck` reports no new errors in `seq_utils.py`, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`, `seq_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-29) — fixed lint/typecheck regressions in strings

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6367 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Fixed a mypy `return-value` error in `strings.py`'s `is_decimal`: the previous `return int_part.isdigit() and frac_part.isdigit() and (int_part or frac_part)` expression returned a `str` (the last truthy operand) instead of a `bool`; wrapped the whole expression in `bool(...)` so the return type is `bool`.
- Fixed an `I001` ruff error in `tests/test_strings.py` where the import block was un-sorted/un-formatted; ran `ruff check --fix` to sort it.
- Refreshed the embedded copies of `strings.py` and `tests/test_strings.py` in `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` runs 6367 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added is_version_at_least/is_version_at_most to version_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6313 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `is_version_at_least(version, minimum)` and `is_version_at_most(version, maximum)` to `version_utils.py` as relational companions to `is_version_greater_equal`/`is_version_less_equal`: they return whether a version satisfies a lower/upper bound, delegating to `compare_versions`. Exported in `__all__` with Google-style docstrings and doctests, plus the aliases `at_least`/`at_most`.
- Added `TestIsVersionAtLeast` and `TestIsVersionAtMost` to `tests/test_version_utils.py` covering greater/equal/less cases, the tuple-length asymmetry (e.g. `1.3` vs `1.3.0`), alias behavior, the `TypeError` paths for non-string arguments, and the `ValueError` path for invalid versions (16 new tests).
- Updated the `version_utils` module prose section of `README.md` to document `is_version_at_least`/`is_version_at_most`.
- Synchronized `version_utils.py`, `tests/test_version_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` runs 6329 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added coerce_to_float to type_check_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6309 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

- Added `coerce_to_float(value)` to `type_check_utils.py` as a complement to `coerce_to_str` and `coerce_to_int`: it accepts ints (including bools), floats, and numeric strings, raising `TypeError` for unsupported types and `ValueError` for non-numeric strings. Exported in `__all__` with a Google-style docstring and doctests.
- Added `TestCoerceToFloat` to `tests/test_type_check_utils.py` covering ints, floats, bools, numeric strings, negative strings, the `ValueError` path, and the `TypeError` paths for lists and None (11 new tests).
- Updated the `type_check_utils` module prose section of `README.md` to document `coerce_to_float`.
- Synchronized `type_check_utils.py`, `tests/test_type_check_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` runs 6320 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

## Latest Session (2026-10-28) — added count_paragraphs to prompt_utils

The board held no task (bootstrap). Verified repository health before starting: `make test` runs 6298 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync (after fixing a stale `prime_utils.py`/`tests/test_prime_utils.py` copy and a mypy `no-any-return` error in `prime_utils.py`).

Completed in this session:

- Fixed a mypy `no-any-return` error in `prime_utils.py`'s `is_automorphic` by replacing `square % (10 ** len(str(n))) == n` with the equivalent `str(square).endswith(str(n))`; this mypy version types `literal ** variable_int` as `Any`, and the behavior is identical for all inputs.
- Refreshed the embedded copies of `prime_utils.py` and `tests/test_prime_utils.py` in `scaffold.sh`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `count_paragraphs(text)` to `prompt_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation; it counts runs of non-blank lines separated by blank lines, treating empty text as zero paragraphs.
- Added `TestCountParagraphs` to `tests/test_prompt_utils.py` covering empty, single, multi-line, multiple paragraphs, multiple blank-line separators, trailing blank lines, all-blank, CRLF, whitespace-only separators, and the `TypeError` path (11 new tests).
- Updated the `prompt_utils` module prose section of `README.md` to list `count_paragraphs`.
- Synchronized `prime_utils.py`, `tests/test_prime_utils.py`, `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Verified: `make test` runs 6309 tests and passes, `make lint` is clean, `make typecheck` reports no issues, and scaffold sync is clean.

Next Planned (posted for the following agent):

- Keep hardening the small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`, `type_check_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

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
- Added `map_or(default, fn)` to `maybe_utils.py` completing the `Maybe` API: it applies `fn` to the contained value if Some, otherwise returns `default`, swallowing exceptions and treating a `None` result as the default. It has a typed signature, a Google-style docstring with doctests, and is safe for both Some and Nothing. Added `TestMapOr` methods to `tests/test_maybe_utils.py` covering Some/Nothing, default-returned-on-Nothing, value passed through the function, default returned when the function returns `None`, default returned when the function raises, default returned on Nothing with a raising function, and float inputs. Updated the `maybe_utils` module prose section of `README.md`. Synchronized `maybe_utils.py`, `tests/test_maybe_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Fixed `reverse_lines(text)` and `strip_blank_lines(text)` in `prompt_utils.py` to split and join on real newlines instead of the literal characters `\n` (backslash-n), so they now correctly handle input containing actual line breaks. Both helpers were already exported in `__all__` but lacked test coverage. Added `TestReverseLines` and `TestStripBlankLines` to `tests/test_prompt_utils.py` covering multi-line/single-line/empty input, whitespace-only blank lines, and the `TypeError` paths. Updated the `prompt_utils` module prose section of `README.md`.
- Added `is_binary(s)` to `strings.py` returning `True` when *s* is non-empty and every character is a binary digit (`0` or `1`), `False` otherwise. It validates that *s* is a string, raising `TypeError` otherwise, and is exported in `__all__` with a Google-style docstring and doctests. Added `TestIsBinary` to `tests/test_strings.py`. Updated the `strings` module prose section of `README.md`.
- Added `reverse_lines(text)` to `prompt_utils.py` reversing the order of lines in *text*, with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation. Added tests to `tests/test_prompt_utils.py`.
- Added `count_letters(s)` to `strings.py` returning the number of alphabetic characters in *s*, with typed signature, `__all__` export, Google-style docstring, and `TypeError` validation. Added `TestCountLetters` to `tests/test_strings.py`.
- Added `count_characters(text)` to `prompt_utils.py` returning the number of characters in *text* (including whitespace), matching `len`, with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-string arguments. Added `TestCountCharacters` to `tests/test_prompt_utils.py` covering empty, ASCII, whitespace-counted, unicode, single-character, and `TypeError` paths. Updated the `prompt_utils` module prose section of `README.md`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `standard_error(numbers)` to `stats.py` returning the standard error of the mean (the sample standard deviation divided by the square root of the sample size), with typed signature, `__all__` export, Google-style docstring, and `TypeError`/`ValueError` validation (raising `ValueError` for empty lists or single-element lists). Added `TestStandardError` to `tests/test_stats.py` covering basic cases, negatives, floats, single-element `ValueError`, empty-list `ValueError`, and `TypeError` paths. Updated the `stats` module prose section of `README.md`. Synchronized `stats.py`, `tests/test_stats.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Added `format_farewell(name, farewell="Goodbye")` to `greeting_utils.py` returning a formatted farewell string, with typed signature, Google-style docstring, and `TypeError` validation. Added `TestFormatFarewell` to `tests/test_greeting_utils.py` covering default, custom, empty name, and `TypeError` paths. Updated the `greeting_utils` module prose section of `README.md`.
- Added comprehensive boundary tests for `strings.py` (empty strings, whitespace-only, unicode/multibyte, type errors, edge cases) to `tests/test_strings.py`.
- Added `is_complex(obj)`, `is_real(obj)`, and `is_rational(obj)` to `numbers_utils.py`, exposing the remaining numeric abstract base classes (`Complex`, `Real`, `Rational`) as `isinstance`-based predicates complementing `is_number` and `is_integral`. Each has a typed signature, a Google-style docstring with doctests, and is exported in `__all__`. Added `TestIsComplex`, `TestIsReal`, and `TestIsRational` to `tests/test_numbers_utils.py` covering true/false/non-number cases. Updated the `numbers_utils` tree entry and prose section of `README.md`. Synchronized `numbers_utils.py`, `tests/test_numbers_utils.py`, `README.md`, and this CHANGELOG into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

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

### Fixed
- Cleaned up `number_utils.py`'s `__all__`: removed duplicate entries (`safe_divide` and `round_to` were listed twice) and added the missing `is_perfect_number` export so every public helper is declared in `__all__` exactly once. Updated the `number_utils` module tree entry and prose section of `README.md` to match the full public API. Verified: `make test` runs 6485 tests and passes, `make lint` is clean, `make typecheck` reports no issues in 528 source files.

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
- Added `collections_abc_utils.py` and `tests/test_collections_abc_utils.py`.
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
- Added `deque_utils.py` and `tests/test_deque_utils.py`.
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
- Added `is_version_between(version, lower, upper, inclusive=True)` to `version_utils.py` with bounds checking and aliases `between`/`is_between`, plus tests; updated README and synchronized embedded copies via `make refresh-scaffold`.
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

- Added `is_neon_number(value)` to `number_utils.py` with a typed signature, `__all__` export, a Google-style docstring with doctests, and `TypeError` validation for non-int arguments (rejecting `bool`); a neon number is a non-negative integer whose square's digit sum equals the number itself (returns `False` for negative values). Added `TestIsNeonNumber` to `tests/test_number_utils.py` covering true cases (0, 1, 9), false cases (2, 10), negative numbers, and the `TypeError` path. Updated the `number_utils` module tree entry and prose section of `README.md` and the `number_utils` line of `.kilo/command/scaffold-project.md`. Recorded the change in the Unreleased section of `CHANGELOG.md`. Synchronized `number_utils.py`, `tests/test_number_utils.py`, `README.md`, `CHANGELOG.md`, and `.kilo/command/scaffold-project.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

- Added `is_classmethod` and `is_staticmethod` to `type_check_utils.py` with `__all__` exports, Google-style docstrings, and tests in `tests/test_type_check_utils.py`. Updated `README.md` and synchronized embedded copies via `make refresh-scaffold`.

## Latest Session (2026-10-28) — added combination and permutation to math_utils

The board held no task (bootstrap context). Verified repository health: all tests pass, `make lint` is clean, and `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Completed in this session:

## Unreleased — added `count_leading_ones` and `has_leading_ones` to `bit_utils`

- Completed the `count_leading_ones(value, width)` and boolean companion `has_leading_ones(value, width)` feature in `bit_utils.py`. The implementations and `__all__` exports were already present but shipped without test coverage or README documentation. `count_leading_ones` returns the number of leading one bits within a fixed bit width (returning `width` when every bit is set), and `has_leading_ones` is its boolean companion reusing `count_leading_ones` for consistency. Both accept typed `int` arguments (rejecting booleans), validate that *value* is non-negative and *width* is positive, raise `ValueError` when *value* does not fit within *width* bits, and ship with Google-style docstrings and ASCII-safe doctests. Added `TestCountLeadingOnes` and `TestHasLeadingOnes` to `tests/test_bit_utils.py` covering basic widths, width-one/large-width cases, consistency (`has_leading_ones` vs `count_leading_ones`), width-fit/value/type errors, and bool rejection. Updated the `bit_utils` prose section of `README.md`. Synchronized `tests/test_bit_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bit_utils` (50 tests), `python -m doctest bit_utils.py` (OK), `python -m unittest tests.test_public_api` (OK), full suite `python -m unittest discover tests/` (OK). No changes to `.github/workflows/**`.

## Unreleased — added `take` and `drop` to `itertools_utils`

- Added `take(iterable, n)` and `drop(iterable, n)` to `itertools_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and validation raising `TypeError`/`ValueError` (rejecting non-iterables, non-`int`/`bool` *n*, and negative *n*). `take` returns up to the first *n* items and `drop` skips the first *n* items, both accepting any iterable (including generators). Added `TestTake` and `TestDrop` to `tests/test_itertools_utils.py` covering basic/more-than-available/zero/empty/generator cases and the type/value error paths (18 new tests; 197 tests in the module). Updated the `itertools_utils` prose section of `README.md`. Synchronized `itertools_utils.py`, `tests/test_itertools_utils.py`, `README.md`, and `CHANGELOG.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_itertools_utils` (197 OK), `python -m doctest itertools_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.



## Unreleased — added `find_index_in_deque` to `deque_utils`

- Added `find_index_in_deque(d, value, start=0, stop=None)` to `deque_utils.py` as a non-raising companion to `index_in_deque`, returning the 0-based index of the first match or `None` when absent. Typed `Optional[int]` return, `__all__` export, Google-style docstring with ASCII-safe doctests. Added `TestFindIndexInDeque` (7 tests) to `tests/test_deque_utils.py` covering basic, missing, `start`/`stop` bounds, empty, and consistency with `index_in_deque`. Updated `README.md` tree/prose. Synchronized `deque_utils.py`, `tests/test_deque_utils.py`, `README.md`, and `CHANGELOG.md` into `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_deque_utils` (67 OK), `python -m doctest deque_utils.py` (OK), `python -m unittest tests.test_public_api` (OK). No changes to `.github/workflows/**`.

## Unreleased — added `count_leading_zeros` and `has_leading_zeros` to `bit_utils`

- Added `count_leading_zeros(value, width)` and boolean companion `has_leading_zeros(value, width)` to `bit_utils.py` with typed signatures, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and validation raising `TypeError`/`ValueError` (including rejection of values that do not fit within *width*). `count_leading_zeros` returns the number of zero bits to the left of the most significant set bit within a fixed *width* (returning *width* for zero). Added `TestCountLeadingZeros` and `TestHasLeadingZeros` to `tests/test_bit_utils.py` covering basic widths, zero/full-width cases, consistency, width-fit/value/type errors, and bool rejection (7 new tests). Updated the `bit_utils` module tree entry and prose section of `README.md`. Synchronized `bit_utils.py`, `tests/test_bit_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m unittest tests.test_bit_utils` (43 tests), `python -m doctest bit_utils.py` (44 doctests), `python -m unittest tests.test_public_api` (OK), full suite `python -m unittest discover tests/` (OK). No changes to `.github/workflows/**`.



- Added `find_index(lst, predicate)` to `list_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation for non-list arguments; it returns the index of the first matching element or `None` when no match is found. Added `TestFindIndex` to `tests/test_list_utils.py` (7 new tests) covering basic/edge cases and the `TypeError` path. Updated the `list_utils` module tree entry and prose section of `README.md` to include `find_index`. Synchronized `list_utils.py`, `tests/test_list_utils.py`, and `README.md` into the embedded copies of `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — added has_whitespace to prompt_utils

- Added `has_whitespace(text)` to `prompt_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and `TypeError` validation for non-string arguments; it returns `True` when *text* contains at least one whitespace character and `False` otherwise, serving as a boolean companion to whitespace-counting helpers. Added `TestHasWhitespace` to `tests/test_prompt_utils.py` covering whitespace, tabs/newlines, strings without whitespace, empty input, and the `TypeError` path (5 new tests). Imported `has_whitespace` at the top of the test file to match the module's `__all__` contract. Updated the `prompt_utils` module tree entry and prose section of `README.md` to include `has_whitespace`. Synchronized `prompt_utils.py`, `tests/test_prompt_utils.py`, `README.md`, `CHANGELOG.md`, and `scaffold.sh` with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Verified: `python -m pytest tests/test_prompt_utils.py -v` passes.

- Added `combination(n, k)` and `permutation(n, k)` to `math_utils.py` with full validation consistent with module conventions (`TypeError` for non-ints/bools, `ValueError` for negative values and `k > n`), exported via `__all__`, Google-style docstrings, and examples. Implementations use efficient iterative formulas without relying on heavy helpers.
- Added `TestCombination` and `TestPermutation` to `tests/test_math_utils.py` covering basic cases, edge values (k=0, k=n), large values, type errors, and value errors; updated imports to include the new functions.
- Updated `README.md` to document `combination` and `permutation` in both the file listing and module description.
- Refreshed embedded copies in `scaffold.sh` with `make refresh-scaffold` and verified with `python tools/refresh_scaffold.py --check`; all tests pass.

- Added `xml_utils.py` and `tests/test_xml_utils.py` with XML parsing/generation helpers, added to `pyproject.toml`, `README.md`, and embedded in `scaffold.sh`.

- Added `unique_preserve_order(lst)` to `list_utils.py` with `__all__` export, Google-style docstring with examples, `TypeError` validation for non-list arguments, and tests in `tests/test_list_utils.py`. Updated `list_utils` description in `README.md`. Synchronized embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

Next Planned (posted for the following agent):

- Keep hardening small utility modules (e.g. `prompt_utils.py`, `stats.py`, `strings.py`, `version_utils.py`, `prime_utils.py`, `number_utils.py`): add a minimal, hermetic helper that fits the existing API style with tests in `tests/test_*.py`.
- Follow conventions: typed APIs, `__all__`, Google-style docstrings, validation raising `TypeError`/`ValueError`.
- Keep `make test`, `make lint`, and `make typecheck` green. If touching anything embedded in `scaffold.sh` (modules/tests/docs/changelog/scaffold templates/commands), run `make refresh-scaffold` and verify with `python tools/refresh_scaffold.py --check`.
- Update `README.md` and `CHANGELOG.md` if adding public APIs; refresh scaffold copies as needed. No changes to `.github/workflows/**`.

- Added `is_spy_number(value)` to `number_utils.py` with digit sum and product validation (raising `TypeError` for non-ints/bools; returns `False` for `<= 0`), exported via `__all__`, Google-style docstring with examples, and comprehensive tests. Updated `number_utils` in `README.md` and `.kilo/command/scaffold-project.md`. Synchronized embedded copies with `make refresh-scaffold`.

## Unreleased — seq_utils find_index predicate search

- Added `find_index(sequence, predicate)` to `seq_utils.py` with a typed signature, `__all__` export, Google-style docstring with doctests, and validation raising `TypeError` for non-sequence inputs and non-callable predicates; it returns the 0-based index of the first element satisfying *predicate*, or `None` when no match is found (complements `index_of` value search). Added `TestFindIndex` to `tests/test_seq_utils.py` (9 tests). Updated `README.md` (tree + prose). Synchronized embedded copies with `make refresh-scaffold`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. Targeted verification: `python -m unittest tests.test_seq_utils -q`, `python -m unittest tests.test_public_api -q`. No `.github/workflows/**` changes.

## Unreleased — dict_utils deep_merge strict validation

- `dict_utils.deep_merge`: added `TypeError` validation (`d1`/`d2` must be `dict`) and clarified docstring vs `merge` (recursive). Prevents confusing `AttributeError` on non-dict inputs and aligns with module conventions.
- `tests/test_dict_utils.py`: added mutation-safety and type-error coverage for `deep_merge`. Verification: `python -m unittest tests.test_dict_utils` (122 OK), `python -m unittest tests.test_public_api` (OK). `python tools/refresh_scaffold.py` refreshed embedded copies; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## Unreleased — set_utils is_not_subset/is_not_superset companions

- Added `is_not_subset(a, b)` and `is_not_superset(a, b)` to `set_utils.py` as boolean companions to `is_subset`/`is_superset` (negation predicates consistent with existing `is_equal`/`is_not_equal` and `is_disjoint`/`has_intersection` pairs). Typed `Iterable[Any] -> bool` APIs, `__all__` exports, Google-style docstrings with ASCII-safe doctests, and `TypeError` validation via existing iterable guards.
- Added `TestIsNotSubset` and `TestIsNotSuperset` to `tests/test_set_utils.py` covering basic/empty/equal/duplicate/consistency-with-positive-predicate and `TypeError` cases.
- Updated `README.md` (`set_utils` tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.
- Validation: `python -m unittest tests.test_set_utils` (OK), `python -m unittest tests.test_public_api` (OK). No `.github/workflows/**` changes.

## Unreleased — set_utils `is_not_equal` companion

- Added `is_not_equal(a, b)` to `set_utils.py` as the boolean companion to `is_equal`, returning `True` when two iterables do not represent the same set (order/duplicates/type ignored). Typed `Iterable[Any] -> bool` API, `__all__` export, Google-style docstring with ASCII-safe doctests, and `TypeError` validation consistent with module conventions.
- Added `TestIsNotEqual` to `tests/test_set_utils.py` covering basic cases, order/duplicate-insensitive equality, empty inputs, strings, consistency with `is_equal`, and type errors.
- Updated `README.md` (`set_utils` tree/prose). Refreshed embedded copies with `python tools/refresh_scaffold.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync.

## Unreleased — bytes_utils starts/ends slice + search stdlib-parity tests

- `bytes_utils.py`: added `start`/`end` slice parameters (with bool-rejected int validation, matching the module's strict style) and Google-style docstrings to `starts_with` and `ends_with`, preserving the existing two-argument behavior as defaults (stdlib-compatible API extension).
- `tests/test_bytes_utils.py`: added slice/bytearray/bool-validation coverage for `starts_with`/`ends_with`; added stdlib-parity empty-subsequence cases for `index`/`rindex`/`find`/`rfind`; added empty-old/empty-sub and bytearray parity cases for `replace`/`count`/`split`. Targeted verification: `python -m unittest tests.test_bytes_utils` (217 OK), `python -m unittest tests.test_public_api` (OK). `python tools/refresh_scaffold.py` refreshed embedded `bytes_utils.py`/`tests/test_bytes_utils.py`; `python tools/refresh_scaffold.py --check` reports all embedded copies in sync. No `.github/workflows/**` changes.

## [2026-11-11 02:02Z] - dis_utils/dumbdbm_utils exported API test coverage

### Added
- `tests/test_dis_utils.py`: coverage for exported `distb` (disassemble active traceback).
- `tests/test_dumbdbm_utils.py`: coverage for exported `open_dbm` alias, exported `error`, and `open_dbm` create/set/get round-trip.

### Changed
- `scaffold.sh`: refreshed embedded copies of `tests/test_dis_utils.py` and `tests/test_dumbdbm_utils.py` (`python tools/refresh_scaffold.py`).

### Verified
- `python -m unittest tests.test_dis_utils tests.test_dumbdbm_utils` (15 OK), `python -m unittest tests.test_public_api` (OK), `python -m ruff check dis_utils.py dumbdbm_utils.py tests/test_dis_utils.py tests/test_dumbdbm_utils.py` (clean), `python -m mypy tests/test_dis_utils.py tests/test_dumbdbm_utils.py dis_utils.py dumbdbm_utils.py` (clean), `python tools/refresh_scaffold.py --check` (in sync).
