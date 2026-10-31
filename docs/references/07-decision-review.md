# Decision Review Checklist (DECISION REVIEW)

> A pre-decision questioning tool, complementary to post-decision records (ADR / CHANGELOG).
> For **any project**: before an AI Agent or a human performs an irreversible, paid, outward-facing, or direction-changing action, run through this checklist first.
> This template is de-project-ified and can be copied directly into your own project.

---

## 1. When this flow is mandatory

If any of the following applies, **answer the checklist before acting, then wait for the decider's confirmation**:

| Category | Examples |
|----------|----------|
| Irreversible | delete/overwrite files, delete branches, force-push, rewrite git history, purge data |
| Paid | buy a service, paid API, upgrade subscription, cloud resources, third-party audit |
| Outward-facing | publish a Release, tag, public post, deploy to production, make a repo public |
| Direction-changing | architecture change, tech stack selection, version strategy, remove existing features, data migration |

## 2. The three decision questions (all required)

### 1. What are the downsides / costs?
- What are the disadvantages, costs, and risks of this option?
- What is the impact on existing features, data, performance, and maintenance cost?
- The answerer **must not downplay or only list the benefits**; when pressed, they must fill in the gaps.

### 2. What if we don't do it?
- If we don't do it or delay it, what do we lose?
- Is the loss permanent or reversible? How big?
- If "doing nothing loses nothing," this option may simply be unnecessary.

### 3. Under what conditions would we regret this?
- Which premise, if false, would make this decision wrong?
- How long until we can still reverse it? What is the cost of reversing?
- Is there room to "pilot small first, then decide whether to go all-in"?

## 3. Five layers of follow-up (when the three questions aren't enough)

### Layer 1: Goal & scope
- What problem are we actually solving? (state it in one sentence)
- What is the minimal scope of this change? Can it be smaller?
- Is anything being changed incidentally that isn't related to this goal?

### Layer 2: Irreversibility
- After doing it, can it be undone? How many steps to undo?
- If it fails, what is the worst case? Will data be lost? Will users be affected?
- Is there a way to ship a "rollback-able version" before the official one?

### Layer 3: Alternatives
- List at least one alternative and explain why it isn't used.
- Is there a "simpler / cheaper / faster" approach?
- Is the alternative rejected for a real constraint, or just out of "habit"?

### Layer 4: Time horizon
- Is doing this now vs. a month from now a big difference?
- Are there changing factors (dependencies, platform, policy) that affect this decision?
- How long after completion before it needs review?

### Layer 5: Security & privacy
- Does it involve user data, passwords, or keys? Flag the risk by default.
- Is any sensitive information written into code, logs, or docs?
- Does the code actually implement the capability the docs claim?

## 4. Common "regret scenario" quick reference

| Decision type | Typical regret condition | Reversal cost |
|---------------|--------------------------|---------------|
| Add a new dependency/framework | project later finds it doesn't need that capability | Medium (migration cost) |
| Delete old code / feature | users / data depend on it | High (possibly unrecoverable) |
| Pay for a service | actual usage far below expectations | Low–Medium (per cycle) |
| Release / tag | wrong version semantics, incomplete content | Low (can re-release) |
| Architecture refactor | test regressions, data migration anomalies | High (needs rollback plan) |
| Make public | privacy / compliance issues | Extreme (public = spread) |

## 5. Decision log template

Filled in by the Agent / owner before execution, kept with the PR or commit:

```markdown
## Decision Log

- **Date**: YYYY-MM-DD
- **Decider**: the person who signed off / the suggester (AI or other)
- **What to do**: (one sentence)
- **Trigger category**: □ Irreversible □ Paid □ Outward-facing □ Direction-changing

### Three decision questions
1. Downsides / costs:
2. Consequence of not doing it:
3. Regret condition (when, and reversal cost):

### Alternatives
- Option B: (description)
- Why not B:

### Security / privacy impact
- (state it if any; write "none" if not)

### Conclusion
- □ Do it (confirmed)  □ Don't  □ Pilot first / delay
- Confirmed on: YYYY-MM-DD
```

## 6. Relationship to the rest of the system

- **AGENTS.md**: embeds this checklist's core (the three decision questions, "ask first if irreversible") into rules the AI must follow — loaded automatically when the AI enters the repo.
- **CHANGELOG / decision records (ADR)**: after a decision is made, write down "why we did it" for future review.
- **Doc Sync spec (`references/08-doc-sync.md`)**: after release / changes, keep doc descriptions consistent with code facts.

> One line: **small things just do; big things get the three questions first; after deciding, write it down.**
