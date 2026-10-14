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
#
set -euo pipefail

usage() {
    cat <<EOF
Usage: $0 <project-name> [output-dir]

Arguments:
  project-name   Name for the new project (used in README, etc.)
  output-dir     Destination directory (default: ./<project-name>)

Examples:
  $0 my-new-project
  $0 "My Project" /tmp/projects/my-project
EOF
    exit 1
}

if [[ $# -lt 1 ]]; then
    usage
fi

PROJECT_NAME="$1"
OUTPUT_DIR="${2:-./${PROJECT_NAME}}"

# Normalize project name for use as a directory identifier
PROJECT_ID=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr -s ' ' '-' | tr -cd 'a-z0-9-')

if [[ -z "$PROJECT_ID" ]]; then
    echo "Error: Could not normalize project name '$PROJECT_NAME' to a valid identifier." >&2
    exit 1
fi

if [[ -d "$OUTPUT_DIR" ]]; then
    echo "Warning: Output directory '$OUTPUT_DIR' already exists." >&2
    echo "Existing files will not be overwritten, but new files will be created." >&2
fi

mkdir -p "$OUTPUT_DIR"/{.github/workflows,.kilo/agent}

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

# --- AGENTS.md ---
cat > "$OUTPUT_DIR/AGENTS.md" <<AGENTS
# Agent Instructions

Project: ${PROJECT_NAME}

## Project Purpose

${PROJECT_NAME} is an autonomous agentic coding project powered by Kilo. A GitHub Actions workflow runs a loop of Kilo agent sessions, each receiving the task: "Execute the task assigned by the previous agent and prepare a task for the next agent!"

## Task Handover Protocol

1. Check the shared Kilo board (\`board_read\`) for any messages from the previous agent
2. If a task is found, execute it
3. If no task is found (bootstrap session), establish the project foundation
4. Post a new task for the next agent via \`board_post\` to \`main\`
5. Ensure all work results in committed changes (non-workflow files) for the CI checkpoint

## Workflow Rules

- The CI workflow excludes \`.github/workflows/**\` from the project progress check
- Only changes to files outside \`.github/workflows/\` count as "meaningful project progress"
- Do NOT modify \`.github/workflows/\` files unless you are bootstrapping

## Coding Conventions

- Write clean, well-documented code
- Follow existing file patterns in the repository
- Use descriptive file and function names
- Keep changes focused and incremental

## Notes

- This project uses the \`kilo/kilo-auto/free\` model
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
AGENTS.md                    # AI agent instructions
kilo.json                    # Kilo project configuration
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
echo "Next steps:"
echo "  cd $OUTPUT_DIR"
echo "  git init"
echo "  git add -A"
echo "  git commit -m \"Initial commit\""
