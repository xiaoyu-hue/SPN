# SPN · AI Collaboration Rules (For Non-Coders)

> **SPN = Self-precipitation**: let your own judgment precipitate and take shape amid the many options the AI hands you.
> For people who can't code but want to build real things with AI.
> **The AI writes the code. You make the calls.**

[简体中文](./README.md) | English

---

## What this is

A set of AI collaboration rules for people with **zero programming background**.

AI coding tools are optimized to make *the demo work*. For a developer that's a productivity win. For someone who can't read code, it's a risk:

- You can't tell whether what it wrote is correct
- You can't tell if it quietly expanded the scope of changes
- **Security boundaries are the one part that produces no visible result** — a database table that's locked and one that's wide open render an identical page
- It will confidently say "done" without having run anything

These rules keep **the judgment with the human**, without requiring the human to understand code.

This isn't a template. Each rule maps to a class of real failure.

---

## Quick start

**Fastest path: copy `AGENTS.md`**

Drop the root `AGENTS.md` into your project directory. Tools that support AGENTS.md (Cursor, Codex, Copilot, Gemini CLI, Aider, Windsurf, and others) load it automatically before work begins.

> ⚠️ Claude Code doesn't read AGENTS.md by default when its own config file exists — you need to import it. A safe pattern: use AGENTS.md as the shared baseline, then add a thin tool-specific file (e.g. put `@AGENTS.md` inside `CLAUDE.md`).

**Look things up as needed**

| What you're doing | Read this |
|---|---|
| Who decides what; when to try vs. when to ask | `references/01-协作哲学与判断归属.md` (English: `.en.md`) |
| About to ship | `references/02-上线前安全自查.md` (English: `.en.md`) |
| Writing a README / picking a license / keeping numbers from going stale | `references/03-文档、局限披露与事实维护.md` |
| Not sure how to phrase a request | `references/04-提示词库.md` |

---

## This repo has two layers

```
SPN/
├── AGENTS.md        ← universal rules, for everyone (what the AI actually loads)
├── SKILL.md         ← skill entry / full-version docs
├── references/      ← universal rules (4 docs; 01/02 also in English)
└── personal/        ← the author's own layer, ⚠️ skip it
```

**`personal/` is not part of the rules.** It's just the author keeping private context
in the same repo — one push, one version, and the case studies above stay traceable.

If you only want the rules: **read the root directory, ignore `personal/`.**

---

## Core

### Three authorization tiers

The only test that matters: **who pays the cost of undoing it.**

- 🟢 **Just do it** — reading files, running tests, locally reversible changes
- 🟡 **Ask first** — changing DB schema, deploying, publishing, outward-facing actions, bulk operations, anything that changes Git state
- 🔴 **Never** — committing secrets, putting service-role keys in frontend code, doing authorization only in the frontend, string-concatenating SQL, silently swallowing errors, fabricating test results

### Three moves that matter most for non-coders

1. **Translate before you decide.** Never approve something using words you don't understand. Not understanding is not your fault — it failed to explain.
2. **Try first or ask first?** One test: *can it be undone with one click?* If yes, try it. If no, ask.
3. **Capability is not a guarantee.** The AI can write crypto code. The phrase "not professionally audited" is yours to write, not its.

### Five-step handshake

State the goal → AI restates the acceptance criteria → AI gives options with tradeoffs → deliver in small verifiable steps → human verifies, AI states honestly what it did and didn't confirm

### Important decisions: three-perspective analysis (added after v1.0.0)

For important calls (architecture, whether to ship, etc.), require the AI to analyze from three perspectives — **full rebuttal → switch to support → neutral comparison** — instead of handing you a single conclusion. Paired with a **debug three-step rule**: describe the error → explain the cause in plain language → give fix steps; no rewriting blindly before the root cause is found.

---

## How this differs from typical AGENTS.md templates

| Typical template | These rules |
|---|---|
| Lists commands and code style | Defines who decides and when to stop |
| Assumes the reader knows tech | **Assumes the reader knows nothing about tech** |
| Lists what you can do | Half the content is **what you must not do, and what it can't do** |
| Gives a conclusion | Requires the AI to present tradeoffs for a human to decide |
| Generic best practices | Every rule maps to a real failure mode |

---

## Limitations (stated honestly)

- Optimized for **users who can't read code**. Professional developers will find parts redundant (especially "translate the jargon" and "try before asking") and should follow their team's own conventions
- The SQL and shell commands in `02` target Supabase/Postgres. Firebase, Cloudflare D1, and other backends need adjustment (adaptation notes added to that doc)
- Security incidents and free-tier figures cited here were verified in 2026-10 and will drift. Re-check before relying on them
- **These rules are not a substitute for a professional security audit.** Apps handling other people's genuinely sensitive data (medical, financial, identity) should still get one
- References `01` and `02` are available in English. `03`, `04`, and `personal/` are Chinese-only for now — translations welcome

---

## License (layered open source)

This repo uses **separate licenses for code and documentation**:

| Content | License | File |
|---|---|---|
| **Code** (scripts, CI config, executable tooling) | **MIT** | `LICENSE` |
| **Documentation** (all rules, prompts, references) | **CC BY 4.0** (attribution) | `LICENSE-DOCS.md` |

You may use, redistribute, modify, and use commercially with attribution (docs require attribution under CC BY 4.0; code under MIT has no attribution requirement but retain it where reasonable).

---

> *"Stay curious. Go explore. Try it. Then verify it."*
