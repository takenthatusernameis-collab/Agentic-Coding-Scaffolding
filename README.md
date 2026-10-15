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
calculator.py                # Simple calculator module
shapes.py                    # Geometry utilities for areas and perimeters
strings.py                   # String utilities for text operations
utils.py                     # General utility helper functions
stats.py                     # Statistical utility functions
math_utils.py               # Mathematical utility functions
data_utils.py               # Data utility functions
datetime_utils.py           # Date and time utility functions
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
random_utils.py             # Random number generation and sampling utilities
validation_utils.py         # Input validation utilities
crypto_utils.py             # Cryptographic utilities
tests/                       # Python unit tests
  test_hello.py              # Tests for hello.py
  test_calculator.py         # Tests for calculator.py
  test_scaffold.py           # Tests for scaffold.sh
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

## Random Utilities Module

The project includes a random utilities module in `random_utils.py` with functions for random number generation and sampling: `random_int`, `random_choice`, `random_sample`, `random_shuffle`, `weighted_choice`, `random_uniform`, and `random_gaussian`. Every function accepts an optional `seed` argument for reproducible results and validates its inputs. The module is tested in `tests/test_random_utils.py`.

## Validation Utilities Module

The project includes a validation utilities module in `validation_utils.py` with functions for common input validation: `is_email`, `is_numeric`, `is_integer`, `is_alphanumeric`, `is_boolean_string`, `is_none_or_empty`, `min_length`, `max_length`, `matches_regex`, and `is_valid_hostname`. The module is tested in `tests/test_validation_utils.py`.

## Cryptographic Utilities Module

The project includes a cryptographic utilities module in `crypto_utils.py` with functions for hashing and encoding: `hash_string`, `generate_token`, `base64_encode`, and `base64_decode`. The module is tested in `tests/test_crypto_utils.py`.
