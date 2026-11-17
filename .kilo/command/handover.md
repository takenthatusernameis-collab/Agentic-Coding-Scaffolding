---
name: handover
description: Prepare and post the next task for the following agent session
---

# Handover Command

This command prepares a task for the next agent session and posts it to the shared board.

## Usage

```
/handover [task-description]
```

If no task description is provided, a default task will be created based on the current project state.

## Workflow

1. Analyze the current project state and any completed work
2. Identify the next logical task for the project
3. Format the task clearly with specific objectives
4. Post the task to the shared board for the next agent

## Task Format

Tasks should include:
- Clear objective/goal
- Specific deliverables
- Any constraints or requirements
- References to relevant files or documentation

## Example

```
/handover "Add a new utility module for CSV processing with tests and update the pyproject.toml"
```