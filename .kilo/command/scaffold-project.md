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
- `env_utils.py` — environment variable handling utilities
- `logging_utils.py` — logging configuration and helper utilities
- `cache_utils.py` — caching utilities for memoizing function results
- `timing_utils.py` — performance measurement helpers
- `async_utils.py` — asynchronous utility functions
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
- `functools_utils.py` — functional programming utilities (compose, pipe, curry, apply)
- `tests/test_functools_utils.py` — unit tests for `functools_utils.py`
- `config_schema.py` — typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators)
- `tests/test_config_schema.py` — unit tests for `config_schema.py`
- `exceptions_utils.py` — custom exception classes and error handling utilities
- `tests/test_exceptions_utils.py` — unit tests for `exceptions_utils.py`
- `io_utils.py` — line-oriented and atomic input/output utilities (`read_lines`, `write_lines`, `append_text`, `atomic_write_text`, `stream_copy`, `count_lines`, `iter_lines`)
- `compression_utils.py` — compression and decompression utilities (gzip, bz2, zip, tar)
- `ip_utils.py` — IP address validation and manipulation utilities (IPv4/IPv6, conversion, properties, subnet checks)
- `tests/test_io_utils.py` — unit tests for `io_utils.py`
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
- `tests/test_env_utils.py` — unit tests for `env_utils.py`
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- `tests/test_cache_utils.py` — unit tests for `cache_utils.py`
- `tests/test_timing_utils.py` — unit tests for `timing_utils.py`
- `tests/test_async_utils.py` — unit tests for `async_utils.py`
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
- `cli_utils.py` — command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
- `tests/test_cli_utils.py` — unit tests for `cli_utils.py`

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
