# Project Status

## Project

Agentic Coding Scaffolding — a self-evolving scaffolding project for autonomous agentic coding loops powered by Kilo.

## Current State

The project foundation is established:

- `hello.py` — sample application entry point with tests (`tests/test_hello.py`)
- Stdlib wrapper modules under `<name>_utils.py`, each with corresponding `tests/test_<name>_utils.py`
- `Makefile` with developer targets: `test`, `lint`, `typecheck`, `run`, `scaffold`, `clean`, `help`, `pre-commit-install`, `pre-commit-run`
- `pyproject.toml` — project metadata, pytest/ruff/mypy config, and `py_modules` registration
- `.github/workflows/main.yml` — scheduled Kilo agent loop (maintainer-managed; do not modify)
- `kilo.json` — Kilo configuration with the `scaffolder` subagent
- `.kilo/` — agent, command, and skill definitions
- `.pre-commit-config.yaml` — pre-commit hooks (ruff, mypy, tests, scaffold smoke test)

## Test Suite

- 2240+ tests across all wrapper modules
- `make test` runs the suite via pytest (falling back to unittest)
- All tests pass as of the latest session

## Linting / Type Checking

- `make lint` — ruff (`select = ["E", "F", "I", "W"]`, line-length 100, target py310)
- `make typecheck` — mypy (`strict = false`, python_version 3.10)

## Convention

Each session adds one new stdlib wrapper module (`<module>_utils.py`) with full test coverage, registers it in `pyproject.toml` (`[tool.setuptools] py_modules`), and posts a handover task for the next agent via the Kilo board.
