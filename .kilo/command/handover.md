# Handover Command

## Description
Prepare and post the next task for the following agent in the Kilo agent loop.

## Usage
`/handover [task_description]`

## Instructions
This command helps the current agent prepare a clear, actionable task for the next agent session. The handover should:

1. **Summarize what was accomplished** in this session
2. **Identify the next logical step** based on project priorities
3. **Provide enough context** for the next agent to start immediately
4. **Reference relevant files** that were modified or created

### Handover Template
```
## Session Summary
- **Completed:** [What was done this session]
- **Files Modified:** [List of changed files]
- **Tests Passed:** [Yes/No and any relevant details]

## Next Task
**Objective:** [Clear, specific goal for the next agent]
**Context:** [Why this task matters and how it fits the project]
**Starting Points:** [Files to examine, commands to run]
**Acceptance Criteria:** [How to verify the task is complete]
```

### Posting the Handover
After preparing the handover, use `board_post` to send it to the `main` participant:
```python
board_post(to="main", type="INFO", body=handover_text)
```

### Important Notes
- Do NOT modify `.github/workflows/` files — they are maintainer-managed
- Only changes outside `.github/workflows/` count as meaningful progress
- The CI workflow auto-commits all non-workflow changes after each session
- Ensure the handover is specific and actionable, not vague