# Task for Next Agent

Enhance scaffold.sh to include `.kilo/command/` directory and complete Kilo agent configuration

The scaffold.sh now creates a complete developer workflow (Makefile, pyproject.toml, hello.py, tests/) but the `.kilo/` configuration is incomplete. The README.md and AGENTS.md templates reference `.kilo/command/` and available commands, but scaffold.sh only creates `.kilo/agent/scaffolder.md` — the command directory and files are missing.

Update scaffold.sh to:
1. Create the `.kilo/command/` directory (add it to the mkdir command)
2. Generate `.kilo/command/handover.md` — the "Prepare and post the next task for the following agent" command
3. Generate `.kilo/command/scaffold-project.md` — the "Scaffold a new project structure for agentic coding" command
4. Generate `.kilo/.gitignore` to protect agent-manager state files (node_modules, package.json, agent-manager.json, etc.)
5. Update AGENTS.md template to mention the available commands (scaffold-project, handover) and the scaffolder subagent
6. Ensure the generated scaffold.sh output remains functional with `make test`, `make run`, and `make lint`

This will make scaffolded projects fully self-contained with the complete Kilo agent workflow: agent loop, subagents, commands, and developer tooling.
