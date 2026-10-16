# Agentic Coding Scaffolding

A self-evolving scaffolding project for autonomous agentic coding loops powered by Kilo.

## Overview

This repository provides a foundation for agentic coding projects. It includes:

- A GitHub Actions workflow that runs a Kilo agent loop
- Project configuration for Kilo (AGENTS.md, kilo.json)
- Custom subagents and commands for scaffolding tasks
- A task handover protocol between agent sessions

## Architecture

```
.github/workflows/main.yml   # CI workflow: Kilo agent loop
.kilo/                       # Kilo project configuration
  agent/                     # Custom subagents
    scaffolder.md            # Scaffolder subagent definition
  command/                   # Custom commands
    handover.md              # Handover task command
    scaffold-project.md      # Scaffold-project command
  skill/                     # Custom skills
    scaffolding-helper.md    # Sample skill definition
  .gitignore                 # Ignore patterns for .kilo directory
.gitignore                   # Common ignore patterns
LICENSE                      # MIT License
.pre-commit-config.yaml      # Pre-commit hooks (ruff, mypy, tests, scaffold)
AGENTS.md                    # AI agent instructions
CHANGELOG.md                 # Changelog (Keep a Changelog format)
kilo.json                    # Kilo project configuration
Makefile                     # Common developer targets
pyproject.toml               # Python project configuration (pytest, ruff, mypy)
scaffold.sh                  # Project scaffolding script
hello.py                     # Sample application entry point
calculator.py                # Simple calculator module with arithmetic operations
config_utils.py              # Configuration utilities for JSON file management
shapes.py                    # Geometry utilities for areas and perimeters
strings.py                   # String utilities for text operations
utils.py                     # General utility helper functions
stats.py                     # Statistical utility functions
math_utils.py               # Mathematical utility functions
data_utils.py               # Data utility functions
datetime_utils.py           # Date and time utility functions
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
uuid_utils.py               # UUID utility functions for generating and validating UUIDs
prompt_utils.py             # Prompt utility functions for working with text prompts
random_utils.py             # Random number generation and sampling utilities
validation_utils.py         # Input validation utilities
crypto_utils.py             # Cryptographic utilities
list_utils.py              # Advanced list manipulation utilities
env_utils.py               # Environment variable handling utilities
logging_utils.py          # Logging configuration and helper utilities
cache_utils.py            # Caching utilities for memoizing function results
timing_utils.py           # Performance measurement helpers
async_utils.py            # Asynchronous utility functions
bit_utils.py              # Bitwise utility functions for working with binary representations
concurrent_utils.py       # Concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
priority_queue_utils.py   # Heap-based priority queue implementation
rate_limiter_utils.py     # Rate limiting utilities (token bucket algorithm)
retry_utils.py            # Retry utilities with exponential backoff and jitter
dict_utils.py            # Dictionary utilities (deep merge, flatten, unflatten, safe get, invert, filter)
json_utils.py            # JSON utility functions (read/write/parse/dump/validate)
collections_utils.py     # Collection utilities (chunk, flatten, frequency, merge_dicts, uniq, and more)
csv_utils.py             # CSV utility functions (read/write/append as dicts or lists)
set_utils.py             # Set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
statistics_utils.py        # Statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
string_utils.py            # Advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
tree_utils.py              # Tree and nested structure utilities (get/set/delete nested, flatten/unflatten, map/filter)
type_utils.py              # Type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
    path_utils.py              # Path manipulation utilities (join, normalize, components, extensions)
color_utils.py             # Color manipulation utilities (hex/rgb/hsl, luminance, contrast, accessibility)
cli_utils.py               # Command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
hash_utils.py              # Hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
pattern_utils.py           # Design pattern utilities (Singleton, Factory, Observer, Strategy)
functools_utils.py         # Functional programming utilities (compose, pipe, curry, apply)
config_schema.py           # Typed configuration schema utilities (SchemaField, ConfigSchema, validators)
exceptions_utils.py        # Custom exception classes and error handling utilities
io_utils.py                # Line-oriented and atomic input/output utilities
ini_utils.py                 # INI configuration file utilities (load, save, get, set, merge sections)
compression_utils.py       # Compression and decompression utilities (gzip, bz2, zip, tar)
ip_utils.py                # IP address validation and manipulation utilities
regex_utils.py             # Regular expression utilities (compile, match, search, replace, split, escape)
terminal_utils.py          # Terminal output utilities (ANSI color, progress bars, clear screen, prompts)
tests/                     # Python unit tests
  test_hello.py              # Tests for hello.py
  test_calculator.py         # Tests for calculator.py
  test_scaffold.py           # Tests for scaffold.sh
  test_config_utils.py       # Tests for config_utils.py
  test_shapes.py             # Tests for shapes.py
  test_strings.py            # Tests for strings.py
  test_utils.py              # Tests for utils.py
  test_stats.py              # Tests for stats.py
  test_math_utils.py         # Tests for math_utils.py
  test_data_utils.py         # Tests for data_utils.py
  test_datetime_utils.py     # Tests for datetime_utils.py
  test_file_utils.py         # Tests for file_utils.py
  test_url_utils.py          # Tests for url_utils.py
  test_random_utils.py       # Tests for random_utils.py
  test_validation_utils.py   # Tests for validation_utils.py
  test_crypto_utils.py       # Tests for crypto_utils.py
  test_list_utils.py         # Tests for list_utils.py
  test_env_utils.py          # Tests for env_utils.py
  test_logging_utils.py       # Tests for logging_utils.py
  test_cache_utils.py         # Tests for cache_utils.py
  test_timing_utils.py        # Tests for timing_utils.py
  test_async_utils.py         # Tests for async_utils.py
  test_bit_utils.py           # Tests for bit_utils.py
  test_concurrent_utils.py    # Tests for concurrent_utils.py
  test_priority_queue_utils.py # Tests for priority_queue_utils.py
  test_rate_limiter_utils.py  # Tests for rate_limiter_utils.py
  test_retry_utils.py         # Tests for retry_utils.py
  test_dict_utils.py         # Tests for dict_utils.py
  test_json_utils.py          # Tests for json_utils.py
  test_collections_utils.py   # Tests for collections_utils.py
  test_csv_utils.py           # Tests for csv_utils.py
  test_set_utils.py           # Tests for set_utils.py
  test_statistics_utils.py    # Tests for statistics_utils.py
  test_string_utils.py        # Tests for string_utils.py
  test_tree_utils.py         # Tests for tree_utils.py
  test_type_utils.py         # Tests for type_utils.py
  test_path_utils.py        # Tests for path_utils.py
  test_color_utils.py      # Tests for color_utils.py
  test_pattern_utils.py         # Tests for pattern_utils.py
  test_functools_utils.py       # Tests for functools_utils.py
  test_exceptions_utils.py    # Tests for exceptions_utils.py
  test_io_utils.py            # Tests for io_utils.py
  test_compression_utils.py   # Tests for compression_utils.py
  test_ip_utils.py             # Tests for ip_utils.py
  test_regex_utils.py         # Tests for regex_utils.py
  test_config_schema.py         # Tests for config_schema.py
    ```

## How It Works

The CI workflow (`main.yml`) runs a loop of Kilo agent sessions. Each session receives the prompt:

> Execute the task assigned by the previous agent and prepare a task for the next agent!

After each session, the workflow:

1. Checks out the repository
2. Runs `kilo run` with the handover command
3. Commits any changes (excluding workflow files)
4. Pushes to the default branch

This creates a continuous, evolving codebase where each agent session builds on the previous one.

## Task Handover Protocol

Tasks for the next agent are posted on the Kilo shared board. Each session:

1. Reads the board for any assigned task
2. Executes the task
3. Posts a new task for the next session

## Getting Started

### For CI (Automated)

The workflow runs automatically on a schedule or via `workflow_dispatch`.

### For Local Development

Install the Kilo CLI and run:

```bash
kilo run --auto "Execute the task assigned by the previous agent and prepare a task for the next agent!"
```

## Calculator Module

The project includes a simple calculator module in `calculator.py` with functions for basic arithmetic operations: add, subtract, multiply, and divide. The module is tested in `tests/test_calculator.py`.

## Shapes Module

The project includes a geometry utilities module in `shapes.py` with functions for calculating the area and perimeter of circles, rectangles, and triangles. Input validation enforces non-negative dimensions and the triangle inequality. The module is tested in `tests/test_shapes.py`.

## Strings Module

The project includes a string utilities module in `strings.py` with functions for common text operations: `reverse_string`, `is_palindrome`, and `count_vowels`. The `is_palindrome` function is case-insensitive and ignores non-alphanumeric characters. The module is tested in `tests/test_strings.py`.

## Statistics Module

The project includes a statistics utilities module in `stats.py` with functions for common statistical operations: `mean`, `median`, `mode`, `variance`, and `stddev`. The module supports both population and sample variance/stddev calculations. Input validation ensures appropriate errors for empty lists or invalid inputs. The module is tested in `tests/test_stats.py`.

## License

MIT

## Math Utilities Module

The project includes a mathematical utilities module in `math_utils.py` with functions for common mathematical operations: `factorial`, `fibonacci`, `gcd`, `lcm`, `is_prime`, and `clamp`. The module is tested in `tests/test_math_utils.py`.

## Data Utilities Module

The project includes a data utilities module in `data_utils.py` with functions for data manipulation: `deep_copy`, `merge_dicts`, `pick`, `omit`, and `flatten_dict`. The module is tested in `tests/test_data_utils.py`.

## Datetime Utilities Module

The project includes a date and time utilities module in `datetime_utils.py` with functions for date/time parsing, formatting, and arithmetic: `parse_datetime`, `format_datetime`, `days_between`, `is_leap_year`, `add_days`, and `get_weekday_name`. The module is tested in `tests/test_datetime_utils.py`.

## File Utilities Module

The project includes a file utilities module in `file_utils.py` with functions for file and path operations: `read_text`, `write_text`, `read_json`, `write_json`, `ensure_dir`, `list_files`, `copy_file`, and `delete_file`. The module is tested in `tests/test_file_utils.py`.

## URL Utilities Module

The project includes a URL and web utilities module in `url_utils.py` with functions for URL validation and manipulation: `is_valid_url`, `extract_domain`, `get_query_params`, `get_query_param`, `add_query_param`, `remove_query_param`, and `build_url`. The module is tested in `tests/test_url_utils.py`.

## Configuration Utilities Module

The project includes a configuration utilities module in `config_utils.py` with functions for loading, saving, and manipulating configuration files: `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs`. The module currently supports JSON format and is tested in `tests/test_config_utils.py`.

## Random Utilities Module

The project includes a random utilities module in `random_utils.py` with functions for random number generation and sampling: `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_uniform`, and `random_gaussian`. Every function accepts an optional `seed` argument for reproducible results and validates its inputs. The module is tested in `tests/test_random_utils.py`.

## Validation Utilities Module

The project includes a validation utilities module in `validation_utils.py` with functions for common input validation: `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname`. The module is tested in `tests/test_validation_utils.py`.

## Cryptographic Utilities Module

The project includes a cryptographic utilities module in `crypto_utils.py` with functions for hashing and encoding: `hash_string`, `generate_token`, `base64_encode`, and `base64_decode`. The module is tested in `tests/test_crypto_utils.py`.

## List Utilities Module

The project includes an advanced list manipulation utilities module in `list_utils.py` with functions for common list operations: `partition`, `group_by`, `safe_get`, `find`, `drop`, `take`, and `intersperse`. Input validation ensures all functions raise `TypeError` when a non-list is passed. The module is tested in `tests/test_list_utils.py`.

## Environment Utilities Module

The project includes an environment variable utilities module in `env_utils.py` with functions for reading, writing, and parsing environment variables: `get_env`, `get_env_required`, `get_env_int`, `get_env_float`, `get_env_bool`, `set_env`, `ensure_env`, `unset_env`, and `prefix_env`. Typed accessors parse values as `int`, `float`, and `bool`, with required-variable and default fallbacks. The module is tested in `tests/test_env_utils.py`.

## Logging Utilities Module

The project includes a logging utilities module in `logging_utils.py` with helpers for logging configuration and function-call tracing: `get_logger` returns a named logger (or the root logger), `configure_logging` configures the root logger with a consistent format, handlers, and level, and `log_calls` is a decorator factory that logs function entry and return values using `functools.wraps` to preserve metadata. The module is tested in `tests/test_logging_utils.py`.

## Cache Utilities Module

The project includes a caching utilities module in `cache_utils.py` with helpers for memoizing function results: `memoize` is a decorator factory that caches return values keyed by call arguments (with optional `maxsize` LRU eviction and `typed` argument distinction), `clear_cache` invalidates the cache of a memoized function, and `cache_info` returns a dictionary with `hits`, `misses`, `maxsize`, and `currsize` statistics. Decorated functions also expose `clear_cache` and `cache_info` attributes for direct introspection. The module is tested in `tests/test_cache_utils.py`.

## Timing Utilities Module

The project includes a performance measurement utilities module in `timing_utils.py` with helpers for measuring and benchmarking code execution: `timer` is a context manager for timing code blocks, `elapsed_time` calculates elapsed time since a start time, and `benchmark` is a decorator that runs a function multiple times and reports average execution time. The module is tested in `tests/test_timing_utils.py`.

## Concurrent Utilities Module

The project includes a concurrent execution utilities module in `concurrent_utils.py` with helpers for parallel and asynchronous processing: `ThreadPool` and `ProcessPool` context manager wrappers around the standard library executors, `gather` for running awaitables concurrently, `run_async` for running async coroutines from synchronous code, and `to_async` for converting synchronous functions to async. The module is tested in `tests/test_concurrent_utils.py`.

## Priority Queue Utilities Module

The project includes a priority queue utilities module in `priority_queue_utils.py` with a heap-based `PriorityQueue` implementation and helper functions. The queue uses a min-heap with an incrementing counter to preserve insertion order for equal priorities. It provides `push`, `pop`, `peek`, `is_empty`, `size`, `clear`, and convenience functions like `create_priority_queue` and `merge_queues`. The module is tested in `tests/test_priority_queue_utils.py`.

## Rate Limiter Utilities Module

The project includes a rate limiting utilities module in `rate_limiter_utils.py` implementing the token bucket algorithm. It provides a `RateLimiter` class, a `token_bucket` context manager, and a `rate_limit` decorator for limiting function call frequency. The module is tested in `tests/test_rate_limiter_utils.py`.

## Retry Utilities Module

The project includes a retry utilities module in `retry_utils.py` with decorators for retrying operations with backoff: `retry` for simple retries with fixed delay and backoff, `retry_with_backoff` for exponential backoff with optional jitter, and `retry_count` which returns the result along with the number of retries performed. The module is tested in `tests/test_retry_utils.py`.

## Dictionary Utilities Module

The project includes a dictionary utilities module in `dict_utils.py` with functions for deep merging, flattening/unflattening nested dictionaries, safe nested gets, dictionary inversion, and predicate-based filtering. The module is tested in `tests/test_dict_utils.py`.

## JSON Utilities Module

The project includes a JSON utilities module in `json_utils.py` with functions for reading, writing, parsing, serializing, validating, and pretty-printing JSON data. The module is tested in `tests/test_json_utils.py`.

## CSV Utilities Module

The project includes a CSV utilities module in `csv_utils.py` with functions for reading and writing CSV files as dictionaries or lists, and appending rows. The module is tested in `tests/test_csv_utils.py`.

## Set Utilities Module

The project includes a set operation utilities module in `set_utils.py` with functions for common set-theoretic and combinatorial operations: `is_subset`, `is_superset`, `intersection`, `union`, `difference`, `symmetric_difference`, `cartesian_product`, and `power_set`. The module is tested in `tests/test_set_utils.py`.

## Statistical Utilities Module

The project includes a statistical utilities module in `statistics_utils.py` with functions for data analysis beyond `stats.py`: `harmonic_mean`, `geometric_mean`, `median_even`, `percentile`, `covariance`, `correlation`, `z_score`, and `normalize`. The module is tested in `tests/test_statistics_utils.py`.

## String Utilities Module

The project includes a string utilities module in `string_utils.py` with advanced string manipulation functions: `slugify`, `camel_to_snake`, `snake_to_camel`, `pluralize`, `truncate`, `wrap_text`, `indent_text`, `remove_extra_whitespace`, and `title_case`. Each function validates its inputs and raises `TypeError` for non-string arguments. The module is tested in `tests/test_string_utils.py`.

## Type Utilities Module

The project includes a type introspection utilities module in `type_utils.py` with functions for inspecting Python type objects: `is_optional` detects `Optional[T]` / `Union[T, None]`, `is_union` detects any `Union` type, `is_generic` detects generic aliases like `List[int]`, `get_type_args` returns the type arguments of a generic, `type_name` produces a human-readable name for a type, and `is_subclass_safe` checks subclass relationships without raising `TypeError`. The module is tested in `tests/test_type_utils.py`.

## Path Utilities Module

The project includes a path manipulation utilities module in `path_utils.py` with functions for joining, normalizing, splitting, and inspecting filesystem paths: `join_path`, `normalize_path`, `get_absolute_path`, `get_relative_path`, `get_parent_dir`, `get_file_name`, `get_file_stem`, `get_file_extension`, `change_extension`, `is_absolute`, `get_path_components`, `get_common_path`, and `ensure_extension`. The module is tested in `tests/test_path_utils.py`.

## Color Utilities Module

The project includes a color manipulation utilities module in `color_utils.py` with functions for converting between color representations (hexadecimal, RGB, HSL), computing WCAG 2.1 relative luminance and contrast ratios, checking accessibility, and adjusting/blending colors: `validate_hex`, `hex_to_rgb`, `rgb_to_hex`, `rgb_to_hsl`, `hsl_to_rgb`, `get_luminance`, `get_contrast_ratio`, `is_accessible`, `adjust_brightness`, and `blend_colors`. Colors are accepted as either a hex string (``#RRGGBB``) or an RGB tuple. The module is tested in `tests/test_color_utils.py`.

## Design Pattern Utilities Module

The project includes a design pattern utilities module in `pattern_utils.py` with reusable implementations of common object-oriented design patterns: `Singleton` (a thread-safe metaclass and `SingletonBase` base class that restrict a class to a single instance), `Factory` (a registry-based factory that creates objects by name), `Observer`/`Observable` (a publish-subscribe mechanism for change notifications), and `Strategy`/`StrategyContext` (plug-and-play algorithm selection). The module is tested in `tests/test_pattern_utils.py`.

## Configuration Schema Module

The project includes a configuration schema module in `config_schema.py` with declarative, typed configuration schemas. `SchemaField` describes a single typed field (`str`, `int`, `float`, `bool`) with optional defaults, required flags, and validators, and `ConfigSchema` composes fields to validate, coerce, and normalize configuration dictionaries. Built-in validators include `int_validator`, `float_validator`, `str_validator`, `bool_validator`, `email_validator`, `hostname_validator`, `url_validator`, `range_validator`, `choices_validator`, and `regex_validator`. The module is tested in `tests/test_config_schema.py`.

Completed task: Added a new `config_schema.py` module with typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators such as `range_validator`, `choices_validator`, `email_validator`) and its tests. Synchronized the scaffold template: added `config_schema.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, `scaffold.sh` heredocs for the module and its tests, and `tests/test_scaffold.py` assertions. Verified all tests pass, ruff and mypy are clean.

## Exception Utilities Module

The project includes custom exception types and utilities in `exceptions_utils.py`: custom exceptions (`ValidationError`, `ConfigurationError`, `NotFoundError`, `PermissionError_`, `TimeoutError_`) with support for error details and field metadata; helper functions `catch_and_wrap()` to catch and wrap exceptions while preserving the cause, `get_error_details()` to extract exception type/message/traceback as a dict, and `is_instance_of_any()` to test for membership in an exception tuple. The module is tested in `tests/test_exceptions_utils.py`.

## IO Utilities Module

The project includes line-oriented and atomic input/output utilities in `io_utils.py`: `read_lines` and `write_lines` for line-based file IO, `append_text` to append to files, `atomic_write_text` to write content atomically via a temp file and `os.replace`, `stream_copy` to copy file contents in chunks, `count_lines` to count lines, and `iter_lines` to stream lines without loading the file into memory. The module is tested in `tests/test_io_utils.py`.

## Terminal Utilities Module

The project includes terminal output utilities in `terminal_utils.py` for formatting terminal output with ANSI escape sequences: `supports_color` detects color support, `colorize` and `print_colored` render text in ANSI colors (black, red, green, yellow, blue, magenta, cyan, white) with optional bold, `clear_screen` clears the terminal, `get_terminal_size` returns the `(columns, lines)`, `ProgressBar` renders a terminal progress bar (usable as a context manager), `progress_bar` wraps an iterable with a progress bar, and `prompt` reads user input with an optional default. Color output is automatically disabled when the stream is not a TTY or the `NO_COLOR` environment variable is set. The module is tested in `tests/test_terminal_utils.py`.

## Async Utilities Module

The project includes asynchronous utility functions in `async_utils.py` for running blocking code in threads, gathering coroutines with timeouts, sleeping asynchronously, and retrying async operations: `run_in_thread`, `gather_with_timeout`, `async_sleep`, and `retry_async`. The module is tested in `tests/test_async_utils.py`.

## Bit Utilities Module

The project includes bitwise utility functions in `bit_utils.py` for working with binary representations of non-negative integers: `count_set_bits` counts the number of 1 bits, `is_power_of_two` tests whether a value is a power of two, `next_power_of_two` and `prev_power_of_two` find the nearest power of two, `reverse_bits` reverses bits within a width, `rotate_left` and `rotate_right` rotate bits, `get_bit`, `set_bit`, `clear_bit`, and `toggle_bit` read or modify individual bits, and `is_even`/`is_odd` test parity. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_bit_utils.py`.

## Collections Utilities Module

The project includes collection utilities in `collections_utils.py` for working with iterables and data structures: `chunk`, `flatten`, `deep_flatten`, `windowed`, `uniq`, `uniq_by`, `frequency`, `most_common`, `least_common`, `merge_dicts`, `to_deque`, `pluck`, `compact`, and `partition_by`. The module is tested in `tests/test_collections_utils.py`.

## Compression Utilities Module

The project includes compression and decompression utilities in `compression_utils.py` supporting gzip, bz2, zip, and tar formats for bytes/strings and archive operations. The module is tested in `tests/test_compression_utils.py`.

## Functools Utilities Module

The project includes functional programming utilities in `functools_utils.py` for composing, piping, and currying functions: `compose`, `pipe`, `curry`, and `apply`. The module is tested in `tests/test_functools_utils.py`.

## IP Utilities Module

The project includes IP address validation and manipulation utilities in `ip_utils.py` for IPv4/IPv6 validation, version detection, conversion between strings and integers, and property checks: `is_valid_ip`, `is_valid_ipv4`, `is_valid_ipv6`, `get_ip_version`, `ip_to_int`, and `int_to_ip`. The module is tested in `tests/test_ip_utils.py`.

## Prompt Utilities Module

The project includes prompt utility functions in `prompt_utils.py` for working with text prompts: `truncate_prompt`, `format_prompt_template`, `clean_prompt`, `extract_keywords`, `wrap_prompt`, and `estimate_token_count`. The module is tested in `tests/test_prompt_utils.py`.

## Regex Utilities Module

The project includes regular expression utilities in `regex_utils.py` for safe regex compilation, matching, extraction, and manipulation: `compile_pattern`, `is_valid_pattern`, `match_pattern`, `search_pattern`, `find_all`, `replace_pattern`, `split_pattern`, `escape_pattern`, `extract_groups`, and `named_groups`. The module is tested in `tests/test_regex_utils.py`.

## Tree Utilities Module

The project includes tree and nested structure utilities in `tree_utils.py` for getting, setting, deleting, flattening, unflattening, mapping, and filtering nested structures: `get_nested`, `set_nested`, `delete_nested`, `flatten_tree`, `unflatten_tree`, `map_tree`, and `filter_tree`. The module is tested in `tests/test_tree_utils.py`.

## UUID Utilities Module

The project includes UUID utility functions in `uuid_utils.py` for generating and validating UUIDs: `generate_uuid`, `generate_uuid4`, `generate_uuid1`, `is_valid_uuid`, and `parse_uuid`. The module is tested in `tests/test_uuid_utils.py`.

## Utils Module

The project includes general utility helper functions in `utils.py`: `flatten`, `chunk`, `unique`, and `is_empty`. The module is tested in `tests/test_utils.py`.

## CLI Utilities Module

The project includes command-line interface utilities in `cli_utils.py` for building simple CLI applications: `create_parser` builds an :mod:`argparse` parser with standard ``--verbose`` and ``--version`` options, `parse_arguments` parses command-line arguments, and `main_wrapper` wraps a main function to return consistent process exit codes (``0`` on success, ``1`` on error, ``130`` on keyboard interrupt). The module is tested in `tests/test_cli_utils.py`.

## Hashing and Checksum Utilities Module

The project includes hashing and checksum utilities in `hash_utils.py` for computing cryptographic hashes and checksums: `md5`, `sha1`, `sha256`, `sha512`, `crc32`, and `hash_file`. Both string and bytes inputs are supported, and `hash_file` supports multiple algorithms. The module is tested in `tests/test_hash_utils.py`.

## INI Configuration Utilities Module

The project includes an INI configuration utilities module in `ini_utils.py` for working with INI-style configuration files: `load_config`, `save_config`, `get_config_value`, `set_config_value`, `merge_configs`, `list_sections`, `has_section`, and `get_section`. Section-based access uses dot notation (``section.key``), keys preserve their case, and parent directories are created automatically on save. The module is tested in `tests/test_ini_utils.py`.

