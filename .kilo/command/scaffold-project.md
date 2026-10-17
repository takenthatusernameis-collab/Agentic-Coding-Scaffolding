---
description: Scaffold a new project structure for agentic coding
---

Generate scaffolding files for a new agentic coding project. This command creates:

- `.github/workflows/main.yml` — CI workflow for the Kilo agent loop
- `AGENTS.md` — AI agent instructions with task handover protocol
- `README.md` — project overview and getting-started guide
- `CHANGELOG.md` — changelog following Keep a Changelog format
- `.pre-commit-config.yaml` — pre-commit hooks for ruff, mypy, tests, and scaffold smoke testing
- `kilo.json` — Kilo project configuration, including the `scaffolder` subagent
- `.kilo/agent/scaffolder.md` — subagent definition for scaffolding tasks
- `.kilo/command/handover.md` — handover command for task handoffs
- `.kilo/command/scaffold-project.md` — scaffold-project command documentation
- `.kilo/skill/scaffolding-helper.md` — sample skill definition
- `.kilo/.gitignore` — ignore patterns for the .kilo directory
- `.gitignore` — common ignore patterns
- `LICENSE` — MIT license file
- `Makefile` — common developer targets (test, lint, typecheck, run, scaffold, clean, help, pre-commit-install, pre-commit-run)
- `pyproject.toml` — Python project configuration with pytest, ruff, and mypy settings
- `hello.py` — sample application entry point
- `calculator.py` — simple calculator module with arithmetic operations
- `config_utils.py` — configuration utilities for JSON file management
- `collections_utils.py` — collection utilities (chunk, flatten, deep_flatten, windowed, uniq, frequency, merge_dicts, and more)
- `shapes.py` — geometry utilities for areas and perimeters of common shapes
- `strings.py` — string utilities for text operations
- `utils.py` — general utility helper functions
- `stats.py` — statistical utility functions
- `math_utils.py` — mathematical utility functions
- `statistics_utils.py` — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
- `string_utils.py` — advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
- `data_utils.py` — data utility functions
- `datetime_utils.py` — date and time utility functions
- `file_utils.py` — file and path utility functions
- `url_utils.py` — URL and web utility functions
- `uuid_utils.py` — UUID utility functions for generating and validating UUIDs
- `prompt_utils.py` — Prompt utility functions for working with text prompts
- `random_utils.py` — random number generation and sampling utilities
- `validation_utils.py` — input validation utilities
- `crypto_utils.py` — cryptographic utilities
- `list_utils.py` — advanced list manipulation utilities
- `locale_utils.py` — locale utility functions for working with locale identifiers and language tags
- `env_utils.py` — environment variable handling utilities
- `logging_utils.py` — logging configuration and helper utilities
- `cache_utils.py` — caching utilities for memoizing function results
- `context_utils.py` — context manager utilities (`chdir`, `temp_environ`, `redirect_stdout`, `redirect_stderr`, `suppress`) for temporarily altering the runtime environment
- `timing_utils.py` — performance measurement helpers
- `async_utils.py` — asynchronous utility functions
- `bit_utils.py` — bitwise utility functions for working with binary representations of integers
- `concurrent_utils.py` — concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
- `priority_queue_utils.py` — heap-based priority queue implementation
- `rate_limiter_utils.py` — rate limiting utilities (token bucket algorithm)
- `retry_utils.py` — retry utilities with exponential backoff and jitter
- `tests/test_hello.py` — unit tests for `hello.py`
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `tests/test_config_utils.py` — unit tests for the config utilities module
- `tests/test_collections_utils.py` — unit tests for `collections_utils.py`
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `tests/test_strings.py` — unit tests for `strings.py`
- `tests/test_utils.py` — unit tests for `utils.py`
- `tests/test_stats.py` — unit tests for `stats.py`
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- `tree_utils.py` — tree and nested structure utilities (get/set/delete nested, flatten/unflatten, map/filter)
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- `type_utils.py` — type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
- `tests/test_type_utils.py` — unit tests for the type utilities module
- `path_utils.py` — path manipulation utilities (join, normalize, components, extensions)
- `tests/test_path_utils.py` — unit tests for `path_utils.py`
- `color_utils.py` — color manipulation utilities (hex/rgb/hsl, luminance, contrast, accessibility)
- `pattern_utils.py` — design pattern utilities (Singleton, Factory, Observer, Strategy)
- `tests/test_color_utils.py` — unit tests for `color_utils.py`
- `tests/test_pattern_utils.py` — unit tests for `pattern_utils.py`
- `regex_utils.py` — regular expression utilities (`compile_pattern`, `is_valid_pattern`, `match_pattern`, `search_pattern`, `find_all`, `replace_pattern`, `split_pattern`, `escape_pattern`, `extract_groups`, `named_groups`)
- `tests/test_regex_utils.py` — unit tests for `regex_utils.py`
- `functools_utils.py` — functional programming utilities (compose, pipe, curry, apply)
- `tests/test_functools_utils.py` — unit tests for `functools_utils.py`
- `config_schema.py` — typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators)
- `tests/test_config_schema.py` — unit tests for `config_schema.py`
- `exceptions_utils.py` — custom exception classes and error handling utilities
- `tests/test_exceptions_utils.py` — unit tests for `exceptions_utils.py`
- `io_utils.py` — line-oriented and atomic input/output utilities (`read_lines`, `write_lines`, `append_text`, `atomic_write_text`, `stream_copy`, `count_lines`, `iter_lines`)
- `ini_utils.py` — INI configuration file utilities (`load_config`, `save_config`, `get_config_value`, `set_config_value`, `merge_configs`, `list_sections`, `has_section`, `get_section`)
- `compression_utils.py` — compression and decompression utilities (gzip, bz2, zip, tar)
- `ip_utils.py` — IP address validation and manipulation utilities (IPv4/IPv6, conversion, properties, subnet checks)
- `tests/test_io_utils.py` — unit tests for `io_utils.py`
- `tests/test_ini_utils.py` — unit tests for `ini_utils.py`
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- `tests/test_datetime_utils.py` — unit tests for `datetime_utils.py`
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- `tests/test_url_utils.py` — unit tests for `url_utils.py`
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `tests/test_random_utils.py` — unit tests for `random_utils.py`
- `tests/test_validation_utils.py` — unit tests for `validation_utils.py`
- `tests/test_crypto_utils.py` — unit tests for `crypto_utils.py`
- `tests/test_list_utils.py` — unit tests for `list_utils.py`
- `tests/test_locale_utils.py` — unit tests for `locale_utils.py`
- `tests/test_env_utils.py` — unit tests for `env_utils.py`
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- `tests/test_cache_utils.py` — unit tests for `cache_utils.py`
- `tests/test_context_utils.py` — unit tests for `context_utils.py`
- `tests/test_timing_utils.py` — unit tests for `timing_utils.py`
- `tests/test_async_utils.py` — unit tests for `async_utils.py`
- `tests/test_bit_utils.py` — unit tests for `bit_utils.py`
- `tests/test_concurrent_utils.py` — unit tests for `concurrent_utils.py`
- `tests/test_priority_queue_utils.py` — unit tests for `priority_queue_utils.py`
- `tests/test_rate_limiter_utils.py` — unit tests for `rate_limiter_utils.py`
- `tests/test_retry_utils.py` — unit tests for `retry_utils.py`
- `dict_utils.py` — dictionary utilities (deep merge, flatten/unflatten, safe get, invert, filter)
- `tests/test_dict_utils.py` — unit tests for `dict_utils.py`
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate)
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`
- `set_utils.py` — set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
- `tests/test_set_utils.py` — unit tests for `set_utils.py`
- `tests/test_color_utils.py` — unit tests for `color_utils.py`
- `terminal_utils.py` — terminal output utilities (ANSI color, progress bars, clear screen, prompts)
- `tests/test_terminal_utils.py` — unit tests for `terminal_utils.py`
- `subprocess_utils.py` — subprocess utilities (`run_command`, `check_output`, `check_call`) using the standard library `subprocess` module with input validation
- `tests/test_subprocess_utils.py` — unit tests for `subprocess_utils.py`
- `cli_utils.py` — command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
- `tests/test_cli_utils.py` — unit tests for `cli_utils.py`
- `hash_utils.py` — hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
- `tests/test_hash_utils.py` — unit tests for `hash_utils.py`
- `http_utils.py` — HTTP status codes and response handling utilities (`status_code_category`, `status_message`, `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, `is_error`)
- `tests/test_http_utils.py` — unit tests for `http_utils.py`
- `html_utils.py` — HTML escaping, unescaping, and tag-stripping utilities (`escape_html`, `unescape_html`, `strip_tags`, `escape_attribute`)
- `tests/test_html_utils.py` — unit tests for `html_utils.py`
- `bytes_utils.py` — bytes and binary utilities (`to_hex`, `from_hex`, `xor`, `chunk`)
- `tests/test_bytes_utils.py` — unit tests for `bytes_utils.py`
- `base64_utils.py` — Base64 and hexadecimal encoding/decoding utilities (`base64_encode`, `base64_decode`, `base64_encode_bytes`, `base64_decode_bytes`, `hex_encode`, `hex_decode`, `is_valid_base64`, `is_valid_hex`)
- `tests/test_base64_utils.py` — unit tests for `base64_utils.py`
- `calendar_utils.py` — calendar utilities (`is_leap_year`, `days_in_month`, `first_day_of_month`, `month_name`, `day_name`, `month_calendar`, `weekdays_in_month`, `weekend_days_in_month`, `is_weekend`, `add_months`)
- `tests/test_calendar_utils.py` — unit tests for `calendar_utils.py`
- `struct_utils.py` — Binary struct packing and unpacking utilities (`pack`, `unpack`, `pack_into`, `unpack_from`, `calcsize`, `is_valid_format`)
- `tests/test_struct_utils.py` — unit tests for `struct_utils.py`
- `duration_utils.py` — time duration utilities (`parse_duration`, `format_duration`, `seconds_to_hms`, `hms_to_seconds`, `to_seconds`, `duration_between`, `add_duration`, `is_valid_duration`)
- `tests/test_duration_utils.py` — unit tests for `duration_utils.py`
- `temp_utils.py` — temporary file and directory management utilities (`create_temp_file`, `create_temp_dir`, `temp_file`, `temp_dir`, `write_temp_file`, `read_temp_file`, `cleanup_temp_path`, `is_temp_path`, `temp_path_exists`)
- `tests/test_temp_utils.py` — unit tests for `temp_utils.py`
- `xml_utils.py` — XML parsing and generation utilities (`parse_xml`, `parse_xml_string`, `build_xml`, `add_child`, `set_attribute`, `get_attribute`, `element_to_dict`, `dict_to_element`, `find_elements`, `find_element`, `get_element_text`, `set_element_text`, `xml_to_string`, `validate_well_formed`)
- `tests/test_xml_utils.py` — unit tests for `xml_utils.py`
- `seq_utils.py` — sequence utilities (`first`, `last`, `nth`, `head`, `tail`, `split_at`, `take_while`, `drop_while`, `interleave`, `adjacent_pairs`, `is_sorted`)
- `tests/test_seq_utils.py` — unit tests for `seq_utils.py`
- `number_utils.py` — number utility functions (`clamp`, `round_to`, `is_integer`, `format_number`, `percentage`)
- `tests/test_number_utils.py` — unit tests for `number_utils.py`
- `os_utils.py` — operating system utilities (platform info, CPU count, disk usage, user info, executable lookup)
- `tests/test_os_utils.py` — unit tests for `os_utils.py`
- `sort_utils.py` — sorting utility functions (`is_sorted`, `bubble_sort`, `merge_sort`, `nth_largest`, `top_n`)
- `tests/test_sort_utils.py` — unit tests for `sort_utils.py`
- `graphlib_utils.py` — graph and dependency resolution utilities (`topological_sort`, `has_cycle`, `dependency_order`, `is_valid_ordering`) for topological sorting and cycle detection of directed graphs
- `tests/test_graphlib_utils.py` — unit tests for `graphlib_utils.py`
- `queue_utils.py` — FIFO queue helpers (`Queue` class, `enqueue`, `dequeue`, `peek`, `size`, `is_empty`, `clear`)
- `tests/test_queue_utils.py` — unit tests for `queue_utils.py`
- `version_utils.py` — version parsing, comparison, and normalization utilities
- `tests/test_version_utils.py` — unit tests for `version_utils.py`
- `sys_utils.py` — Python runtime and system information utilities (`get_python_version`, `get_executable`, `get_platform`, `get_path`, `get_argv`, `get_recursion_limit`, `set_recursion_limit`, stream encodings, frame info, refcount)
- `tests/test_sys_utils.py` — unit tests for `sys_utils.py`
- `networking_utils.py` — networking utilities for TCP ports, hostname resolution, and local IP detection
- `tests/test_networking_utils.py` — unit tests for `networking_utils.py`
- `operator_utils.py` — operator utilities (`identity`, `negate`, `add`, `subtract`, `multiply`, `divide`, `power`, `modulo`, `clamp`, `between`) for common functional operations
- `tests/test_operator_utils.py` — unit tests for `operator_utils.py`
- `textwrap_utils.py` — text wrapping utilities (`wrap_text`, `shorten_text`, `dedent_text`, `indent_text`, `fill_text`)
- `tests/test_textwrap_utils.py` — unit tests for `textwrap_utils.py`
- `prime_utils.py` — prime number utilities (`prime_factors`, `nth_prime`, `primes_up_to`, `next_prime`, `previous_prime`)
- `tests/test_prime_utils.py` — unit tests for `prime_utils.py`
- `decimal_utils.py` — decimal arithmetic utilities (`to_decimal`, `add`, `subtract`, `multiply`, `divide`, `power`, `quantize`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, `is_zero`)
- `tests/test_decimal_utils.py` — unit tests for `decimal_utils.py`
- `fractions_utils.py` — fraction arithmetic utilities (`to_fraction`, `add`, `subtract`, `multiply`, `divide`, `power`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, `is_zero`, `is_integer`, `numerator`, `denominator`, `to_float`, `from_float`)
- `tests/test_fractions_utils.py` — unit tests for `fractions_utils.py`
- `weakref_utils.py` — weak reference utilities (`WeakRef`, `WeakMethod`, `create_weakref`, `create_proxy`, `get_object`, `is_alive`, `create_finalizer`)
- `tests/test_weakref_utils.py` — unit tests for `weakref_utils.py`
- `heapq_utils.py` — heap queue utilities wrapping the standard library `heapq` module (`heapify`, `heappush`, `heappop`, `heapreplace`, `heappushpop`, `merge`, `nlargest`, `nsmallest`)
- `tests/test_heapq_utils.py` — unit tests for `heapq_utils.py`
- `markdown_utils.py` — Markdown utility functions (`extract_code_blocks`, `strip_markdown`, `count_words`, `is_heading`, `heading_level`)
- `tests/test_markdown_utils.py` — unit tests for `markdown_utils.py`
- `time_utils.py` — time utility functions for working with timestamps and durations (`now_epoch`, `now_iso`, `epoch_to_iso`, `iso_to_epoch`)
- `tests/test_time_utils.py` — unit tests for `time_utils.py`
- `semver_utils.py` — Semantic versioning utilities (`parse_semver`, `compare_semver`, `bump_major`, `bump_minor`, `bump_patch`, `is_valid_semver`, `SemanticVersion`)
- `tests/test_semver_utils.py` — unit tests for `semver_utils.py`
- `template_utils.py` — string template rendering utilities (`render_template`, `substitute`, `safe_substitute`, `render_from_dict`, `has_placeholders`, `extract_placeholders`) supporting `str.format()` and `string.Template` styles with placeholder extraction
- `tests/test_template_utils.py` — unit tests for `template_utils.py`

## Usage

```bash
scaffold-project <project-name> [output-dir] [--no-test]
```

After scaffolding, `scaffold.sh` runs a smoke test (unittest) in the new project
to verify the generated files work. Pass `--no-test` to skip it.

## Examples

```bash
scaffold-project "My AI Project"
scaffold-project my-cool-tool /tmp/projects/my-tool
scaffold-project my-cool-tool ./out --no-test
```
