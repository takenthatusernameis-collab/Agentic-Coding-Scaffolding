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
template_utils.py           # String template rendering utilities (render_template, substitute, safe_substitute, render_from_dict, has_placeholders, extract_placeholders)
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
uuid_utils.py               # UUID utility functions for generating and validating UUIDs
prompt_utils.py             # Prompt utility functions for working with text prompts
random_utils.py             # Random number generation and sampling utilities
validation_utils.py         # Input validation utilities
crypto_utils.py             # Cryptographic utilities
list_utils.py              # Advanced list manipulation utilities
locale_utils.py           # Locale utility functions for working with locale identifiers and language tags
env_utils.py               # Environment variable handling utilities
logging_utils.py          # Logging configuration and helper utilities
cache_utils.py            # Caching utilities for memoizing function results
memoize_utils.py          # Memoization utilities (memoize decorator) with cache_clear
context_utils.py          # Context manager utilities for temporarily altering the runtime environment (working directory, environment variables, standard streams)
itertools_utils.py         # Iteration helpers wrapping itertools (chain, flatten, chunk, product, combinations, permutations, etc.)
timing_utils.py           # Performance measurement helpers
async_utils.py            # Asynchronous utility functions
bit_utils.py              # Bitwise utility functions for working with binary representations
call_once_utils.py        # Call-once execution utilities (call_once decorator)
concurrent_utils.py       # Concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
priority_queue_utils.py   # Heap-based priority queue implementation
queue_utils.py            # FIFO queue helpers (enqueue, dequeue, peek, size, is_empty)
rate_limiter_utils.py     # Rate limiting utilities (token bucket algorithm)
retry_utils.py            # Retry utilities with exponential backoff and jitter
ring_buffer_utils.py     # Fixed-size circular (ring) buffer utilities
secrets_utils.py           # Cryptographically secure secrets and token utilities (token_bytes, token_hex, token_urlsafe, compare_digest, randbelow, randbits, choice)
selectors_utils.py           # Selectors utilities wrapping the standard library selectors module (create_default_selector, register, unregister, select, get_key, get_map, close_selector)
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
duration_utils.py          # Time duration utilities (parse, format, convert between units)
temp_utils.py              # Temporary file and directory management utilities
xml_utils.py               # XML parsing and generation utilities
seq_utils.py               # Sequence utilities (first, last, nth, head, tail, split_at, take_while, drop_while, interleave, adjacent_pairs, is_sorted)
number_utils.py            # Number utility functions (clamp, round_to, is_integer, format_number, percentage)
os_utils.py                # Operating system utilities (platform info, CPU count, disk usage, user info, executable lookup)
sort_utils.py              # Sorting utility functions (is_sorted, bubble_sort, merge_sort, nth_largest, top_n)
sys_utils.py               # Python runtime and system information utilities (version, argv, executable, recursion limit, stream encodings)
threading_utils.py         # Threading utilities wrapping the standard library threading module
networking_utils.py         # Networking utilities for TCP ports, hostname resolution, and local IP detection
graphlib_utils.py          # Graph and dependency resolution utilities (topological sort, cycle detection)
greeting_utils.py          # Greeting utilities (greet, format_names, random_greeting)
version_utils.py           # Version utility functions (parse, compare, normalize)
semver_utils.py            # Semantic versioning utilities
shutil_utils.py            # High-level file operations (copy, move, remove, archive, disk usage)
socketserver_utils.py           # Socketserver utilities wrapping the standard library socketserver module
inspect_utils.py           # Callable and object introspection utilities (name, signature, parameters, source)
interval_utils.py          # Interval utilities (normalization, containment, overlap, intersection, union, merge)
textwrap_utils.py          # Text wrapping utilities (wrap_text, shorten_text, dedent_text, indent_text, fill_text)
prime_utils.py             # Prime number utilities (prime_factors, nth_prime, primes_up_to, next_prime, previous_prime)
decimal_utils.py           # Decimal arithmetic utilities (to_decimal, add, subtract, multiply, divide, power, quantize, compare, abs_value, negate, is_positive, is_negative, is_zero)
difflib_utils.py           # Difflib utility functions for sequence comparison and diffing
fractions_utils.py         # Fraction arithmetic utilities (to_fraction, add, subtract, multiply, divide, power, compare, abs_value, negate, is_positive, is_negative, is_zero, is_integer, numerator, denominator, to_float, from_float)
heapq_utils.py             # Heap queue utilities wrapping stdlib heapq (heapify, heappush, heappop, heapreplace, heappushpop, merge, nlargest, nsmallest)
markdown_utils.py          # Markdown utility functions (extract code blocks, strip formatting, count words, heading detection)
time_utils.py              # Time utility functions (now_epoch, now_iso, epoch_to_iso, iso_to_epoch)
timezone_utils.py          # Time zone utilities (IANA lookups, conversion, formatting, DST) wrapping stdlib zoneinfo
cli_utils.py               # Command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
hash_utils.py              # Hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
hmac_utils.py              # HMAC-based message authentication utilities (MD5, SHA1, SHA256, SHA512) with constant-time verification
http_utils.py              # HTTP status codes and response handling utilities
id_utils.py                # Identifier generation and validation utilities (generate_id, new_id, is_valid_id)
html_utils.py              # HTML escaping, unescaping, and tag-stripping utilities
bytes_utils.py             # Bytes and binary utilities (to_hex, from_hex, xor, chunk)
circuit_breaker_utils.py   # Circuit breaker resilience utilities (CircuitBreaker, CircuitOpenError) with thread-safe state transitions
array_utils.py             # Array utility functions wrapping the standard library array module
base64_utils.py            # Base64 and hexadecimal encoding/decoding utilities
bisect_utils.py            # Bisect utility functions for binary search on sorted sequences
calendar_utils.py            # Calendar utilities for date and month calculations (is_leap_year, days_in_month, month_name, day_name, add_months)
cmath_utils.py               # Complex mathematics utilities wrapping the standard library cmath module
struct_utils.py            # Binary struct packing and unpacking utilities
pattern_utils.py           # Design pattern utilities (Singleton, Factory, Observer, Strategy)
functools_utils.py         # Functional programming utilities (compose, pipe, curry, apply)
operator_utils.py          # Operator utilities (identity, negate, add, subtract, multiply, divide, power, modulo, clamp, between)
config_schema.py           # Typed configuration schema utilities (SchemaField, ConfigSchema, validators)
copy_utils.py              # Copy utilities (shallow/deep copy, dict copy, merge) wrapping stdlib copy module
exceptions_utils.py        # Custom exception classes and error handling utilities
enum_utils.py              # Enum utilities for working with Python enum.Enum classes
io_utils.py                # Line-oriented and atomic input/output utilities
ini_utils.py                 # INI configuration file utilities (load, save, get, set, merge sections)
weakref_utils.py            # Weak reference utilities for managing weak references to objects
argparse_utils.py           # Argument parsing utilities
warnings_utils.py           # Utilities wrapping the standard library warnings module
compression_utils.py       # Compression and decompression utilities (gzip, bz2, zip, tar)
ip_utils.py                # IP address validation and manipulation utilities
regex_utils.py             # Regular expression utilities (compile, match, search, replace, split, escape)
terminal_utils.py          # Terminal output utilities (ANSI color, progress bars, clear screen, prompts)
subprocess_utils.py         # Subprocess utilities (run_command, check_output, check_call)
tests/                     # Python unit tests
  test_async_utils.py         # Tests for async_utils.py
  test_array_utils.py        # Tests for array_utils.py
  test_base64_utils.py        # Tests for base64_utils.py
  test_bisect_utils.py       # Tests for bisect_utils.py
  test_bit_utils.py           # Tests for bit_utils.py
  test_call_once_utils.py     # Tests for call_once_utils.py
  test_bytes_utils.py         # Tests for bytes_utils.py
  test_circuit_breaker_utils.py   # Tests for circuit_breaker_utils.py
  test_cache_utils.py         # Tests for cache_utils.py
  test_memoize_utils.py      # Tests for memoize_utils.py
  test_calculator.py          # Tests for calculator.py
  test_calendar_utils.py      # Tests for calendar_utils.py
  test_cmath_utils.py        # Tests for cmath_utils.py
  test_cli_utils.py           # Tests for cli_utils.py
  test_color_utils.py         # Tests for color_utils.py
  test_collections_utils.py   # Tests for collections_utils.py
  test_compression_utils.py   # Tests for compression_utils.py
  test_config_schema.py       # Tests for config_schema.py
  test_copy_utils.py          # Tests for copy_utils.py
  test_config_utils.py        # Tests for config_utils.py
  test_concurrent_utils.py    # Tests for concurrent_utils.py
  test_context_utils.py       # Tests for context_utils.py
  test_crypto_utils.py        # Tests for crypto_utils.py
  test_csv_utils.py           # Tests for csv_utils.py
  test_data_utils.py          # Tests for data_utils.py
  test_datetime_utils.py      # Tests for datetime_utils.py
  test_decimal_utils.py       # Tests for decimal_utils.py
  test_dict_utils.py          # Tests for dict_utils.py
  test_duration_utils.py      # Tests for duration_utils.py
  test_env_utils.py           # Tests for env_utils.py
  test_exceptions_utils.py    # Tests for exceptions_utils.py
  test_file_utils.py          # Tests for file_utils.py
  test_fractions_utils.py     # Tests for fractions_utils.py
  test_functools_utils.py     # Tests for functools_utils.py
  test_graphlib_utils.py      # Tests for graphlib_utils.py
  test_greeting_utils.py      # Tests for greeting_utils.py
  test_hash_utils.py          # Tests for hash_utils.py
  test_hmac_utils.py          # Tests for hmac_utils.py
  test_heapq_utils.py         # Tests for heapq_utils.py
  test_hello.py               # Tests for hello.py
  test_html_utils.py          # Tests for html_utils.py
  test_http_utils.py          # Tests for http_utils.py
  test_id_utils.py            # Tests for id_utils.py
  test_ini_utils.py           # Tests for ini_utils.py
  test_io_utils.py            # Tests for io_utils.py
  test_ip_utils.py            # Tests for ip_utils.py
  test_itertools_utils.py     # Tests for itertools_utils.py
  test_json_utils.py          # Tests for json_utils.py
  test_list_utils.py          # Tests for list_utils.py
  test_locale_utils.py        # Tests for locale_utils.py
  test_logging_utils.py       # Tests for logging_utils.py
  test_markdown_utils.py      # Tests for markdown_utils.py
  test_math_utils.py          # Tests for math_utils.py
  test_networking_utils.py    # Tests for networking_utils.py
  test_number_utils.py        # Tests for number_utils.py
  test_operator_utils.py      # Tests for operator_utils.py
  test_os_utils.py            # Tests for os_utils.py
  test_path_utils.py          # Tests for path_utils.py
  test_pattern_utils.py       # Tests for pattern_utils.py
  test_prime_utils.py         # Tests for prime_utils.py
  test_priority_queue_utils.py # Tests for priority_queue_utils.py
  test_prompt_utils.py        # Tests for prompt_utils.py
  test_queue_utils.py         # Tests for queue_utils.py
  test_random_utils.py        # Tests for random_utils.py
  test_rate_limiter_utils.py  # Tests for rate_limiter_utils.py
  test_regex_utils.py         # Tests for regex_utils.py
test_retry_utils.py         # Tests for retry_utils.py
test_ring_buffer_utils.py   # Tests for ring_buffer_utils.py
test_scaffold.py            # Tests for scaffold.sh
  test_secrets_utils.py       # Tests for secrets_utils.py
  test_seq_utils.py           # Tests for seq_utils.py
  test_set_utils.py           # Tests for set_utils.py
  test_shapes.py              # Tests for shapes.py
  test_shutil_utils.py        # Tests for shutil_utils.py
  test_socketserver_utils.py     # Tests for socketserver_utils.py
  test_sort_utils.py          # Tests for sort_utils.py
  test_statistics_utils.py    # Tests for statistics_utils.py
  test_stats.py               # Tests for stats.py
  test_string_utils.py        # Tests for string_utils.py
  test_strings.py             # Tests for strings.py
  test_struct_utils.py        # Tests for struct_utils.py
  test_subprocess_utils.py    # Tests for subprocess_utils.py
  test_sys_utils.py           # Tests for sys_utils.py
  test_threading_utils.py     # Tests for threading_utils.py
  test_template_utils.py      # Tests for template_utils.py
  test_terminal_utils.py      # Tests for terminal_utils.py
  test_temp_utils.py          # Tests for temp_utils.py
  test_textwrap_utils.py      # Tests for textwrap_utils.py
  test_time_utils.py          # Tests for time_utils.py
  test_timezone_utils.py      # Tests for timezone_utils.py
  test_timing_utils.py        # Tests for timing_utils.py
  test_tree_utils.py          # Tests for tree_utils.py
  test_type_utils.py          # Tests for type_utils.py
  test_url_utils.py           # Tests for url_utils.py
  test_utils.py               # Tests for utils.py
  test_uuid_utils.py          # Tests for uuid_utils.py
  test_validation_utils.py    # Tests for validation_utils.py
  test_version_utils.py       # Tests for version_utils.py
  test_semver_utils.py        # Tests for semver_utils.py
  test_interval_utils.py      # Tests for interval_utils.py
  test_weakref_utils.py       # Tests for weakref_utils.py
  test_warnings_utils.py      # Tests for warnings_utils.py
  test_xml_utils.py           # Tests for xml_utils.py
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

## Locale Utilities Module

The project includes a locale utility functions module in `locale_utils.py` with helpers for working with locale identifiers and language tags: `normalize_locale` normalizes a locale string to `language_REGION` form, `language_code` extracts the language code, `region_code` extracts the region code, and `is_valid_locale` checks whether a string looks like a valid locale identifier. All functions validate their inputs and raise `TypeError` on invalid arguments. The module is tested in `tests/test_locale_utils.py`.

## Environment Utilities Module

The project includes an environment variable utilities module in `env_utils.py` with functions for reading, writing, and parsing environment variables: `get_env`, `get_env_required`, `get_env_int`, `get_env_float`, `get_env_bool`, `set_env`, `ensure_env`, `unset_env`, and `prefix_env`. Typed accessors parse values as `int`, `float`, and `bool`, with required-variable and default fallbacks. The module is tested in `tests/test_env_utils.py`.

## Logging Utilities Module

The project includes a logging utilities module in `logging_utils.py` with helpers for logging configuration and function-call tracing: `get_logger` returns a named logger (or the root logger), `configure_logging` configures the root logger with a consistent format, handlers, and level, and `log_calls` is a decorator factory that logs function entry and return values using `functools.wraps` to preserve metadata. The module is tested in `tests/test_logging_utils.py`.

## Cache Utilities Module

The project includes a caching utilities module in `cache_utils.py` with helpers for memoizing function results: `memoize` is a decorator factory that caches return values keyed by call arguments (with optional `maxsize` LRU eviction and `typed` argument distinction), `clear_cache` invalidates the cache of a memoized function, and `cache_info` returns a dictionary with `hits`, `misses`, `maxsize`, and `currsize` statistics. Decorated functions also expose `clear_cache` and `cache_info` attributes for direct introspection. The module is tested in `tests/test_cache_utils.py`.

## Memoization Utilities Module

The project includes a lightweight memoization utilities module in `memoize_utils.py` providing a single `memoize` decorator that caches a function's return values keyed by its positional and keyword arguments. Unlike `cache_utils.memoize`, this decorator takes the function directly (not as a factory) and exposes a `cache_clear` method on the wrapped callable to empty the cache. It validates that its argument is callable and raises `TypeError` otherwise. The module is tested in `tests/test_memoize_utils.py`.

## Timing Utilities Module

The project includes a performance measurement utilities module in `timing_utils.py` with helpers for measuring and benchmarking code execution: `timer` is a context manager for timing code blocks, `elapsed_time` calculates elapsed time since a start time, and `benchmark` is a decorator that runs a function multiple times and reports average execution time. The module is tested in `tests/test_timing_utils.py`.

## Concurrent Utilities Module

The project includes a concurrent execution utilities module in `concurrent_utils.py` with helpers for parallel and asynchronous processing: `ThreadPool` and `ProcessPool` context manager wrappers around the standard library executors, `gather` for running awaitables concurrently, `run_async` for running async coroutines from synchronous code, and `to_async` for converting synchronous functions to async. The module is tested in `tests/test_concurrent_utils.py`.

## Priority Queue Utilities Module

The project includes a priority queue utilities module in `priority_queue_utils.py` with a heap-based `PriorityQueue` implementation and helper functions. The queue uses a min-heap with an incrementing counter to preserve insertion order for equal priorities. It provides `push`, `pop`, `peek`, `is_empty`, `size`, `clear`, and convenience functions like `create_priority_queue` and `merge_queues`. The module is tested in `tests/test_priority_queue_utils.py`.

## Queue Utilities Module

The project includes a queue utilities module in `queue_utils.py` providing a simple FIFO `Queue` class backed by `collections.deque` along with module-level helper functions. The `Queue` class supports `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `clear`, `to_list`, and `from_list`, with `IndexError` raised on dequeue or peek from an empty queue. Module-level functions `create`, `enqueue`, `dequeue`, `peek`, `is_empty`, and `size` provide functional-style wrappers. The module is tested in `tests/test_queue_utils.py`.

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

## Enum Utilities Module

The project includes enum utilities in `enum_utils.py` for working with Python `enum.Enum` classes: `enum_to_dict` converts an enum class to a name-to-value dictionary, `get_enum_member` looks up a member by name or value, `is_enum_member` checks whether a value matches a member, `list_enum_members` returns all members in declaration order, `enum_value_from_name` returns a member's value by name, and `enum_name_from_value` returns a member's name by value. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_enum_utils.py`.

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

## HMAC Utilities Module

The project includes HMAC-based message authentication utilities in `hmac_utils.py` for computing HMAC signatures (MD5, SHA1, SHA256, SHA512) with constant-time signature verification: `hmac_md5`, `hmac_sha1`, `hmac_sha256`, `hmac_sha512`, `hmac_new`, `sign`, `verify`, and `compare_digest`. The module is tested in `tests/test_hmac_utils.py`.

## INI Configuration Utilities Module

The project includes an INI configuration utilities module in `ini_utils.py` for working with INI-style configuration files: `load_config`, `save_config`, `get_config_value`, `set_config_value`, `merge_configs`, `list_sections`, `has_section`, and `get_section`. Section-based access uses dot notation (``section.key``), keys preserve their case, and parent directories are created automatically on save. The module is tested in `tests/test_ini_utils.py`.

## HTML Utilities Module

The project includes HTML utility functions in `html_utils.py` for escaping, unescaping, and sanitizing HTML content: `escape_html` escapes special characters (`&`, `<`, `>`, `"`, `'`) for safe insertion into HTML documents, `unescape_html` decodes named and numeric HTML entities back to their original characters, `strip_tags` removes all HTML tags leaving only text content, and `escape_attribute` escapes values for safe use inside HTML attributes. All functions validate their inputs and raise `TypeError` for non-string arguments. The module is tested in `tests/test_html_utils.py`.

## Bytes Utilities Module

The project includes bytes and binary utilities in `bytes_utils.py` for working with raw bytes: `to_hex` returns the hexadecimal representation of bytes, `from_hex` decodes a hex string back into bytes, `xor` XORs data with a repeating key, and `chunk` splits bytes into fixed-size chunks. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_bytes_utils.py`.

## Itertools Utilities Module

The project includes iteration helpers in `itertools_utils.py` wrapping the standard library `itertools` module with input validation: `chain_iterables`, `flatten_once`, `take_while_pred`, `chunk_iterable`, `product_of`, `combinations_of`, and more. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_itertools_utils.py`.

## Base64 Utilities Module

The project includes Base64 and hexadecimal encoding/decoding utilities in `base64_utils.py`: `base64_encode` and `base64_decode` for standard and URL-safe Base64, `base64_encode_bytes` and `base64_decode_bytes` for raw bytes, `hex_encode` and `hex_decode` for hexadecimal, and `is_valid_base64` / `is_valid_hex` for validation. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_base64_utils.py`.

## Bisect Utilities Module

The project includes bisect utility functions in `bisect_utils.py` for binary search on sorted sequences, wrapping the standard library `bisect` module: `bisect_left` and `bisect_right` return the insertion point to the left or right of existing entries, `insort_left` and `insort_right` insert elements while maintaining sort order, and `find_leftmost` / `find_rightmost` return the index of the first or last occurrence of a value (or `None` when absent). All functions accept an optional `lo`/`hi` range and validate their inputs. The module is tested in `tests/test_bisect_utils.py`.

## Binary Struct Utilities Module

The project includes binary struct packing and unpacking utilities in `struct_utils.py` wrapping the standard library `struct` module: `pack` and `unpack` convert between values and bytes, `pack_into` and `unpack_from` read/write at a buffer offset, `calcsize` reports the byte size of a format string, and `is_valid_format` validates a format string. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid input. The module is tested in `tests/test_struct_utils.py`.

## HTTP Status Codes and Response Handling Module

The project includes HTTP utility functions in `http_utils.py` for working with HTTP status codes and response handling: `STATUS_CODES` is a mapping of standard HTTP status codes to their reason phrases, `status_code_category` returns the leading digit (1-5) of a status code, `status_message` returns the standard reason phrase or `None` for unknown codes, and the `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, and `is_error` predicates classify a status code into its response category. The module is tested in `tests/test_http_utils.py`.

## Time Duration Utilities Module

The project includes time duration utilities in `duration_utils.py` for parsing, formatting, and converting time durations: `parse_duration` parses human-readable duration strings (e.g. `"1h30m"`, `"90s"`, `"2.5 days"`) into total seconds, `format_duration` renders seconds as a compact human-readable string, `seconds_to_hms` and `hms_to_seconds` convert between seconds and `(hours, minutes, seconds)`, `to_seconds` combines time components into seconds, `duration_between` computes the `timedelta` between two datetimes, and `add_duration` adds a parsed duration to a datetime. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_duration_utils.py`.

## Temporary File and Directory Utilities Module

The project includes temporary file and directory utilities in `temp_utils.py` for creating, writing, reading, and cleaning up temporary filesystem resources: `create_temp_file` and `create_temp_dir` create named temp files/directories, `temp_file` and `temp_dir` are context managers that remove resources on exit, `write_temp_file` and `read_temp_file` read/write temp file contents, `cleanup_temp_path` removes a temp file or directory, `is_temp_path` checks whether a path lives under the system temp directory, and `temp_path_exists` reports whether a path exists. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_temp_utils.py`.

## XML Parsing and Generation Utilities Module

The project includes XML parsing and generation utilities in `xml_utils.py` for parsing XML documents and strings, building XML elements, converting between elements and dictionaries, querying with XPath, and serializing elements back to strings using the standard library `xml.etree.ElementTree` module: `parse_xml`, `parse_xml_string`, `build_xml`, `add_child`, `set_attribute`, `get_attribute`, `element_to_dict`, `dict_to_element`, `find_elements`, `find_element`, `get_element_text`, `set_element_text`, `xml_to_string`, and `validate_well_formed`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_xml_utils.py`.

## Sequence Utilities Module

The project includes sequence utilities in `seq_utils.py` for common sequence operations: `first`, `last`, and `nth` retrieve elements by position (returning `None` when absent or out of range); `head` and `tail` return leading or trailing elements; `split_at` divides a sequence at an index; `take_while` and `drop_while` consume elements based on a predicate; `interleave` round-robins elements from multiple sequences; `adjacent_pairs` forms consecutive pairs; and `is_sorted` checks ascending or descending order with an optional key. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_seq_utils.py`.

## Number Utilities Module

The project includes number utility functions in `number_utils.py` for common numeric operations: `clamp` restricts a value to a closed interval, `round_to` rounds a value to a given number of decimal places, `is_integer` tests whether a value is integral, `format_number` formats a number with thousands separators and fixed decimals, and `percentage` returns a part as a percentage of a total formatted as a string. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_number_utils.py`.

## Operating System Utilities Module

The project includes operating system utilities in `os_utils.py` for inspecting the platform and environment: `get_platform_info` returns system/release/version/machine/processor/Python details, `get_cpu_count` reports the available CPU count, `get_disk_usage` reports total/used/free/percent disk usage, `get_user_home` and `get_username` return the current user's home and login name, `find_executable` locates an executable on ``PATH``, `expand_path` expands ``~`` and environment variables to an absolute path, and `is_executable` checks whether a path exists and is executable. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_os_utils.py`.

## Sorting Utilities Module

The project includes sorting utility functions in `sort_utils.py` for sorting and ordering operations: `is_sorted` checks whether a sequence is sorted, `bubble_sort` and `merge_sort` return new sorted lists, `nth_largest` returns the n-th largest element (1-based), and `top_n` returns the top n items sorted by key. All functions accept an optional `key` and `reverse` argument. The module is tested in `tests/test_sort_utils.py`.

## Graph and Dependency Resolution Utilities Module

The project includes graph and dependency resolution utilities in `graphlib_utils.py` for topological sorting and cycle detection of directed graphs using the standard library `graphlib` module: `topological_sort` returns nodes in dependency order, `has_cycle` detects cycles, `dependency_order` orders items by their dependencies, and `is_valid_ordering` validates a candidate ordering. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_graphlib_utils.py`.

## Version Utilities Module

The project includes version utility functions in `version_utils.py` for parsing, comparing, and normalizing dotted version strings: `parse_version` parses a dotted version string into a tuple of integers, `compare_versions` compares two version strings returning -1/0/1, `is_greater` returns whether one version is greater than another, and `normalize_version` pads or truncates a version to a fixed component count. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_version_utils.py`.

## Text Wrapping Utilities Module

The project includes text wrapping utility functions in `textwrap_utils.py` for wrapping, shortening, dedenting, indenting, and filling text using the standard library `textwrap` module: `wrap_text`, `shorten_text`, `dedent_text`, `indent_text`, and `fill_text`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_textwrap_utils.py`.

## Prime Number Utilities Module

The project includes prime number utilities in `prime_utils.py` for prime-related operations: `prime_factors` returns the prime factors of an integer, `nth_prime` returns the nth prime (1-indexed), `primes_up_to` returns all primes up to a limit, `next_prime` finds the next prime after a given number, and `previous_prime` finds the previous prime before a given number. The module builds on `math_utils.is_prime` and validates its inputs. The module is tested in `tests/test_prime_utils.py`.

## Decimal Utilities Module

The project includes decimal arithmetic utilities in `decimal_utils.py` for precise decimal number operations using the standard library `decimal` module: `to_decimal`, `add`, `subtract`, `multiply`, `divide`, `power`, `quantize`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, and `is_zero`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_decimal_utils.py`.


## Difflib Utilities Module

The project includes difflib utility functions in `difflib_utils.py` for sequence comparison and diffing using the standard library `difflib` module: `get_close_matches` finds close matches for a word, `ratio` returns the similarity ratio between two strings, `unified_diff` and `context_diff` produce unified/context diffs between sequences of lines, and `ndiff` produces a human-readable delta. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_difflib_utils.py`.


## Heap Queue Utilities Module

The project includes heap queue utilities in `heapq_utils.py` wrapping the standard library `heapq` module: `heapify`, `heappush`, `heappop`, `heapreplace`, `heappushpop`, `merge`, `nlargest`, and `nsmallest`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_heapq_utils.py`.

## Operator Utilities Module

The project includes operator utilities in `operator_utils.py` for common functional operations: `identity`, `negate`, arithmetic operators `add`, `subtract`, `multiply`, `divide`, `power`, and `modulo`, plus `clamp` to bound a value to a range and `between` to test membership in an interval (inclusive by default). All functions are generic over their arguments. The module is tested in `tests/test_operator_utils.py`.

## System Utilities Module

The project includes Python runtime and system information utilities in `sys_utils.py` for inspecting the interpreter and runtime environment: `get_python_version` returns the version as a dictionary, `get_python_version_string` returns the full version string, `get_executable` returns the interpreter path, `get_argv` returns command-line arguments, `get_platform` returns the platform identifier, `get_path` returns the module search path, `get_recursion_limit`/`set_recursion_limit` read and set the recursion limit, `get_stdout_encoding`/`get_stderr_encoding`/`get_stdin_encoding` report stream encodings, `is_interactive` detects interactive sessions, `get_frame_info` inspects a stack frame, and `get_refcount` returns an object's reference count. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_sys_utils.py`.

## Context Utilities Module

The project includes context manager utilities in `context_utils.py` for temporarily altering the runtime environment and restoring it on exit: `chdir` changes the current working directory, `temp_environ` updates environment variables (optionally clearing the rest), `redirect_stdout` and `redirect_stderr` redirect the standard streams, and `suppress` swallows listed exceptions. All context managers restore the previous state even when an exception is raised within the context. The module is tested in `tests/test_context_utils.py`.

## Networking Utilities Module

The project includes networking utilities in `networking_utils.py` for TCP port and host operations: `is_valid_port` validates port numbers (1-65535), `is_port_open` checks whether a TCP port is reachable on a host, `find_free_port` returns an unused local TCP port, `resolve_hostname` resolves a hostname to its IPv4 address, `get_local_ip` returns the local machine's IPv4 address, and `tcp_ping` measures TCP connection latency. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_networking_utils.py`.

## Markdown Utilities Module

The project includes Markdown utility functions in `markdown_utils.py` for working with Markdown text: `extract_code_blocks` extracts fenced code blocks (``` ... ```), `strip_markdown` removes common Markdown formatting while keeping readable text, `count_words` counts whitespace-delimited words, `is_heading` detects Markdown headings, and `heading_level` returns the heading level (1-6) or 0 if not a heading. All functions validate their inputs and raise `TypeError` for non-string arguments. The module is tested in `tests/test_markdown_utils.py`.

## Time Utilities Module

The project includes time utility functions in `time_utils.py` for working with timestamps and durations: `now_epoch` returns the current Unix timestamp in seconds, `now_iso` returns the current UTC time as an ISO 8601 string, `epoch_to_iso` converts a Unix timestamp to an ISO 8601 UTC string, and `iso_to_epoch` parses an ISO 8601 string into a Unix timestamp (returning `None` for invalid input). The module is tested in `tests/test_time_utils.py`.

## Timezone Utilities Module

The project includes time zone utilities in `timezone_utils.py` for working with IANA time zones using the standard library `zoneinfo` module: `get_timezone` looks up a `ZoneInfo` by name, `is_valid_timezone` validates an identifier, `get_utc_now` returns the current UTC time, `get_local_timezone` returns the system local zone, `convert_datetime` converts datetimes between zones, `format_datetime` renders a datetime for a zone, `utc_offset` reports the UTC offset, `is_dst` reports daylight saving time status, and `get_common_timezones` / `get_all_timezones` list zone identifiers. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_timezone_utils.py`.

## Template Utilities Module

The project includes string template utilities in `template_utils.py` for rendering and substituting variables in template strings: `render_template` renders a template using `str.format()` style placeholders, `substitute` renders a template using `string.Template` style placeholders, `safe_substitute` renders a template without raising on missing placeholders, `render_from_dict` renders a template from a mapping of variables, `has_placeholders` checks whether a template contains any placeholders, and `extract_placeholders` returns the placeholder names found in a template. The module supports both `str.format()` style and `string.Template` style placeholders and is tested in `tests/test_template_utils.py`.

## Fractions Utilities Module

The project includes fraction arithmetic utilities in `fractions_utils.py` for exact rational number operations using the standard library `fractions` module: `to_fraction`, `add`, `subtract`, `multiply`, `divide`, `power`, `compare`, `abs_value`, `negate`, `is_positive`, `is_negative`, `is_zero`, `is_integer`, `numerator`, `denominator`, `to_float`, and `from_float`. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_fractions_utils.py`.

## Identifier Utilities Module

The project includes identifier generation and validation utilities in `id_utils.py` for creating short, URL-safe random identifiers: `generate_id` returns a random alphanumeric string of a given length, `new_id` returns a default 8-character identifier, and `is_valid_id` checks whether a string is a valid identifier of a given length. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_id_utils.py`.

## Inspect Utilities Module

The project includes callable and object introspection utilities in `inspect_utils.py` for working with Python callables using the standard library `inspect` module: `get_callable_name` returns the name of a callable or the class name of a callable instance, `is_callable` tests whether an object can be called, `is_async_callable` detects coroutine functions, `get_signature` returns an `inspect.Signature`, `get_parameter_names` and `get_parameter_kinds` describe a callable's parameters, `count_parameters` returns the parameter count, `has_parameter` checks for a named parameter, `bind_arguments` binds positional and keyword arguments with defaults applied, `is_builtin` detects built-in functions, and `get_source_file`/`get_source_lines` locate a callable's source. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_inspect_utils.py`.

## Call Once Utilities Module

The project includes call-once execution utilities in `call_once_utils.py` for ensuring a function runs only a single time: `call_once` decorates a function so its first invocation is cached and all subsequent calls return the cached result without re-invoking the wrapped function. Execution is thread-safe and the returned wrapper exposes a `reset` method to clear the cached state. The module is tested in `tests/test_call_once_utils.py`.

## Circuit Breaker Utilities Module

The project includes circuit breaker utilities in `circuit_breaker_utils.py` implementing the circuit breaker resilience pattern: `CircuitBreaker` wraps an operation and short-circuits calls once a configurable failure threshold is reached, cycling through `CLOSED`, `OPEN`, and `HALF_OPEN` states with thread-safe transitions.     `CircuitBreaker.call` executes a callable through the breaker, `can_execute` reports whether a call would be allowed, and `reset` returns the circuit to the closed state. A `CircuitOpenError` is raised when the circuit rejects a call. The module is tested in `tests/test_circuit_breaker_utils.py`.

## Deprecation Utilities Module

The project includes deprecation utilities in `deprecation_utils.py` for marking APIs as deprecated: `deprecated` decorates a callable so every invocation emits a `DeprecationWarning` describing the deprecation. An optional `version` records when the deprecation was introduced, an optional `replacement` names the suggested alternative, and an optional `message` overrides the default warning text. The wrapped callable forwards all arguments and return values and preserves its metadata via `functools.wraps`. The module is tested in `tests/test_deprecation_utils.py`.

## Ring Buffer Utilities Module

The project includes fixed-size circular (ring) buffer utilities in `ring_buffer_utils.py`: `RingBuffer` is a bounded buffer that overwrites the oldest element when full, with `append`, `get`, `peek`, `pop`, `clear`, `to_list`, `from_list`, plus `capacity`, `is_full`, and `is_empty` properties. Module-level helpers `create`, `append`, `get`, `pop`, `peek`, `is_empty`, `is_full`, `size`, `clear`, and `to_list` are also provided. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_ring_buffer_utils.py`.

## Copy Utilities Module

The project includes copy utilities in `copy_utils.py` for duplicating Python objects and mappings using the standard library `copy` module: `shallow_copy` returns a shallow copy, `deep_copy` returns a deep copy, `copy_dict` and `deep_copy_dict` return shallow and deep copies of a dictionary, `merge_copy` merges multiple dictionaries into a new one without mutating the inputs, and `is_same_object` performs an identity check. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_copy_utils.py`.

## Warnings Utilities Module

The project includes argument parsing utilities in `argparse_utils.py` wrapping the standard library `argparse` module: `make_parser` creates an `ArgumentParser` with common defaults, `add_flag` adds a boolean store_true flag, `add_option` adds a single-value option, `add_positional` adds a positional argument, `add_subparsers` adds subcommands support, `parse_args` parses arguments, `int_positive` validates positive integers, and `float_range` creates a float range validator. The module is tested in `tests/test_argparse_utils.py`.

The project includes warnings utilities in `warnings_utils.py` wrapping the standard library `warnings` module: `warn` emits a warning message with an optional category and stacklevel, `simplefilter` sets the global warning filter action, `catch_warnings` is a context manager that captures warnings emitted within its scope, `filterwarnings` adds a warning filter entry, and `resetwarnings` clears all warning filters. All functions validate their inputs and raise `TypeError` or `ValueError` on invalid arguments. The module is tested in `tests/test_warnings_utils.py`.

## Threading Utilities Module

The project includes threading utilities in `threading_utils.py` wrapping the standard library `threading` module: `create_lock` and `create_rlock` return new lock and reentrant lock objects, `create_semaphore` and `create_bounded_semaphore` return semaphores with a validated initial counter, `create_event` returns an event, `create_condition` returns a condition variable, `create_timer` and `create_thread` build configured timer and thread objects, `current_thread` returns the caller's thread, `active_count` reports the number of alive threads, `enumerate_threads` lists alive threads, and `synchronized` is a decorator that serializes calls using a lock. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_threading_utils.py`.

## Selectors Utilities Module

The project includes selectors utilities in `selectors_utils.py` wrapping the standard library `selectors` module for I/O multiplexing: `create_default_selector` returns a platform-default selector, `register` and `unregister` monitor or stop monitoring file objects for read/write events, `select` waits until registered file objects are ready, `get_key` and `get_map` inspect registrations, and `close_selector` releases resources. Event masks `EVENT_READ` and `EVENT_WRITE` are re-exported. All functions validate their inputs and raise `TypeError` or `ValueError` for invalid arguments. The module is tested in `tests/test_selectors_utils.py`.

## Socketserver Utilities Module

The project includes socketserver utilities in `socketserver_utils.py` wrapping the standard library `socketserver` module for building TCP/UDP servers: `create_tcp_server` and `create_udp_server` create validated server instances, `handle_one_request` processes a single request, `serve_forever` blocks serving requests, `shutdown_server` and `close_server` stop and release a server, and `get_server_address` / `is_serving` inspect bound address and serving state. All functions validate their inputs and raise `TypeError` for invalid arguments. The module is tested in `tests/test_socketserver_utils.py`.
