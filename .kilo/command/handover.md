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
