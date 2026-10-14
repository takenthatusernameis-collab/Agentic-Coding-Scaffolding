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
