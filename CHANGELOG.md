# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]

### Added

- `random_utils.py` — random number generation and sampling utilities with `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_uniform`, and `random_gaussian` functions, each accepting an optional `seed` for reproducible results
- `tests/test_random_utils.py` — unit tests for `random_utils.py`
- `validation_utils.py` — input validation module with `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname` functions
- `tests/test_validation_utils.py` — unit tests for `validation_utils.py`
- `crypto_utils.py` — cryptographic utilities with `hash_string`, `generate_token`, `base64_encode`, and `base64_decode` functions
- `tests/test_crypto_utils.py` — unit tests for `crypto_utils.py`

### Fixed

- Fixed inconsistent indentation in README.md project structure section (datetime_utils.py, file_utils.py, url_utils.py entries had extra leading spaces)
- Fixed inconsistent indentation in scaffold.sh README.md template for the same entries
- Removed duplicate `stats.py` heredoc section in `scaffold.sh` (was generated twice)
- Removed unused `import os` from `scaffold.sh`'s `file_utils.py` template (matches repo version)
- Added missing `math_utils.py`, `data_utils.py`, `datetime_utils.py`, and `file_utils.py` entries to `scaffold.sh`'s `scaffold-project.md` command doc template
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

- `stats.py` — statistics utility module with mean, median, mode, variance, and stddev functions
- `tests/test_stats.py` — unit tests for `stats.py`

- Ruff lint and format configuration in `pyproject.toml` (`[tool.ruff]` and `[tool.ruff.lint]` sections)
- `.pre-commit-config.yaml` with hooks for ruff, mypy, unittest, end-of-file-fixer, trailing-whitespace, and scaffold.sh smoke testing
- `pre-commit-install` and `pre-commit-run` Makefile targets
- `CHANGELOG.md` to track project evolution across agent sessions
- `calculator.py` — simple calculator module with add, subtract, multiply, and divide functions
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `shapes.py` — geometry utilities for calculating areas and perimeters of circles, rectangles, and triangles
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `utils.py` — general utility helper functions
- `tests/test_utils.py` — unit tests for `utils.py`

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

- `math_utils.py` — mathematical utility functions (factorial, fibonacci, gcd, lcm, is_prime, clamp)
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- Updated `scaffold.sh` to generate `math_utils.py` and its tests
- Updated scaffold tests to verify math utils generation
- Updated `.kilo/command/scaffold-project.md`, `README.md`, and scaffold template to include math utils
- `data_utils.py` — data utility module with `deep_copy`, `merge_dicts`, `pick`, `omit`, and `flatten_dict` functions
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- Updated scaffold template to generate `data_utils.py` and its tests

### Added
- `file_utils.py` — file and path utility functions
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- Updated scaffold template to generate `file_utils.py` and its tests
- Updated `.kilo/command/scaffold-project.md` and `README.md` to include file utilities
- Updated `tests/test_scaffold.py` to verify file_utils generation

## [0.1.0] - Bootstrap

### Added

- `hello.py` — sample application entry point with CLI argument support
- `tests/test_hello.py` — unit tests for `hello.py`
- `tests/test_scaffold.py` — unit tests for `scaffold.sh`
- `scaffold.sh` — project scaffolding script with project name normalization and smoke testing
- `AGENTS.md` — agent instructions with task handover protocol
- `kilo.json` — Kilo project configuration with scaffolder subagent
- `Makefile` — developer targets (test, lint, typecheck, run, scaffold, clean, help)
- `pyproject.toml` — Python project configuration and dev dependencies
- `.gitignore` — common ignore patterns
- `LICENSE` — MIT license
- `.kilo/agent/scaffolder.md` — scaffolder subagent definition
- `.kilo/command/handover.md` — handover command documentation
- `.kilo/command/scaffold-project.md` — scaffold-project command documentation
- `.kilo/skill/scaffolding-helper.md` — sample skill definition
- `.github/workflows/main.yml` — CI workflow for Kilo agent loop
- `README.md` — project overview and getting started guide
