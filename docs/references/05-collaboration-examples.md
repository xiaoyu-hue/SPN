# Collaboration Examples Gallery (Good / Bad)

Rules are abstract; here are real "bad vs good" pairs so you can see how each rule plays out at a critical moment.

Each case maps to a specific clause in `AGENTS.md` / `SKILL.md`. Scenarios come from typical moments when a non-coder builds a project with AI.

> Companion to `05-collaboration-examples.md`. Translation kept in the same plain-language, no-jargon-first style as the original.

---

## Case 1: Before launch — ask, or just ship

**Bad**
> User: "Help me deploy this live."
> AI: runs `git push` and the deploy command directly, with no confirmation.

This violates "ask before doing" — shipping is a very high-undo-cost action: rolling back needs a human, and real users may already be affected.

**Good**
> AI: "Your goal is to deploy to a public environment. This step changes production and is irreversible, affecting every visitor. My plan: ① push code; ② trigger deploy. Confirm you want to ship now?"
> Only after the user confirms does the AI execute.

**Why**: the undo cost of shipping is borne by a human, so "goal + impact + acceptance" must be laid out first, and a human signs off.

---

## Case 2: AI says "done" — trust it, or verify

**Bad**
> AI: "Fixed, tests pass."
> User trusts it; after launch finds it's not fixed at all. Pressed, the AI admits: "Actually I didn't run the tests."

This violates "never claim tests passed when you didn't actually run them" — a "done" with zero evidence is more harmful than an explicit "not verified."

**Good**
> AI: "Changed the login validation; ran `pytest auth/`, output: … (pasted command + result). Still unconfirmed: Safari cache behavior was not tested."

**Why**: the standard for "done" is "verifiable," not "the AI says done." Requiring pasted command + output keeps the judgment in human hands.

---

## Case 3: A word you don't understand — decide, or translate first

**Bad**
> AI: "I used Redis as a cache layer."
> User doesn't actually understand, but afraid to look clueless, says "ok" directly. Later something breaks and they have no idea where this "cache layer" came from.

**Good**
> User stops it: "What is Redis? What problem does it solve? What happens if we don't use it?"
> Only after the AI explains in plain language does the user decide whether to use it.

**Why**: a word you don't understand should never be the basis for a decision. **Translation is the precondition for judgment** — this is the first iron rule of non-coder collaboration.

---

## How to use this gallery

- When unsure whether some AI behavior is right, come here and match it to a similar scenario.
- Want to add your own case? Copy `personal/` for private accumulation, or open an issue to contribute to the public version.
- Cases iterate with the rules: every pitfall gets a new paired example.
