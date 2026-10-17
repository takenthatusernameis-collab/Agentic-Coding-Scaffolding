# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]

- Added `enum_utils.py` — enum utilities for working with Python `enum.Enum` classes (`enum_to_dict`, `get_enum_member`, `is_enum_member`, `list_enum_members`, `enum_value_from_name`, `enum_name_from_value`) with input validation.
- `tests/test_enum_utils.py` — unit tests for `enum_utils.py`
- Added `enum_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions.

- Added `inspect_utils.py` — callable and object introspection utilities (`get_callable_name`, `is_callable`, `is_async_callable`, `get_signature`, `get_parameter_names`, `get_parameter_kinds`, `count_parameters`, `has_parameter`, `bind_arguments`, `is_builtin`, `get_source_file`, `get_source_lines`) using the standard library `inspect` module with input validation.
- `tests/test_inspect_utils.py` — unit tests for `inspect_utils.py`

- Added `id_utils.py` — identifier generation and validation utilities (`generate_id`, `new_id`, `is_valid_id`) for short URL-safe random identifiers with input validation.
- `tests/test_id_utils.py` — unit tests for `id_utils.py`

- Added `interval_utils.py` — interval utilities (`normalize_interval`, `is_valid_interval`, `interval_contains`, `interval_overlaps`, `interval_intersection`, `interval_union`, `merge_intervals`, `interval_length`) for closed numeric intervals with input validation.
- `tests/test_interval_utils.py` — unit tests for `interval_utils.py`
- Added `interval_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and test tree, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- Synchronized the `scaffold.sh` README tree with the repository `README.md` project structure tree: the scaffold template was missing 23 modules (`template_utils.py`, `uuid_utils.py`, `prompt_utils.py`, `itertools_utils.py`, `color_utils.py`, `number_utils.py`, `os_utils.py`, `sort_utils.py`, `prime_utils.py`, `decimal_utils.py`, `fractions_utils.py`, `heapq_utils.py`, `markdown_utils.py`, `bytes_utils.py`, `functools_utils.py`, `operator_utils.py`, `exceptions_utils.py`, `io_utils.py`, `ini_utils.py`, `weakref_utils.py`, `compression_utils.py`, `ip_utils.py`, `regex_utils.py`, `subprocess_utils.py`) and 26 test files (`test_async_utils.py`, `test_base64_utils.py`, `test_bytes_utils.py`, `test_calendar_utils.py`, `test_cli_utils.py`, `test_context_utils.py`, `test_decimal_utils.py`, `test_duration_utils.py`, `test_fractions_utils.py`, `test_hash_utils.py`, `test_html_utils.py`, `test_ini_utils.py`, `test_itertools_utils.py`, `test_networking_utils.py`, `test_number_utils.py`, `test_operator_utils.py`, `test_os_utils.py`, `test_prompt_utils.py`, `test_seq_utils.py`, `test_sort_utils.py`, `test_subprocess_utils.py`, `test_sys_utils.py`, `test_temp_utils.py`, `test_template_utils.py`, `test_terminal_utils.py`, `test_uuid_utils.py`, `test_weakref_utils.py`, `test_xml_utils.py`) from the repo tree, and had a stray `tests/test_calendar_utils.py` entry outside the `tests/` sub-section. Replaced both the module and tests sections of the scaffold template tree with the canonical alphabetized repo tree so scaffolded projects inherit a complete, consistent structure.

- Registered `locale_utils` across the full scaffold pipeline: the module existed as a source file with passing tests and was listed in `pyproject.toml` `py_modules`, but was missing from `scaffold.sh` (header comment, `py_modules` list, README tree, module/test sections, and CHANGELOG entries), `README.md` (tree, test tree, module description section), `.kilo/command/scaffold-project.md` (modules and tests lists), and `tests/test_scaffold.py` (required files, module lists, and functional smoke test). Added the `locale_utils.py` and `tests/test_locale_utils.py` heredoc blocks to `scaffold.sh`, the `test_locale_utils_functions_work` smoke test, and synchronized all documentation so scaffolded projects now include the locale utilities module.

- Added the missing `tests/test_compression_utils.py` and `tests/test_ip_utils.py` heredoc blocks to `scaffold.sh`: both modules existed as source files with passing tests and were registered in `pyproject.toml` `py_modules`, but the test heredocs were absent, so `--no-test` scaffolded projects were missing them. Verified the scaffold smoke test now generates both test files.

- Rebuilt the `scaffold.sh` header comment from the canonical README tree: removed 23 duplicate module/test entries and added the 6 missing modules (`itertools_utils`, `compression_utils`, `ip_utils`, `prompt_utils`, `uuid_utils`, `template_utils`) plus their test entries so the header lists every module exactly once in tree order.

- Removed a corrupted artifact left by a previous session: a phantom directory named `<` containing a bogus `</rfl:parameter>home/.../tests/test_copy_utils.py` file (a tool-call path leaked into file content). The `copy_utils.py` module does not exist in this repository; the artifact was untracked and is now deleted. Cleared the stale `.ruff_cache` so `make lint` reports against the real tree.

- Fixed a leaked line-number token (`113:`) in the `README.md` project structure tree that appeared as a prefix on the `compression_utils.py` entry.

- Added the missing `tests/test_subprocess_utils.py`, `tests/test_hash_utils.py`, `tests/test_weakref_utils.py`, `tests/test_fractions_utils.py`, and `tests/test_stats.py` entries to the Unreleased CHANGELOG section so the generated changelog lists every test file (the modules themselves were already documented, but their test entries were absent).

- Fixed `scaffold.sh` so it actually generates `functools_utils.py`, `itertools_utils.py`, and `regex_utils.py` (and their tests) in scaffolded projects: the modules were registered in `pyproject.toml` `py_modules` and listed in the scaffold header comment but had no heredoc blocks, so scaffolded projects were missing them. Added the 6 missing heredoc blocks and verified the scaffold smoke test generates all modules with passing tests, ruff, and mypy.

- Registered `template_utils` in `pyproject.toml` `py_modules`, where it was missing and causing an inconsistency with `scaffold.sh`, the README tree, and the CHANGELOG.

- `template_utils.py` — string template rendering utilities (`render_template`, `substitute`, `safe_substitute`, `render_from_dict`, `has_placeholders`, `extract_placeholders`) supporting `str.format()` and `string.Template` styles with placeholder extraction
- `tests/test_template_utils.py` — unit tests for `template_utils.py`

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `time_utils.py` — time utility functions for working with timestamps and durations (`now_epoch`, `now_iso`, `epoch_to_iso`, `iso_to_epoch`)
- `tests/test_time_utils.py` — unit tests for `time_utils.py`
- Added `time_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `decimal_utils.py` — decimal arithmetic utilities (`to_decimal`, `add`, `subtract`, `multiply`, `divide`, `power`, `quantize`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, `is_zero`) using the standard library `decimal` module with input validation
- `tests/test_decimal_utils.py` — unit tests for `decimal_utils.py`
- Added `decimal_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `heapq_utils.py` — heap queue utilities wrapping the standard library `heapq` module (`heapify`, `heappush`, `heappop`, `heapreplace`, `heappushpop`, `merge`, `nlargest`, `nsmallest`) with input validation
- `tests/test_heapq_utils.py` — unit tests for `heapq_utils.py`
- Added `heapq_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `calendar_utils.py` — calendar utilities (`is_leap_year`, `days_in_month`, `first_day_of_month`, `month_name`, `day_name`, `month_calendar`, `weekdays_in_month`, `weekend_days_in_month`, `is_weekend`, `add_months`) for date and month calculations using stdlib `calendar` with input validation
- `tests/test_calendar_utils.py` — unit tests for `calendar_utils.py`
- Synchronized `calendar_utils.py` across `scaffold.sh`, `pyproject.toml` `py_modules`, README tree and module section, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions

- `prime_utils.py` — prime number utilities (`prime_factors`, `nth_prime`, `primes_up_to`, `next_prime`, `previous_prime`) building on `math_utils.is_prime` with input validation
- `tests/test_prime_utils.py` — unit tests for `prime_utils.py`
- Added `prime_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `operator_utils.py` — operator utilities (`identity`, `negate`, `add`, `subtract`, `multiply`, `divide`, `power`, `modulo`, `clamp`, `between`) for common functional operations

- `sys_utils.py` — Python runtime and system information utilities (`get_python_version`, `get_python_version_string`, `get_executable`, `get_argv`, `get_platform`, `get_path`, `get_recursion_limit`, `set_recursion_limit`, `get_stdout_encoding`, `get_stderr_encoding`, `get_stdin_encoding`, `is_interactive`, `get_frame_info`, `get_refcount`) wrapping the standard library `sys` module with input validation
- `tests/test_sys_utils.py` — unit tests for `sys_utils.py`
- Added `sys_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions
- `semver_utils.py` — Semantic versioning utilities (`parse_semver`, `compare_semver`, `bump_major`, `bump_minor`, `bump_patch`, `is_valid_semver`, `SemanticVersion`) following Semantic Versioning 2.0.0
- `tests/test_semver_utils.py` — unit tests for `semver_utils.py`
- Added `semver_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- Added `semver_utils.py` with Semantic Versioning utilities and corresponding tests. Synchronized scaffold and docs.
- Bootstrap verification: all 1500 tests, ruff checks, and mypy checks pass on 2026-10-16

- `networking_utils.py` — networking utilities for TCP port and host operations (`is_valid_port`, `is_port_open`, `find_free_port`, `resolve_hostname`, `get_local_ip`, `tcp_ping`) wrapping the standard library `socket` module with input validation
- `tests/test_networking_utils.py` — unit tests for `networking_utils.py`
- Added `networking_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `itertools_utils.py` — iteration helpers (`chain_iterables`, `flatten_once`, `take_while_pred`, `chunk_iterable`, `product_of`, `combinations_of`, and more) wrapping the standard library `itertools` module with input validation
- `tests/test_itertools_utils.py` — unit tests for `itertools_utils.py`
- Added `itertools_utils.py` to README tree and module section, CHANGELOG Unreleased entry, and scaffold.sh module list

- `context_utils.py` — context manager utilities (`chdir`, `temp_environ`, `redirect_stdout`, `redirect_stderr`, `suppress`) for temporarily altering the runtime environment (working directory, environment variables, standard streams) and restoring it on exit using the standard library with input validation
- `tests/test_context_utils.py` — unit tests for `context_utils.py`
- Added `context_utils.py` to `pyproject.toml` `py_modules`, README tree and module section, `scaffold.sh` header comment and heredocs, `.kilo/command/scaffold-project.md`, and `tests/test_scaffold.py` assertions, plus this CHANGELOG Unreleased entry

- `textwrap_utils.py` — text wrapping utilities (`wrap_text`, `shorten_text`, `dedent_text`, `indent_text`, `fill_text`) using the standard library `textwrap` module with input validation
- `tests/test_textwrap_utils.py` — unit tests for `textwrap_utils.py`
- Added `textwrap_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `sys_utils.py` — Python runtime and system information utilities (`get_python_version`, `get_python_version_string`, `get_executable`, `get_argv`, `get_platform`, `get_path`, `get_recursion_limit`, `set_recursion_limit`, `get_stdout_encoding`, `get_stderr_encoding`, `get_stdin_encoding`, `is_interactive`, `get_frame_info`, `get_refcount`) for inspecting the interpreter and runtime environment using the standard library `sys` module with input validation
- `tests/test_sys_utils.py` — unit tests for `sys_utils.py`
- Added `sys_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `graphlib_utils.py` — graph and dependency resolution utilities (`topological_sort`, `has_cycle`, `dependency_order`, `is_valid_ordering`) for topological sorting and cycle detection of directed graphs using the standard library `graphlib` module with input validation
- `tests/test_graphlib_utils.py` — unit tests for `graphlib_utils.py`
- Added `graphlib_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `queue_utils.py` — FIFO queue utilities (`Queue` class backed by `collections.deque` with `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `clear`, `to_list`, `from_list`, plus module-level `create`, `enqueue`, `dequeue`, `peek`, `is_empty`, `size` helpers) with input validation
- `tests/test_queue_utils.py` — unit tests for `queue_utils.py`
- Added `queue_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `version_utils.py` — version parsing, comparison, and normalization utilities (`parse_version`, `compare_versions`, `is_greater`, `normalize_version`) for dotted version strings with input validation
- `tests/test_version_utils.py` — unit tests for `version_utils.py`
- Added `version_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `seq_utils.py` — sequence utilities (`first`, `last`, `nth`, `head`, `tail`, `split_at`, `take_while`, `drop_while`, `interleave`, `adjacent_pairs`, `is_sorted`) for common sequence operations with input validation
- `tests/test_seq_utils.py` — unit tests for `seq_utils.py`
- Added `seq_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `number_utils.py` — number utility functions (`clamp`, `round_to`, `is_integer`, `format_number`, `percentage`) for common numeric operations with input validation
- `tests/test_number_utils.py` — unit tests for `number_utils.py`
- Added `number_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions

- `sort_utils.py` — sorting utility functions (`is_sorted`, `bubble_sort`, `merge_sort`, `nth_largest`, `top_n`) for sorting and ordering operations
- `tests/test_sort_utils.py` — unit tests for `sort_utils.py`
- Added `sort_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions

- `temp_utils.py` — temporary file and directory management utilities (`create_temp_file`, `create_temp_dir`, `temp_file`, `temp_dir`, `write_temp_file`, `read_temp_file`, `cleanup_temp_path`, `is_temp_path`, `temp_path_exists`) wrapping the standard library `tempfile` module with input validation
- `tests/test_temp_utils.py` — unit tests for `temp_utils.py`
- Added `temp_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `xml_utils.py` — XML parsing and generation utilities (`parse_xml`, `parse_xml_string`, `build_xml`, `add_child`, `set_attribute`, `get_attribute`, `element_to_dict`, `dict_to_element`, `find_elements`, `find_element`, `get_element_text`, `set_element_text`, `xml_to_string`, `validate_well_formed`) wrapping the standard library `xml.etree.ElementTree` module with input validation
- `tests/test_xml_utils.py` — unit tests for `xml_utils.py`
- Added `xml_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `duration_utils.py` — time duration utilities (`parse_duration`, `format_duration`, `seconds_to_hms`, `hms_to_seconds`, `to_seconds`, `duration_between`, `add_duration`, `is_valid_duration`) for parsing, formatting, and converting time durations with input validation
- `tests/test_duration_utils.py` — unit tests for `duration_utils.py`
- Added `duration_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `http_utils.py` — HTTP status codes and response handling utilities (`status_code_category`, `status_message`, `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, `is_error`) using the standard library `http` module with input validation
- `tests/test_http_utils.py` — unit tests for `http_utils.py`
- Added `http_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `struct_utils.py` — Binary struct packing and unpacking utilities (`pack`, `unpack`, `pack_into`, `unpack_from`, `calcsize`, `is_valid_format`) wrapping the standard library `struct` module with input validation
- `tests/test_struct_utils.py` — unit tests for `struct_utils.py`
- Added `struct_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

### Fixed

- Completed the `struct_utils` sync that was partially done: added `struct_utils.py` and `tests/test_struct_utils.py` entries to `.kilo/command/scaffold-project.md`, added `struct_utils.py` / `tests/test_struct_utils.py` assertions to `tests/test_scaffold.py`, and added the `tests/test_struct_utils.py` entry to the scaffolded README tree in `scaffold.sh`.

- Synchronized `pyproject.toml` `py_modules` with the repository: added missing `duration_utils` and `xml_utils` modules (both exist as source files with tests and are already listed in `README.md`, `scaffold.sh`, and `.kilo/command/scaffold-project.md`) so package metadata matches the actual modules.

- `html_utils.py` — HTML escaping, unescaping, and tag-stripping utilities (`escape_html`, `unescape_html`, `strip_tags`, `escape_attribute`) using the standard library `html` module with input validation
- `tests/test_html_utils.py` — unit tests for `html_utils.py`
- Added `html_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `bytes_utils.py` — bytes and binary utilities (`to_hex`, `from_hex`, `xor`, `chunk`) for working with raw bytes and binary data with input validation
- `tests/test_bytes_utils.py` — unit tests for `bytes_utils.py`
- Fixed `scaffold.sh` syntax error introduced by a previous checkpoint commit: two bare module-list lines (missing `#   ` comment prefix) inside the script header broke bash parsing for project names containing parentheses. Replaced them with properly commented header lines and added the missing `bytes_utils.py` / `tests/test_bytes_utils.py` heredoc blocks so scaffolded projects generate the module and its tests. Added `bytes_utils` to `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `tests/test_scaffold.py` assertions.

- `base64_utils.py` — Base64 and hexadecimal encoding/decoding utilities (`base64_encode`, `base64_decode`, `base64_encode_bytes`, `base64_decode_bytes`, `hex_encode`, `hex_decode`, `is_valid_base64`, `is_valid_hex`) using the standard library `base64` module with input validation
- `tests/test_base64_utils.py` — unit tests for `base64_utils.py`
- Added `base64_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions

- `bit_utils.py` — bitwise utility functions for working with binary representations of integers (`count_set_bits`, `is_power_of_two`, `next_power_of_two`, `prev_power_of_two`, `reverse_bits`, `rotate_left`, `rotate_right`, `get_bit`, `set_bit`, `clear_bit`, `toggle_bit`, `is_even`, `is_odd`) with input validation
- `tests/test_bit_utils.py` — unit tests for `bit_utils.py`
- Added `bit_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `operator_utils.py` — operator utilities (`identity`, `negate`, `add`, `subtract`, `multiply`, `divide`, `power`, `modulo`, `clamp`, `between`) for common functional operations
- `tests/test_operator_utils.py` — unit tests for `operator_utils.py`
- Added `operator_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests

### Changed

- Synchronized `pyproject.toml` `py_modules` with the repository: added missing `prompt_utils` and `uuid_utils` modules (both exist as source files with tests and are already listed in `README.md`, `scaffold.sh`, and `.kilo/command/scaffold-project.md`) so package metadata matches the actual modules.

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `ini_utils.py` — INI configuration file utilities (`load_config`, `save_config`, `get_config_value`, `set_config_value`, `merge_configs`, `list_sections`, `has_section`, `get_section`) for working with INI-style config files using `configparser`
- `tests/test_ini_utils.py` — unit tests for `ini_utils.py`
- Added `ini_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests

- `cli_utils.py` — command-line interface utilities with `create_parser` (an `argparse` parser with `--verbose` and `--version`), `parse_arguments`, and `main_wrapper` (wraps a main function returning exit codes `0`, `1`, or `130`)
- `tests/test_cli_utils.py` — unit tests for `cli_utils.py`
- Added `cli_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests

### Fixed

- Fixed inconsistent indentation in the `README.md` project structure tree: `path_utils.py`, `color_utils.py`, `pattern_utils.py`, `functools_utils.py`, `config_schema.py`, `exceptions_utils.py`, `io_utils.py`, `compression_utils.py`, `ip_utils.py`, `regex_utils.py`, `terminal_utils.py`, and the `tests/` sub-section were indented with 4 extra leading spaces instead of aligning with their siblings; also fixed `test_type_utils.py`, `test_path_utils.py`, `test_color_utils.py`, `test_pattern_utils.py`, `test_functools_utils.py`, `test_exceptions_utils.py`, `test_io_utils.py`, `test_compression_utils.py`, `test_ip_utils.py`, `test_regex_utils.py`, and `test_config_schema.py` entries in the tests sub-section. Synchronized the same fix into `scaffold.sh`'s generated `README.md` template so scaffolded projects inherit consistent indentation.

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `collections_utils.py` — collection utilities (`chunk`, `flatten`, `deep_flatten`, `windowed`, `uniq`, `uniq_by`, `frequency`, `most_common`, `least_common`, `merge_dicts`, `to_deque`, `pluck`, `compact`, `partition_by`) for working with iterables and data structures
- `tests/test_collections_utils.py` — unit tests for `collections_utils.py`
- `regex_utils.py` — regular expression utilities (`compile_pattern`, `is_valid_pattern`, `match_pattern`, `search_pattern`, `find_all`, `replace_pattern`, `split_pattern`, `escape_pattern`, `extract_groups`, `named_groups`) for safe regex compilation, matching, extraction, and manipulation
- `tests/test_regex_utils.py` — unit tests for `regex_utils.py`
- `tests/test_io_utils.py` — unit tests for `io_utils.py`
- `pattern_utils.py` — design pattern utilities (`Singleton` metaclass/base class, `Factory`, `Observer`/`Observable`, `Strategy`/`StrategyContext`) for common object-oriented patterns
- `tests/test_pattern_utils.py` — unit tests for `pattern_utils.py`
- `functools_utils.py` — functional programming utilities (`compose`, `pipe`, `curry`, `apply`) for composing, piping, and currying functions
- `tests/test_functools_utils.py` — unit tests for `functools_utils.py`
- `color_utils.py` — color manipulation utilities (`validate_hex`, `hex_to_rgb`, `rgb_to_hex`, `rgb_to_hsl`, `hsl_to_rgb`, `get_luminance`, `get_contrast_ratio`, `is_accessible`, `adjust_brightness`, `blend_colors`) supporting hex strings and RGB tuples with WCAG 2.1 luminance and contrast calculations
- `tests/test_color_utils.py` — unit tests for `color_utils.py`
- Added `color_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `path_utils.py` — path manipulation utilities (`join_path`, `normalize_path`, `get_absolute_path`, `get_relative_path`, `get_parent_dir`, `get_file_name`, `get_file_stem`, `get_file_extension`, `change_extension`, `is_absolute`, `get_path_components`, `get_common_path`, `ensure_extension`)
- `tests/test_path_utils.py` — unit tests for `path_utils.py`
- Added `path_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `string_utils.py` — advanced string manipulation utilities (`slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `indent_text`, `remove_extra_whitespace`, `title_case`)
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- Added `string_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `statistics_utils.py` — statistical utility functions (`harmonic_mean`, `geometric_mean`, `median_even`, `percentile`, `covariance`, `correlation`, `z_score`, `normalize`) beyond `stats.py`
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`
- Added `statistics_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- Synchronized `scaffold.sh` templates (`scaffold-project.md`, generated `README.md`, generated `CHANGELOG.md`) to include `statistics_utils.py` entries
- Updated `test_scaffold.py` to verify `statistics_utils.py` and `tests/test_statistics_utils.py` generation
- Fixed `# --- statistics_utils.py ---` and `# --- tests/test_statistics_utils.py ---` heredoc blocks in `scaffold.sh` to generate the module and its tests in scaffolded projects
- `tree_utils.py` — tree and nested structure utilities (get_nested, set_nested, delete_nested, flatten_tree, unflatten_tree, map_tree, filter_tree)
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- Synchronized `scaffold.sh` to include `tree_utils.py` and its tests in header, `py_modules`, and heredocs
- Updated `README.md`, `.kilo/command/scaffold-project.md`, and `CHANGELOG.md` to list `tree_utils.py` and `tests/test_tree_utils.py`
- Updated `test_scaffold.py` to expect `tree_utils.py` and `tests/test_tree_utils.py` in scaffolded outputs
- `terminal_utils.py` — terminal output utilities (`supports_color`, `colorize`, `print_colored`, `clear_screen`, `get_terminal_size`, `ProgressBar`, `progress_bar`, `prompt`) for ANSI-colored terminal output, progress bars, and user input
- `tests/test_terminal_utils.py` — unit tests for `terminal_utils.py`
- Added `terminal_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- Updated `test_scaffold.py` to verify `terminal_utils.py` and `tests/test_terminal_utils.py` generation


### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `config_schema.py` — typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators such as `range_validator`, `choices_validator`, `email_validator`)
- `tests/test_config_schema.py` — unit tests for `config_schema.py`
- `exceptions_utils.py` — custom exception classes and error handling utilities (`ValidationError`, `ConfigurationError`, `NotFoundError`, `PermissionError_`, `TimeoutError_`) with error details support; helper functions `catch_and_wrap()`, `get_error_details()`, and `is_instance_of_any()` for flexible exception handling
- `tests/test_exceptions_utils.py` — unit tests for `exceptions_utils.py`


### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `cache_utils.py` — caching utilities module with `memoize` decorator factory (supporting `maxsize` LRU eviction and `typed` argument distinction), `clear_cache` helper to invalidate stored results, and `cache_info` helper to inspect cache statistics
- `tests/test_cache_utils.py` — unit tests for `cache_utils.py`
- `timing_utils.py` — performance measurement helpers with `timer` context manager, `elapsed_time` function, and `benchmark` decorator
- `tests/test_timing_utils.py` — unit tests for `timing_utils.py`
- `concurrent_utils.py` — concurrent execution utilities with `ThreadPool`, `ProcessPool`, `gather`, `run_async`, and `to_async` functions
- `tests/test_concurrent_utils.py` — unit tests for `concurrent_utils.py`
- `priority_queue_utils.py` — heap-based priority queue implementation with `PriorityQueue` class and helper functions
- `tests/test_priority_queue_utils.py` — unit tests for `priority_queue_utils.py`
- `rate_limiter_utils.py` — rate limiting utilities using token bucket algorithm with `RateLimiter`, `token_bucket`, and `rate_limit` decorator
- `tests/test_rate_limiter_utils.py` — unit tests for `rate_limiter_utils.py`
- `retry_utils.py` — retry utilities with `retry`, `retry_with_backoff`, and `retry_count` decorators for exponential backoff and jitter
- `tests/test_retry_utils.py` — unit tests for `retry_utils.py`
- `dict_utils.py` — dictionary utilities (deep merge, flatten/unflatten, safe get, invert, filter)
- `tests/test_dict_utils.py` — unit tests for `dict_utils.py`
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate/pretty print)
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`

### Fixed

- Removed three duplicate heredoc blocks from `scaffold.sh` (`tests/test_rate_limiter_utils.py`, `tests/test_retry_utils.py`, `tests/test_dict_utils.py`) — the second copies were missing the `if __name__ == "__main__"` guard and would have overwritten the correct files during scaffolding
- Added missing `json_utils.py` and `csv_utils.py` entries to `scaffold.sh` header comment, generated README tree, generated CHANGELOG, generated `.kilo/command/scaffold-project.md` template, repo `README.md` tree and module sections, repo `CHANGELOG.md` Unreleased section, and repo `pyproject.toml` `py_modules`


### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `config_utils.py` — configuration utilities module with `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs` functions for working with JSON configuration files
- `tests/test_config_utils.py` — unit tests for `config_utils.py`

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `random_utils.py` — random number generation and sampling utilities with `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_uniform`, and `random_gaussian` functions, each accepting an optional `seed` for reproducible results
- `tests/test_random_utils.py` — unit tests for `random_utils.py`
- `validation_utils.py` — input validation module with `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname` functions
- `tests/test_validation_utils.py` — unit tests for `validation_utils.py`
- `crypto_utils.py` — cryptographic utilities with `hash_string`, `generate_token`, `base64_encode`, and `base64_decode` functions
- `tests/test_crypto_utils.py` — unit tests for `crypto_utils.py`
- `list_utils.py` — advanced list manipulation utilities with `partition`, `group_by`, `safe_get`, `find`, `drop`, `take`, and `intersperse` functions
- `tests/test_list_utils.py` — unit tests for `list_utils.py`
- `env_utils.py` — environment variable handling utilities with `get_env`, `get_env_required`, `get_env_int`, `get_env_float`, `get_env_bool`, `set_env`, `ensure_env`, `unset_env`, and `prefix_env` functions
- `tests/test_env_utils.py` — unit tests for `env_utils.py`

### Fixed

- Synchronized `scaffold.sh` embedded `math_utils.py` template with the repository version, restoring full Args/Raises/Examples docstrings and the `n > 20` branch comment
- Synchronized `scaffold.sh` embedded `stats.py` template with the repository version: added Examples docstrings, deterministic mode tie-breaking, sample-variance element-count guard, and `float` return type on `mode`
- Synchronized `scaffold.sh` embedded `datetime_utils.py` template with the repository version: restored multiline function signatures and RST-style `` `` `` inline literals in docstrings
- Synchronized `scaffold.sh` embedded `tests/test_math_utils.py` template with the repository version, adding coprime/same GCD cases, zero LCM case, expanded prime edge cases, and `factorial(1)`/`fibonacci(6)` assertions
- Updated `scaffold.sh` embedded `.kilo/command/scaffold-project.md` template wording for the `kilo.json` scaffolder description to match the repo version
- Fixed inconsistent indentation in README.md project structure section (datetime_utils.py, file_utils.py, url_utils.py entries had extra leading spaces)
- Fixed inconsistent indentation in scaffold.sh README.md template for the same entries
- Removed duplicate `stats.py` heredoc section in `scaffold.sh` (was generated twice)
- Removed unused `import os` from `scaffold.sh`'s `file_utils.py` template (matches repo version)
- Added missing `math_utils.py` and `data_utils.py` entries to `scaffold.sh`'s generated `CHANGELOG.md` template
- Fixed `scaffold.sh` header comments to list all generated modules
- Fixed inconsistent indentation in repo's `.kilo/command/scaffold-project.md` (extra spaces on `file_utils.py`, `datetime_utils.py` entries)
- Fixed `data_utils.py` indentation in `scaffold.sh`'s generated `README.md` project structure section
- Synchronized `random_utils.py` and `validation_utils.py` modules across `scaffold.sh` embedded templates (`README.md`, `CHANGELOG.md`, `scaffold-project.md`), `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and `CHANGELOG.md`; added `validation_utils.py` and `crypto_utils.py` heredocs to `scaffold.sh`

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `url_utils.py` — URL and web utility module with `is_valid_url`, `extract_domain`, `get_query_params`, `get_query_param`, `add_query_param`, `remove_query_param`, and `build_url` functions
- `tests/test_url_utils.py` — unit tests for `url_utils.py`
- Updated scaffold template to generate `url_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include URL utilities
- Tests verifying `scaffold-project.md` and `CHANGELOG.md` list `url_utils.py` and its tests
- `LICENSE` — MIT license file (added to repo, scaffold.sh template, and scaffold-project.md)
- `PROJECT_YEARS` and `PROJECT_AUTHOR` variables in `scaffold.sh` for dynamic license generation
- Tests in `tests/test_scaffold.py` verifying all modules are listed in generated `scaffold-project.md` and `CHANGELOG.md`
- Tests verifying generated `file_utils.py` does not import unused `os` module
- Tests verifying `scaffold-project.md` list items have consistent formatting
- `LICENSE` entry added to `test_required_files_generated` in `tests/test_scaffold.py`

### Changed

- Synchronized `scaffold.sh` template with the repository: removed duplicate `stats.py` section, fixed `file_utils.py` import, added missing module entries to `scaffold-project.md` and `CHANGELOG.md` templates, fixed `README.md` project structure indentation, added `LICENSE` generation, and added `PROJECT_YEARS`/`PROJECT_AUTHOR` variables
- Added `LICENSE` file to the repository and `scaffold.sh` template, `scaffold-project.md` command doc, and README project structure
- `datetime_utils.py` — date and time utility module with `parse_datetime`, `format_datetime`, `days_between`, `is_leap_year`, `add_days`, and `get_weekday_name` functions
- `tests/test_datetime_utils.py` — unit tests for `datetime_utils.py`
- Updated scaffold template to generate `datetime_utils.py` and its tests
- Verified project foundation by running test suite, lint, and typecheck
- `strings.py` — string utility module with `reverse_string`, `is_palindrome`, and `count_vowels` functions
- `tests/test_strings.py` — unit tests for `strings.py`

### Fixed

- Removed duplicate `utils.py` and `tests/test_utils.py` entries from scaffold.sh's generated CHANGELOG.md (was listed 3 times instead of once)
- Added missing `utils.py` to the README.md project structure section
- Added missing `strings.py`, `utils.py`, `tests/test_strings.py`, and `tests/test_utils.py` to scaffold.sh's generated `scaffold-project.md` command doc and the repo's `.kilo/command/scaffold-project.md`
- Added `strings.py`, `utils.py`, `tests/test_strings.py`, and `tests/test_utils.py` to `test_required_files_generated` assertions in `tests/test_scaffold.py`
- Fixed `--no-test` argument parsing in `scaffold.sh` so the flag works regardless of argument position (previously only checked `$2`, causing `--no-test` as the third argument to be ignored and `--no-test` as the second argument to set `OUTPUT_DIR` incorrectly)
- Synchronized `scaffold.sh` embedded README.md with generated files: added `calculator.py`, `CHANGELOG.md`, `.pre-commit-config.yaml`, `.kilo/.gitignore`, and complete Makefile target table including `typecheck`, `pre-commit-install`, and `pre-commit-run`

### Tests

- Added `TestScaffoldNoTestFlag` test class verifying `--no-test` works as the third argument, without an output directory, and does not set `OUTPUT_DIR` to `--no-test`
- Added tests for README completeness (`test_readme_contains_calculator_and_new_files`, `test_readme_makefile_table_includes_all_targets`) and CHANGELOG completeness (`test_changelog_lists_new_files`)
- Added `tests/test_shapes.py` with unit tests for circle, rectangle, and triangle area/perimeter functions including input validation

### Changed

- Synchronized `scaffold.sh` with the repository: added generation of `calculator.py`, `tests/test_calculator.py`, `.pre-commit-config.yaml`, `CHANGELOG.md`, `.kilo/.gitignore`, ruff lint configuration in generated `pyproject.toml`, and `pre-commit-install`/`pre-commit-run` Makefile targets
- Updated `.kilo/command/scaffold-project.md` to document all generated files including the new calculator module, pre-commit config, and changelog
- Updated `README.md` project structure section to include all configuration files and new modules
- Added comprehensive tests in `tests/test_scaffold.py` for ruff config, Makefile targets, pre-commit hooks, and calculator operations

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `math_utils.py` — mathematical utility functions (factorial, fibonacci, gcd, lcm, is_prime, clamp)
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- Updated `scaffold.sh` to generate `math_utils.py` and its tests
- Updated scaffold tests to verify math utils generation
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include math utils
- `data_utils.py` — data utility module with `deep_copy`, `merge_dicts`, `pick`, `omit`, and `flatten_dict` functions
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- Updated scaffold template to generate `data_utils.py` and its tests
- Updated `tests/test_scaffold.py` to verify file_utils generation

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `file_utils.py` — file and path utility functions
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- Updated scaffold template to generate `file_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md` and `README.md` to include file utilities
- Updated `tests/test_scaffold.py` to verify file_utils generation
- Established project foundation by running test suite, lint, typecheck, and posted a task for next agent to scaffold a new project.

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `logging_utils.py` — logging configuration and helper utilities with `get_logger`, `configure_logging`, and a `log_calls` decorator for tracing function calls
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- Synchronized `scaffold.sh` templates (`scaffold-project.md`, generated `README.md`, generated `CHANGELOG.md`), repo `README.md`, repo `.kilo/command/scaffold-project.md`, and `tests/test_scaffold.py` to include the `logging_utils` module and its tests

### Fixed

- Fixed `scaffold.sh` README.md template Architecture section: added missing `config_utils.py` listing, added all missing test file entries (including `test_config_utils.py`), removed redundant `tests/` placeholder entry, and updated module descriptions to match the canonical README. Verified scaffold smoke test passes with all generated modules.
### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate/pretty print)
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- Updated `scaffold.sh` to generate `json_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include JSON utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`
- Updated `scaffold.sh`, `.kilo/command/scaffold-project.md`, and `README.md` to include CSV utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `set_utils.py` — set operation utilities (`is_subset`, `is_superset`, `intersection`, `union`, `difference`, `symmetric_difference`, `cartesian_product`, `power_set`)
- `tests/test_set_utils.py` — unit tests for `set_utils.py`
- Updated `scaffold.sh` to generate `set_utils.py` and its tests
- `statistics_utils.py` — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include set and statistics utilities
- `string_utils.py` — advanced string manipulation utilities (`slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `indent_text`, `remove_extra_whitespace`, `title_case`)
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and scaffold template to include string utilities
- `tree_utils.py` — tree and nested structure utilities (`get_nested`, `set_nested`, `delete_nested`, `flatten_tree`, `unflatten_tree`, `map_tree`, `filter_tree`)
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- Updated `scaffold.sh` to generate `tree_utils.py` and its tests
- `type_utils.py` — type introspection utilities (`is_optional`, `is_union`, `is_generic`, `get_type_args`, `type_name`, `is_subclass_safe`)
- `tests/test_type_utils.py` — unit tests for `type_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and scaffold template to include type utilities
- `uuid_utils.py` — UUID utility functions (generate_uuid, generate_uuid4, generate_uuid1, is_valid_uuid, parse_uuid)
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `prompt_utils.py` — Prompt utility functions (truncate_prompt, format_prompt_template, clean_prompt, extract_keywords, wrap_prompt, estimate_token_count)
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `async_utils.py` — asynchronous utility functions (`run_in_thread`, `gather_with_timeout`, `async_sleep`, `retry_async`)
- `tests/test_async_utils.py` — unit tests for `async_utils.py`
- Updated `scaffold.sh` to generate `async_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include async utilities
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and scaffold template to include uuid and prompt utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `compression_utils.py` — compression and decompression utilities (gzip, bz2, zip, tar) with support for bytes/strings and archive operations
- `tests/test_compression_utils.py` — unit tests for `compression_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and `pyproject.toml` to include compression utilities

### Added

- Added `weakref_utils.py` with weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`).
- `ip_utils.py` — IP address validation and manipulation utilities (IPv4/IPv6 validation, version detection, conversion between strings and integers, property checks like private/loopback/multicast/link-local/reserved, normalization, and subnet membership)
- `tests/test_ip_utils.py` — unit tests for `ip_utils.py`
- Updated `scaffold.sh`, `README.md`, `.kilo/command/scaffold-project.md`, and `pyproject.toml` to include IP utilities

- `os_utils.py` — operating system utilities (`get_platform_info`, `get_cpu_count`, `get_disk_usage`, `get_user_home`, `get_username`, `find_executable`, `expand_path`, `is_executable`) for inspecting the platform and environment using the standard library
- `tests/test_os_utils.py` — unit tests for `os_utils.py`
- Added `os_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions


## Bootstrap session

- Verified test suite passes (75 test modules).
