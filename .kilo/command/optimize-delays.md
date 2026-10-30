---
description: Find and remove the highest-leverage avoidable delay bottleneck without weakening repository guarantees
---

# Delay bottleneck elimination

Execute this pass against the current repository only. Read AGENTS.md, the durable handoff, the active task, and any relevant workflow/permission constraints first.

## 1. Establish the state delta
- Inspect git status --short, recent commits, active board task, durable checkpoint, and available test/build/data status.
- Reuse the last verified evidence. Do not re-run full discovery, full test suites, provider probes, or expensive jobs if relevant inputs and state are unchanged.
- Name the currently blocked task and quantify its wait/recurrence where evidence exists.

## 2. Classify the wait
Choose exactly one primary class:
- AVOIDABLE_PROCESS_DELAY: redundant polling, sleeps, serial work, repeated setup, unnecessary manual handoffs, duplicate checkpoints, excessive test cadence, unbounded jobs, or repeated no-op cycles.
- EXTERNAL_CONSTRAINT: provider outage/rate limit, missing external data, service restriction, or third-party dependency.
- INTEGRITY_OR_SAFETY_GATE: statistical embargo, holdout isolation, minimum history/sample, source terms, permissions, maintainer-only workflow, security controls, or required user authorization.
- UNKNOWN_DELAY: not enough evidence; instrument first.

Do not label a genuine gate an engineering bottleneck just because it delays completion.

## 3. Improve the execution prompt
Rewrite the proposed task in one iteration using evidence from this repository. The task must:
- start with the shortest high-information diagnostic;
- state the dependency graph and parallelizable work;
- define bounded timeouts/retries, with permanent errors failing fast;
- resume from verified checkpoints and skip completed units;
- use targeted tests after local changes and broad tests at real milestones;
- distinguish required waiting from idle time;
- define measurable before/after acceptance criteria;
- state explicit do-not-bypass gates.

Before executing the revised task, check it against the repository scope and authorization rules. Refine it once more if it contains unnecessary serial steps, repeated probes, ambiguous completion conditions, or forced work quotas.

## 4. Remove one high-leverage delay
Prefer a small durable change: state-delta guard, event-driven wake-up, bounded timeout, task sharding/checkpoint, deduplicated handover, deterministic batching, caching of validated results, or a focused diagnostic/test. Do not make unrelated edits or optimize without measurement.

If blocked by an external gate, do not retry identical requests. Do independent permitted work that does not contaminate a frozen/confirmatory track.

## 5. Verify and preserve guarantees
- Run the smallest relevant verification first.
- Run the full repository gate at a material milestone or after a change affecting shared/core behavior.
- Record exact commands and outputs; never claim unrun tests passed.
- Confirm data/safety/statistical/authorization rules remain intact.
- Measure the avoided wait or reduction in repeated work when possible.

## 6. Handover policy
- Update durable state only when a real change, new evidence, or task transition occurred.
- Do not create timestamp-only commits, duplicate board tasks, or empty cycles.
- Leave one specific next task only if a real next step exists.

## Hard boundaries
Never shorten confirmatory windows, reuse holdouts, lower sample/history requirements, fabricate data, exceed provider limits, bypass source terms, change permissions, touch maintainer-managed workflows, or exceed explicit authorization. When a real gate cannot be shortened, write down its exact release condition and stop polling until a meaningful state change.

Success means less idle time and lower lead time with unchanged or stronger correctness, reproducibility, security, research integrity, and verification quality.
