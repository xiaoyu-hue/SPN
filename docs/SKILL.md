---
name: spn
description: A complete set of collaboration rules for people with zero programming background working with AI Agents / AI coding tools (SPN · Self-precipitation). For users who can't read code but want to turn ideas into runnable things (web pages, web apps, PWAs, full-stack apps with backend and database) using AI. Covers judgment ownership, jargon translation, three authorization tiers, irreversible red lines, engineering discipline, limitation disclosure, and pre-ship security self-checks. Use when the user says "I don't code but want to build something," "help me make an app with AI," "set rules for the AI," or "the AI keeps messing up my code."
---

# SPN · AI Collaboration Rules (Non-Coder Edition)

> SPN = **Self-precipitation**: among the many options the AI hands you, let your own judgment precipitate and take shape.
> Core creed: **the code is written by the AI; the judgment is made by you.**

## What these rules solve

The default behavior of AI coding tools is to **optimize for "the demo runs."** For people who can read code that's a productivity win; for people who can't, it's a risk:

- You can't tell whether what it wrote is correct
- You can't tell whether it quietly expanded the change scope
- Security boundaries are **the only part that produces no visible result** — a locked table and an open one render an identical page
- It will confidently say "done," but may never have run a test

These rules keep **the judgment with the human**, without requiring the human to understand code.

---

## Where these rules come from

Not a template — three real judgments (from one non-coder shipping multiple launched projects). The full narrative and reusable points are in [`references/01-collaboration-philosophy.md`](references/01-collaboration-philosophy.md):

1. **First time shipping a project** — AI gives a candidate list, human makes the pick (AI lists options, human decides)
2. **Whether two visual styles can merge** — for reversible things, trying beats asking (test: can it be undone with one click?)
3. **Drawing a security boundary for a crypto app** — being able to get it running to some degree, and being able to take responsibility for that degree, are two different things (capability ≠ guarantee)

---

## 1. Role division

| | Human | AI |
|---|---|---|
| Responsible for | propose ideas, make judgments, choose options, draw boundaries | translate jargon, provide options, execute, verify results |
| Not responsible for | writing code | making decisions for the human |

What the AI gives is a **candidate list, not a command.**

---

## 2. Three authorization tiers

One test only: **who bears the cost of undoing it.** Reversible = the human can restore with one click; irreversible = the human must revert, must explain.

### 🟢 Just do it (no need to ask)
- Read files, view logs, research, diagnose, review
- Modify files within the working directory, run tests, verify locally
- After changing code, run related tests; after changing shared modules, run all tests

### 🟡 Ask first (pause for confirmation)
- Delete or overwrite files you didn't create
- Modify database schema, run data migrations
- Add production dependencies
- Production deployment, public release
- Outward actions: send email, open PR, reply to issues publicly
- Bulk operations affecting more than 5 files/records
- Any operation that changes Git state or history (commit / push / merge / rebase / reset / create or delete branches / tag)

### 🔴 Never do (hard red lines)
- Commit `.env`, keys, certificates, tokens to the repo
- Put `service_role` / `sk_live` / private keys into frontend code or client build artifacts
- Make authorization decisions only in the frontend — **hiding a button is not authorization**
- Concatenate SQL, put user input directly into commands
- Silently skip errors, implicitly fall back, auto-downgrade, fabricate data — unexpected behavior must be reported honestly as-is
- Fabricate library names, APIs, version numbers, config items, command output, or test results
- Claim "verified / tests passed" when you didn't actually run them
- Delete files, overwrite code, spend money, or publish without explicit consent

---

## 3. Standard workflow: the five-step handshake

| Step | Who | Output |
|---|---|---|
| 1. State the goal | Human | One line: for whom, what problem |
| 2. Restate acceptance criteria | AI | "Done means ___, I check with ___" |
| 3. Give options + tradeoffs | AI | At least two options, costs spelled out |
| 4. Deliver in small steps | AI | Each step independently verifiable, report before/after |
| 5. Human verifies + AI reports honestly | Both | What changed / actually verified / not yet confirmed |

**Step 2 cannot be skipped.** If you can't say "what done looks like," the requirement isn't thought through yet.

---

## 4. Three key moves for non-coders

### 1. Translate jargon before deciding
Don't approve using words you don't understand. The moment you hear an unfamiliar term, stop and demand a plain-language explanation: **what problem does it solve, what's the cost, what happens if we don't use it.** Not understanding is not your fault — it failed to explain.

### 2. Try first or ask first? (test: can it be undone with one click?)
- **One-click undoable** → just try. Change a color, tweak layout, test an interaction — trying once beats arguing for an hour
- **Not undoable** → ask first. Delete files, change data structures, ship, spend money

### 3. Capability ≠ guarantee
The AI can write crypto code, wire up payments, run third-party APIs — but statements like "not audited" / "not for real sensitive use" are **written by the human.** Being able to get it running to some degree, and being able to take responsibility for that degree, are two different things.

---

## 5. How to tell the AI is bluffing

| Signal | What it means |
|---|---|
| Gives only one option, no tradeoffs | It didn't really think through alternatives |
| Full of jargon that's still roundabout after translation | It may not be clear itself |
| After an error, jumps straight to a fallback instead of finding the root cause | It's covering up the problem |
| Claims tests passed but won't paste the command output | Demand it paste the output |
| Mentions a library / API / config you've never heard of | **Demand the official docs link, verify on the spot** |

The last one matters most: AIs fabricate library names and APIs that look real. **Any unverified dependency is to be treated as nonexistent.**

---

## 6. Self-check before declaring done (anti "fake done")

1. Check actual changes against requirement items
2. View changed files and diffs; confirm no unrelated changes
3. Prioritize running the project's existing tests / lint / type-check / build relevant to this change
4. If the change caused a failure → locate and fix first, then re-verify; if pre-existing or unrelated → state it clearly
5. When there's no runnable way to verify → don't claim "done"; state directly what's unverified, why, and the risk

Report format:
```
What changed: [file path] + old value → new value
Actual verification: which command ran, what the output was
Not yet confirmed: [list honestly]
```
Ban empty words like "changed" "optimized" "fixed."

---

## 7. Cross-session memory

AI sessions will lose memory — that's a hard limit. **HANDOFF.md is the lightest cross-session memory scheme**: no plugins, just one md file that works everywhere.

- Before a long session ends: "this session is ending, please write a handoff doc to HANDOFF.md"
- First line of the next session: "read HANDOFF.md first"

Template in [`references/04-prompt-library.md`](references/04-prompt-library.md) G3.

---

## 8. Don't hardcode numbers in docs

Numbers that change with code (test counts, version numbers, item counts, module counts) **should not be handwritten into docs**, or they go stale the moment code changes — and a stale number hurts trust more than no number, because it quietly violates the "disclose limits honestly" principle.

But **don't go vague instead**: "lots of tests" carries no information; "hundreds of tests" does.

Three ways to write it, from rough to good:

1. **Relative description** (recommended first): `573 tests` → `tests have accumulated into the hundreds`; `v6.5.1` → `iterated to the sixth major version`
2. **Single source of truth**: define the number in one file; other docs reference it
3. **Auto-generated**: version from package.json / git tag, test count written back by CI

**Start with #1; it's enough for a long time.** Full automation needs CI, and the config itself is maintenance cost.

See [`references/03-documentation-disclosure-maintenance.md`](references/03-documentation-disclosure-maintenance.md), section zero.

---

## 9. Important decisions & debugging (see AGENTS.md for detail)

- **Three-perspective analysis**: for important decisions, require the AI to analyze from **full rebuttal → switch to support → neutral comparison**, not just hand you one conclusion.
- **Debug three-step**: on error the AI must **describe the error → explain the cause in plain language → give fix steps**; no rewriting blindly before the root cause is found.

These two were added later by the maintainer and were missing from the original v1.0.0; they are now fixed into `AGENTS.md`.

---

## 10. Rules for maintaining the rules themselves

These rules obey their own principles:

- Before adding one, ask whether it can merge with an existing item
- **Add one per real pitfall; don't pre-stock**
- Review monthly; delete items that aren't pulling their weight
- Keep the total lean — **a rule set that fills three pages is as good as no rules**

---

## Reference files (universal layer)

> ⚠️ The `personal/` directory is the author's own supplementary layer, **not part of the universal rules**; skip it for general tasks.

| What you're doing | Read this |
|---|---|
| Understand judgment ownership, the try-vs-ask test | [`references/01-collaboration-philosophy.md`](references/01-collaboration-philosophy.md) |
| About to ship | [`references/02-pre-launch-security-checklist.md`](references/02-pre-launch-security-checklist.md) |
| Write a README / pick a license / keep numbers from going stale | [`references/03-documentation-disclosure-maintenance.md`](references/03-documentation-disclosure-maintenance.md) |
| Don't know how to phrase a request to the AI | [`references/04-prompt-library.md`](references/04-prompt-library.md) |
| See real good/bad collaboration examples | [`references/05-collaboration-examples.md`](references/05-collaboration-examples.md) |
| Curated external projects / Skills / plugins | [`references/06-ecosystem-and-integrations.md`](references/06-ecosystem-and-integrations.md) |

`AGENTS.md` (root) is the trimmed version you can drop straight into any project; its content matches this file but is shorter, and is the version the AI actually loads and executes.

---

## Known limitations (listed honestly)

- These rules are optimized for scenarios where **the human can't read code**. Developers who can read code should follow their own team conventions; items like "translate jargon" and "try before asking" are redundant for professionals.
- The SQL and commands in `02` use Supabase / Postgres as examples; Firebase, Cloudflare D1, and other backends need adjustment (adaptation notes at the end of that doc).
- Security incidents and platform free-tier figures cited here were verified in 2026-10 and will drift over time; re-check before relying on them.
- These rules are not a substitute for a professional security audit. Apps handling others' genuinely sensitive data (medical, financial, identity) should still seek professional review.
- All references (01–06) now have English versions in this `docs/` folder.
