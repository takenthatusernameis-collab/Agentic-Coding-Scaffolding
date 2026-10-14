#!/usr/bin/env bash
#
# scaffold.sh - Generate a complete agentic coding project template
#
# Usage: ./scaffold.sh <project-name> [output-dir]
#
# Creates a ready-to-use project structure with:
#   - GitHub Actions workflow (Kilo agent loop)
#   - AGENTS.md with project-specific instructions
#   - README.md for the new project
#   - kilo.json configuration
#   - .kilo/agent/scaffolder.md subagent definition
#   - .gitignore
#   - Makefile with common developer targets (test, lint, run, clean, help)
#   - pyproject.toml for Python project configuration and dependencies
#   - hello.py sample application entry point
#   - tests/test_hello.py unit tests for the sample application
#
set -euo pipefail

usage() {
    cat <<EOF
Usage: $0 <project-name> [output-dir] [--no-test]

Arguments:
  project-name   Name for the new project (used in README, etc.)
  output-dir     Destination directory (default: ./<project-name>)
  --no-test      Skip the post-scaffold smoke test (default: run it)

Examples:
  $0 my-new-project
  $0 "My Project" /tmp/projects/my-project
  $0 my-new-project ./out --no-test
EOF
    exit 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
  usage
fi

PROJECT_NAME="$1"

# Normalize project name for use as a directory identifier
PROJECT_ID=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr -s ' ' '-' | tr -cd 'a-z0-9-')

if [[ -z "$PROJECT_ID" ]]; then
    echo "Error: Could not normalize project name '$PROJECT_NAME' to a valid identifier." >&2
    exit 1
fi

OUTPUT_DIR="${2:-./${PROJECT_ID}}"
SMOKE_TEST=1
if [[ "${2:-}" == "--no-test" ]]; then
  SMOKE_TEST=0
fi

if [[ -d "$OUTPUT_DIR" ]]; then
    echo "Warning: Output directory '$OUTPUT_DIR' already exists." >&2
    echo "Existing files will not be overwritten, but new files will be created." >&2
fi

mkdir -p "$OUTPUT_DIR"/{.github/workflows,.kilo/agent,.kilo/command,.kilo/skill,tests}

# --- .github/workflows/main.yml ---
cat > "$OUTPUT_DIR/.github/workflows/main.yml" <<'WORKFLOW'
name: Kilo General Agent Loop

on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:
    inputs:
      agents:
        description: "Maximum sequential Kilo worker sessions for this activation"
        required: false
        default: "1000"
        type: number

permissions:
  contents: write

concurrency:
  group: kilo-repository
  cancel-in-progress: false

jobs:
  kilo:
    runs-on: ubuntu-24.04
    timeout-minutes: 360

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
          persist-credentials: true

      - name: Run general-purpose Kilo agent loop
        id: kilo
        shell: bash
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          KILO_DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
          KILO_INPUT_AGENTS: ${{ inputs.agents || '1000' }}
          KILO_IDLE_TIMEOUT_SECONDS: "900"
        run: |
          set -Eeuo pipefail
          umask 077

          command='Execute the task assigned by the previous agent and prepare a task for the next agent!'

          echo "Starting Kilo agent loop for project: ${KILO_DEFAULT_BRANCH:-<project>}"
          echo "Run prompt: $command"

          # Install the Kilo CLI
          npm install --no-audit --no-fund --prefix "$RUNNER_TEMP/kilo" @kilocode/cli@7.7.1
          export PATH="$RUNNER_TEMP/kilo/node_modules/.bin:$PATH"
          kilo --version

          git config user.name "kilo-autonomous"
          git config user.email "kilo-autonomous@users.noreply.github.com"

          agents="${KILO_INPUT_AGENTS:-1000}"
          if ! [[ "$agents" =~ ^[0-9]+$ ]]; then agents=1000; fi
          (( agents < 1 )) && agents=1
          (( agents > 1000 )) && agents=1000

          for ((agent_index=1; agent_index<=agents; agent_index++)); do
            echo "Starting Kilo session ${agent_index}/${agents}"

            kilo run --model kilo/kilo-auto/free --auto "$command"

            # Commit any non-workflow changes
            git restore --source=HEAD --staged --worktree -- .github/workflows >/dev/null 2>&1 || true
            git add -A -- . ':(exclude).github/workflows/**' ':(exclude).git/**'
            if ! git diff --cached --quiet; then
              git commit -m "chore(kilo): checkpoint agent session"
              git push origin "HEAD:$(git rev-parse --abbrev-ref HEAD)" || true
              echo "Checkpoint committed and pushed."
            fi
          done
WORKFLOW

# --- .gitignore ---
cat > "$OUTPUT_DIR/.gitignore" <<'GITIGNORE'
node_modules/
*.log
.DS_Store
*.sqlite
*.sqlite3
*.db
.env
.env.*
.venv/
venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.tox/
coverage.xml
.coverage
*.pyc
*.pyo
kilo-session-*.log
kilo-progress-*.log
*.tmp
GITIGNORE

# --- Makefile ---
cat > "$OUTPUT_DIR/Makefile" <<MAKEFILE
# Makefile for ${PROJECT_NAME}
# Common developer commands for project management

.PHONY: test lint run scaffold clean help

## Run the Python test suite using pytest (falling back to unittest if pytest is unavailable)
test:
	@echo "Running tests..."
	@if command -v pytest >/dev/null 2>&1; then \\
		pytest tests/ -v; \\
	else \\
		python -m unittest discover tests/ -v; \\
	fi

## Run ruff to check code style and formatting
lint:
	@echo "Running linting..."
	@if command -v ruff >/dev/null 2>&1; then \\
		ruff check .; \\
	else \\
		echo "ruff not installed. Install with: pip install ruff"; \\
		exit 1; \\
	fi

## Run hello.py with an optional name argument (e.g., make run or make run NAME=Alice)
run:
	@echo "Running hello.py..."
	@python hello.py \$(NAME)

## Invoke scaffold.sh to scaffold a new project
scaffold:
	@echo "Running scaffold.sh..."
	@./scaffold.sh

## Remove __pycache__, .pytest_cache, and other build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type f -name "coverage.xml" -delete 2>/dev/null || true

## Print usage information for all available targets
help:
	@echo "Available targets:"
	@echo "  test       Run the Python test suite"
	@echo "  lint       Run ruff code style checker"
	@echo "  run        Run hello.py (usage: make run [NAME=YourName])"
	@echo "  scaffold   Scaffold a new project using scaffold.sh"
	@echo "  clean      Remove build artifacts"
	@echo "  help       Show this help message"
MAKEFILE

# --- pyproject.toml ---
cat > "$OUTPUT_DIR/pyproject.toml" <<PYPROJECT
[project]
name = "${PROJECT_ID}"
version = "0.1.0"
description = "A project scaffolded for autonomous agentic coding with Kilo."
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "kilo-autonomous", email = "kilo-autonomous@users.noreply.github.com" }]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
PYPROJECT

# --- hello.py ---
cat > "$OUTPUT_DIR/hello.py" <<'HELLO'
import sys


def main(name: str = "World") -> None:
    """Print a greeting for the given name.

    Args:
        name: The name to greet. Defaults to "World".
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    cli_name = sys.argv[1] if len(sys.argv) > 1 else "World"
    main(cli_name)
HELLO

# --- tests/test_hello.py ---
cat > "$OUTPUT_DIR/tests/test_hello.py" <<'TESTHELLO'
import io
import unittest
from unittest.mock import patch

from hello import main


class TestHello(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_world(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_alice(self, mock_stdout):
        main("Alice")
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Alice!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_with_custom_name(self, mock_stdout):
        main("Bob")
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Bob!")


if __name__ == '__main__':
    unittest.main()
TESTHELLO

# --- .kilo/command/handover.md ---
cat > "$OUTPUT_DIR/.kilo/command/handover.md" <<'HANDOVER'
---
description: Prepare and post the next task for the following agent
---

Prepare and post the next task for the following agent.

1. Review the current state of the repository.
2. Check the shared Kilo board (`board_read`) for context.
3. Identify what the next agent should work on based on the current repository state and any incomplete tasks.
4. Post a clear, specific task to the board using `board_post` to `main` with type `INFO`.
5. The task should be actionable, focused, and build on work already done or identified gaps.

When you are done, ensure all work results in committed changes (non-workflow files) so the CI checkpoint can verify meaningful project progress.
HANDOVER

# --- .kilo/command/scaffold-project.md ---
cat > "$OUTPUT_DIR/.kilo/command/scaffold-project.md" <<'SCAFFOLD'
---
description: Scaffold a new project structure for agentic coding
---

Generate scaffolding files for a new agentic coding project. This command creates:

- `.github/workflows/main.yml` — CI workflow for the Kilo agent loop
- `AGENTS.md` — AI agent instructions with task handover protocol
- `README.md` — project overview and getting-started guide
- `kilo.json` — Kilo project configuration
- `.kilo/agent/scaffolder.md` — subagent definition for scaffolding tasks
- `.kilo/skill/scaffolding-helper.md` — sample skill definition
- `.gitignore` — common ignore patterns
- `Makefile` — common developer targets
- `pyproject.toml` — Python project configuration
- `hello.py` — sample application
- `tests/test_hello.py` — unit tests

## Usage

```bash
scaffold-project <project-name> [output-dir]
```

## Examples

```bash
scaffold-project "My AI Project"
scaffold-project my-cool-tool /tmp/projects/my-tool
```
SCAFFOLD


# --- .kilo/skill/scaffolding-helper.md ---
cat > "$OUTPUT_DIR/.kilo/skill/scaffolding-helper.md" <<'SKILLSAMPLE'
---
name: scaffolding-helper
description: Helps with project scaffolding tasks and maintaining scaffold templates
---

This is a sample skill for the scaffolding system. Skills provide specialized instructions and workflows for specific tasks.

When using this skill:
1. Follow the established project patterns
2. Maintain consistency across scaffolded files
3. Ensure generated code is well-documented
SKILLSAMPLE

# --- .kilo/.gitignore ---
cat > "$OUTPUT_DIR/.kilo/.gitignore" <<'KILOGITIGNORE'
node_modules
package.json
package-lock.json
pnpm-lock.yaml
bun.lock
yarn.lock
.gitignore
agent-manager.json
KILOGITIGNORE

# --- AGENTS.md ---
cat > "$OUTPUT_DIR/AGENTS.md" <<'AGENTS'
# Agent Instructions

Project: ${PROJECT_NAME}

## Project Purpose

${PROJECT_NAME} is an autonomous agentic coding project powered by Kilo. A GitHub Actions workflow runs a loop of Kilo agent sessions, each receiving the task: "Execute the task assigned by the previous agent and prepare a task for the next agent!"

## Task Handover Protocol

1. Check the shared Kilo board (`board_read`) for any messages from the previous agent
2. If a task is found, execute it
3. If no task is found (bootstrap session), establish the project foundation
4. Post a new task for the next agent via `board_post` to `main`
5. Ensure all work results in committed changes (non-workflow files) for the CI checkpoint

## Workflow Rules

- The CI workflow excludes `.github/workflows/**` from the project progress check
- Only changes to files outside `.github/workflows/` count as "meaningful project progress"
- Do NOT modify `.github/workflows/` files unless you are bootstrapping

## Developer Commands

Use the following Makefile targets during development:

- `make test` — Run the Python test suite
- `make lint` — Run ruff code style checker
- `make run` — Run hello.py (`make run NAME=Alice`)
- `make clean` — Remove build artifacts
- `make help` — Show all available targets

## Agent Configuration

- Project config: `kilo.json` at the repository root
- Custom subagents: `.kilo/agent/*.md`
- Custom commands: `.kilo/command/*.md`
- Kilo permissions: `permission` key in `kilo.json`

## Available Subagents

- `scaffolder` - A subagent for generating project scaffolding and templates
- `explore` (built-in) - Read-only codebase exploration

## Available Commands

- `scaffold-project` - Scaffold a new project structure
- `handover` - Prepare and post the next task for the following agent

## Coding Conventions

- Write clean, well-documented code
- Follow existing file patterns in the repository
- Use descriptive file and function names
- Keep changes focused and incremental

## Notes

- This project uses the `kilo/kilo-auto/free` model
- Sessions have an idle timeout of 900 seconds
- The overall CI job has a 355-minute safety cutoff
AGENTS

# --- README.md ---
cat > "$OUTPUT_DIR/README.md" <<README
# ${PROJECT_NAME}

A project scaffolded for autonomous agentic coding with Kilo.

## Overview

This repository provides a foundation for autonomous agent development. A GitHub Actions workflow runs a loop of Kilo agent sessions that iteratively build and refine the project.

## How It Works

Each agent session runs with the prompt "Execute the task assigned by the previous agent and prepare a task for the next agent!" — creating a continuous, evolving codebase.

## Project Structure

\`\`\`
.github/workflows/main.yml   # CI workflow: Kilo agent loop
.kilo/                       # Kilo project configuration
  agent/                     # Custom subagents
  command/                   # Custom commands
  skill/                     # Custom skills
AGENTS.md                    # AI agent instructions
kilo.json                    # Kilo project configuration
Makefile                     # Common developer targets (test, lint, run, clean, help)
pyproject.toml               # Python project configuration and dependencies
hello.py                     # Sample application entry point
tests/                       # Python unit tests
  test_hello.py              # Tests for hello.py
\`\`\`

## Developer Commands

This project includes a \`Makefile\` with the following targets:

| Target    | Description                              |
|-----------|------------------------------------------|
| \`make test\`    | Run the Python test suite with pytest    |
| \`make lint\`    | Run ruff code style checker              |
| \`make run\`     | Run hello.py (\`make run NAME=Alice\`)   |
| \`make scaffold\`| Run scaffold.sh to scaffold a new project|
| \`make clean\`   | Remove build artifacts                   |
| \`make help\`    | Show all available targets               |

## Getting Started

\`\`\`bash
# Run the sample application
make run

# Run tests
make test

# Check code style
make lint
\`\`\`

## License

MIT
README

# --- kilo.json ---
cat > "$OUTPUT_DIR/kilo.json" <<'KILOJSON'
{
  "$schema": "https://app.kilo.ai/config.json",
  "permission": "allow"
}
KILOJSON

# --- .kilo/agent/scaffolder.md ---
cat > "$OUTPUT_DIR/.kilo/agent/scaffolder.md" <<'AGENT'
---
description: Generates project scaffolding, templates, and boilerplate code
mode: subagent
model: kilo/kilo-auto/free
---

You are a scaffolding specialist subagent. Your purpose is to generate project scaffolding, templates, and boilerplate code.

When invoked:

1. Analyze the requested scaffolding need
2. Generate clean, well-structured files following existing patterns
3. Create a README or notes file explaining what was scaffolded
4. Follow the coding conventions defined in AGENTS.md
AGENT

echo ""
echo "Scaffolded project '$PROJECT_NAME' at: $OUTPUT_DIR"
echo ""
echo "Created files:"
find "$OUTPUT_DIR" -type f | sort | sed "s/^/  /"
echo ""

if [[ "$SMOKE_TEST" == "1" ]] && command -v python >/dev/null 2>&1; then
  echo "Running smoke test in $OUTPUT_DIR ..."
  if (cd "$OUTPUT_DIR" && python -m unittest discover tests/ -v); then
    echo "Smoke test passed."
  else
    echo "Warning: smoke test failed. The scaffold may be incomplete." >&2
  fi
else
  echo "Smoke test skipped (pass --no-test to skip intentionally)."
fi

echo ""
echo "Next steps:"
echo "  cd $OUTPUT_DIR"
echo "  git init"
echo "  git add -A"
echo "  git commit -m \"Initial commit\""
