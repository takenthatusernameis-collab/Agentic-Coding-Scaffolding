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
  command/                   # Custom commands
AGENTS.md                    # AI agent instructions
kilo.json                    # Kilo project configuration
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

## License

MIT
