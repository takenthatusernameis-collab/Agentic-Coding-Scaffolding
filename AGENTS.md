# Agent Instructions

Project: Agentic Coding Scaffolding

## Project Purpose

This repository is a self-evolving scaffolding project for autonomous agentic coding. A GitHub Actions workflow runs a loop of Kilo agent sessions, each receiving the task: "Execute the task assigned by the previous agent and prepare a task for the next agent!"

## Task Handover Protocol

1. Check the shared Kilo board (`board_read`) for any messages from the previous agent
2. If a task is found, execute it
3. If no task is found (bootstrap session), establish the project foundation
4. Post a new task for the next agent via `board_post` to `main`
5. Ensure all work results in committed changes (non-workflow files) for the CI checkpoint

## Workflow Rules

- The CI workflow excludes `.github/workflows/**` from the project progress check
- Only changes to files outside `.github/workflows/` count as "meaningful project progress"
- The workflow auto-commits all non-workflow changes after each session
- Do NOT modify `.github/workflows/` files — they are maintainer-managed

## Coding Conventions

- Write clean, well-documented code
- Follow existing file patterns in the repository
- Use descriptive file and function names
- Keep changes focused and incremental

## Agent Configuration

- Project config: `kilo.json` at the repository root
- Custom subagents: `.kilo/agent/*.md`
- Custom commands: `.kilo/command/*.md`
- Custom skills: `.kilo/skill/*.md`
- Kilo permissions: `permission` key in `kilo.json`

## Available Subagents

- `scaffolder` - A subagent for generating project scaffolding and templates
- `explore` (built-in) - Read-only codebase exploration

## Available Commands

- `scaffold-project` - Scaffold a new project structure
- `handover` - Prepare and post the next task for the following agent

## Developer Commands

Use the following Makefile targets during development:

- `make test` - Run the Python test suite
- `make lint` - Run ruff code style checker
- `make typecheck` - Run mypy static type checking
- `make run` - Run hello.py (`make run NAME=Alice`)
- `make scaffold` - Scaffold a new project using scaffold.sh
- `make pre-commit-install` - Install pre-commit hooks into .git/hooks
- `make pre-commit-run` - Run all pre-commit hooks against tracked files
- `make clean` - Remove build artifacts
- `make help` - Show all available targets

## Notes

- This project uses the `kilo/kilo-auto/free` model
- Sessions have an idle timeout of 900 seconds
- The overall CI job has a 355-minute safety cutoff
- All tests, ruff, and mypy pass as of the latest bootstrap session
