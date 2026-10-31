# Prompt Library

> Categorized by **when to use**, not by source. Replace the brackets with your actual situation.
> A opening / B scoping / C delivery / D quality / E security / F rescue / G session / H learning

---

## A. Session opening: set the AI's role

### A1｜Universal role setting (use this when you don't know what else to use)

```
You and I are collaborating on a project. Rules:

[Expression] Lead with the conclusion in plain language; put professional detail after.
The first time a term appears, explain it in parentheses. If unsure, say "unsure" directly.
Never fabricate library names, APIs, version numbers, or config items. When giving options,
state the tradeoff — e.g. "this is fast but harder to extend later" — don't just give a conclusion.

[Opposition mechanism] When my idea has a technical flaw, a logic hole, or a better alternative,
point out the problem first and give at least one alternative; I decide, don't comply silently.

[Code delivery] When giving code, you must say: what this code does, which file and where it goes,
what you changed, and how to run and verify it. Give one runnable minimal version at a time,
don't dump a whole big project at once. When the project errors, first have me describe or paste
the error, explain the cause in plain language, then give fix steps — don't skip diagnosis and rewrite.

[Process] On receiving a request, confirm goal and scope before acting; if key info is missing,
ask all at once, don't guess while building. Break big tasks into small steps, deliver verifiable
results each step. Suggest tech choices with rationale; wait for my call; implement details and
small issues directly without asking for everything. For irreversible operations — deleting files,
overwriting code, paid services, public releases — get my consent first.

[Safety awareness] For code involving user data, passwords, or keys, by default remind me of
security and privacy risks; don't hardcode sensitive info into code.
```

**The two most valuable lines**: one is "never fabricate library names/APIs/versions," the other is "get consent before irreversible operations." The first stops the AI from fabricating things that look real; the second stops it from deleting databases, shipping, or spending money on its own.

### A2｜"I don't get tech" (stack this after A1 when your description is unclear)

```
I'm a non-technical newbie user, and I have a temper, and my descriptions might not be clear.
My requirements aren't professional tech terms; you first need to understand my need,
and turn my instruction into a concrete executable task.
If you can't understand, or my instruction is vague, you can stop anytime and ask to confirm my specific need.
```

**This solves a real pain point**: your needs are often felt ("the UI lacks big-company class"), not technical. This forces the AI to **translate the feeling into a task first**.

---

## B. Scoping: before you start

### B1｜Research first, then code (use before any new project)

```
I'm developing [XXX]. Don't write code yet; first search GitHub for excellent open-source projects
in the same category, analyze their core features, architecture, and existing shortcomings.
Based on the research, output a better landing plan; after I confirm, we start developing.

Core principle: research first, then code. Don't let the AI build from scratch out of nothing;
let it iterate on the shoulders of existing excellent projects.
```

**Value**: the AI defaults to "just write you one," and what it writes is often the first mediocre idea you thought of. Have it look at ten similar projects first; the plan quality is completely different.

### B2｜PRD formula

```
Output a standard product requirements doc, structure:
1. Project overview  2. User goals  3. Core features  4. Interaction rules  5. Constraints

Need: [your product/idea here]

Other requirements:
1. [change to your platform: Web / PWA / mini-program / Android]
2. [backend, database, registration/login or not]
3. Keep only a few core features, as lean as possible
4. Clean and simple pages
```

The 3rd item "keep only a few core features" is worth keeping — **it's the life-or-death line of v1.0.**

---

## C. Execution & delivery

### C1｜Restate acceptance criteria (use before starting)

```
Before acting, first restate in three sentences:
1. What is the goal of this task
2. Which files will you change
3. What "done" looks like — what operation can I use to confirm it's truly done

If you can't state any of these three, the requirement isn't thought through; ask me first.
```

### C2｜Deliver in small steps (use for big tasks)

```
This task is fairly large. Break it into small steps that can each be verified; each step:
- Runs and shows results on its own
- Reports immediately after: which file changed, old value → new value, what you actually ran to verify
- Don't proceed to the next step until I confirm

Don't hoard one giant change and hand it to me all at once.
```

### C3｜Self-check before done (use at wrap-up, anti "fake done")

```
Before declaring the task done, self-check against the goal:
1. Check actual changes against requirement items
2. View changed files and diffs; confirm no unrelated changes
3. Prioritize running the project's existing tests / lint / type-check / build relevant to this change
4. If this change caused a check to fail, locate, fix, then re-verify; if pre-existing or unrelated, tell me clearly
5. When there's no runnable way to verify, don't claim "done"; tell me directly what's unverified, why, and the risk

Finally report in a short checklist: what's done, verification evidence, remaining risk.
```

**The AI loves to say "done" but actually didn't run tests or changed unrelated files. Paste this every wrap-up.**

### C4｜Honest reporting format

```
Report this change in this format:

What changed: [file path] + old value → new value (write "new" for added files, "deleted" for removed ones)
Actual verification: which command ran, what the output was
Not yet confirmed: [list honestly]

Ban empty words like "changed" "optimized" "fixed." Never say "tests passed" for a verification you didn't actually run.
```

---

## D. Quality & design

### D1｜Design self-check (after finishing the UI)

```
Using Awwwards, Webby Awards, FWA award-winning sites as the quality bar,
after finishing, self-check from these eight dimensions and keep optimizing until no obvious improvement remains:
typography, whitespace, visual hierarchy, color, motion, micro-interaction, responsiveness, originality.
```

Pair with this (make it give options before changing):
```
First score each dimension (1-10) and say where points were deducted; after I confirm priority, then change.
Don't change everything at once; show me the effect after one round.
```

### D2｜Comprehensive code review (periodic big cleanup)

```
Please do a highly deep, comprehensive code review covering:
1. Code quality  2. Test coverage & quality  3. UI/UX interaction
4. Code conventions  5. Docs vs code sync + doc quality
6. Security (including server-side)

Output format: graded by severity (fatal / serious / general / suggestion),
each with: location, problem, why it's a problem, fix.
For dimensions where you find nothing, say "found nothing" explicitly; don't fabricate to fill quota.
```

**⚠️ Don't run it all at once.** One pass on a big project yields hundreds of items you can't handle,
and it ends up an unread list. **Recommend reviewing one dimension at a time.**

---

## E. Security

### E1｜Attack yourself before shipping

```
Before shipping, play an attacker and find this project's problems:
1. What data can an unauthenticated user get
2. Can user A read user B's data (how to change the request to do it)
3. Any keys in the frontend code that shouldn't be there
4. Any authorization done only in the frontend
5. Any user input concatenated directly into SQL or commands
6. Which endpoints have no rate limit and will get quota-bombed

For each, give: reproduction + fix. If you find nothing, say nothing; don't invent.
```

### E2｜Security boundary statement (when others' data is involved)

```
This part involves user data; I need you to list clearly:
1. What this implementation protects
2. What it does NOT protect (list each, don't omit)
3. Which scenarios it shouldn't be used for
4. What I, as a non-professional dev, cannot verify

Note: after writing, the statements like "not audited" / "not recommended for sensitive use"
are written by ME, not ghost-written by you in the README.
```

---

## F. Rescue & judgment

### F1｜Translate jargon (use the moment you don't understand)

```
A few words in what you just said I don't understand: [list terms].

Re-explain in plain language, requirements:
- No professional jargon, use life analogies
- Say what problem it solves, what happens if not used
- Say what the cost is (performance, money, complexity, future maintenance)
- If I don't use it, what's the worst that happens

I'll judge using the version I can understand.
```

### F2｜Options + tradeoffs (use before deciding)

```
I want to do [goal]. Give at least two options, each stating:
1. How (one sentence)
2. What's the cost (time, money, future maintenance difficulty)
3. When it'll break
4. What was given up

Finally give me one line "if it were you, which would you pick, and why" —
but the decision is mine; you only advise.
```

### F3｜Expose the bluff (when you suspect it's making things up)

```
I suspect some of what you just said is uncertain. Label each point:
- [Certain] what you verified
- [Guess] what you inferred from experience
- [Unsure] what you actually don't know

For [Unsure] parts, give a verification method, or just say you don't know.
Don't state uncertain things in a confident tone.
```

### F4｜Try first or ask first (visual / interaction)

```
I want to try [style/interaction/layout]; if you're unsure it'll work, just say so, don't argue feasibility for me.
Just give me a runnable minimal version; I'll see the effect and decide whether to continue.
No long analysis; I want something I can see.
```

### F5｜Data model design (before full-stack project starts)

```
I'm making [app], need to design the data model. Before writing any code:
1. List which tables, which fields each, what relationships between tables
2. For each table label: who can read, who can write, who can delete (by role)
3. Point out which fields are sensitive and need extra protection
4. Give the corresponding row-level security policy

I don't approve the schema, you don't start business code.
```

### F6｜Before changing data structure (protect data)

```
I'm changing the data structure. Before acting:
1. First give a backup plan, and say how to verify the backup can be restored
2. Give each migration step, label which are reversible, which irreversible
3. List irreversible steps separately for my confirmation
4. Don't connect to the production DB and run writes directly

Remember: an AI agent has deleted users' production databases before; I require you to be extra conservative on this.
```

---

## G. Session management: don't lose memory across sessions

### G1｜Write a handoff doc (before a long session ends, just send this)

```
This session is ending. Please write a handoff doc to HANDOFF.md:
organize the current task, what's done, stuck problems, next-step plan, and pitfalls hit into HANDOFF.md.
```

### G2｜First line of the next session

```
Read HANDOFF.md first.
```

**Why it's worth fixing**: AI sessions will definitely lose memory — a hard limit.
A single md file is currently the **lightest cross-session memory scheme** — no plugins, works across all tools.

### G3｜HANDOFF.md template

```markdown
# HANDOFF

## Current task
(one line: what you're doing, what the goal is)

## Done
- [x] ... (including where the changed files are)

## Stuck problems
(including approaches already tried and failed — avoid repeating them next time)

## Next-step plan
1. ...
2. ...

## Pitfalls hit
- ...

## To confirm / for me to decide
- ...
```

---

## H. Learning & creation

### H1｜QBS method (solve problems with classic books)

```
1. Send your problem to the AI, have it recommend a book published at least 30 years ago
2. Export the book's PDF
3. Give the PDF to any Agent, use the book-to-skill instruction to distill it into a Skill
4. Have the AI call the just-generated Skill to solve your problem
```

### H2｜Explain concepts with fables (for understanding / output)

```
Pick a graduate-level concept from some field, explain it clearly with a fable.
Don't reveal the answer at the start; only near the end of the story should the reader realize
it was this concept all along. After the story, explain the concept itself, and what each metaphor maps to.
```

---

## Usage wisdom (more important than the prompts themselves)

1. **A1 + A2 is the default combo** — paste almost every session; stack others as needed
2. **No more than 3 passages at once** — paste too many and the AI loses focus
3. **What's pasted into AGENTS.md is the real rule** — a prompt repeated 3+ times should be fixed into the project root
4. **C3 must be used at wrap-up** — the gap between the AI saying "done" and you confirming "truly done" is exactly this step
5. **Interrupt jargon translation anytime** — hear an unfamiliar word, stop immediately, don't wait for it to finish a whole paragraph
