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
---
description: Prepare a state-delta-aware task handover without duplicate no-op work
---

Prepare the next task using the durable state and shared Kilo board.

1. Read current task/board messages and inspect recent commits plus git status --short.
2. Compare the current state with the previous verified checkpoint. Identify only unfinished work or material new changes; do not repeat completed verification or rediscover an unchanged blocker.
3. If nothing materially changed and the current task remains blocked on the same external/integrity gate, do not post a duplicate task or make a timestamp-only handoff commit. Leave the existing board task intact and exit cleanly.
4. If progress or a genuine state change occurred, select one highest-value next task with explicit scope, dependencies, bounded commands/timeouts, acceptance criteria, and preserved safety/integrity gates.
5. Post one clear task to the board using board_post to main with type INFO only when it is materially different from the existing active task.
6. Preserve repository rules: do not touch maintainer-managed workflow files; do not commit secrets, caches, or generated clutter; keep genuine work committed for CI checkpointing.

The objective is reliable continuity and lower end-to-end lead time, not more sessions, messages, or commits.
