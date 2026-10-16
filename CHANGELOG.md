# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]

### Added

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


### Added

- `config_schema.py` — typed configuration schema utilities (`SchemaField`, `ConfigSchema`, validators such as `range_validator`, `choices_validator`, `email_validator`)
- `tests/test_config_schema.py` — unit tests for `config_schema.py`


### Added

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

- `config_utils.py` — configuration utilities module with `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs` functions for working with JSON configuration files
- `tests/test_config_utils.py` — unit tests for `config_utils.py`

### Added

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

- `file_utils.py` — file and path utility functions
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- Updated scaffold template to generate `file_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md` and `README.md` to include file utilities
- Updated `tests/test_scaffold.py` to verify file_utils generation
- Established project foundation by running test suite, lint, typecheck, and posted a task for next agent to scaffold a new project.

### Added

- `logging_utils.py` — logging configuration and helper utilities with `get_logger`, `configure_logging`, and a `log_calls` decorator for tracing function calls
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- Synchronized `scaffold.sh` templates (`scaffold-project.md`, generated `README.md`, generated `CHANGELOG.md`), repo `README.md`, repo `.kilo/command/scaffold-project.md`, and `tests/test_scaffold.py` to include the `logging_utils` module and its tests

### Fixed

- Fixed `scaffold.sh` README.md template Architecture section: added missing `config_utils.py` listing, added all missing test file entries (including `test_config_utils.py`), removed redundant `tests/` placeholder entry, and updated module descriptions to match the canonical README. Verified scaffold smoke test passes with all generated modules.
### Added

- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate/pretty print)
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- Updated `scaffold.sh` to generate `json_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include JSON utilities

### Added

- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`
- Updated `scaffold.sh`, `.kilo/command/scaffold-project.md`, and `README.md` to include CSV utilities

### Added

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

