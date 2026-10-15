# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Ruff lint and format configuration in `pyproject.toml` (`[tool.ruff]` and `[tool.ruff.lint]` sections)
- `.pre-commit-config.yaml` with hooks for ruff, mypy, unittest, end-of-file-fixer, trailing-whitespace, and scaffold.sh smoke testing
- `pre-commit-install` and `pre-commit-run` Makefile targets
- `CHANGELOG.md` to track project evolution across agent sessions
- `calculator.py` — simple calculator module with add, subtract, multiply, and divide functions
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `shapes.py` — geometry utilities for calculating areas and perimeters of circles, rectangles, and triangles
- `tests/test_shapes.py` — unit tests for `shapes.py`

### Fixed

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
- `.kilo/agent/scaffolder.md` — scaffolder subagent definition
- `.kilo/command/handover.md` — handover command documentation
- `.kilo/command/scaffold-project.md` — scaffold-project command documentation
- `.kilo/skill/scaffolding-helper.md` — sample skill definition
- `.github/workflows/main.yml` — CI workflow for Kilo agent loop
- `README.md` — project overview and getting started guide
