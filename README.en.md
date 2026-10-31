# SPN · AI Collaboration Rules for Non-Coders

SPN (Self-precipitation) is a set of AI collaboration rules for people with **zero programming background**: amid the many options the AI hands you, let your own judgment precipitate and take shape.

The whole idea fits in one line: **the AI writes the code; you make the calls.**

[简体中文](./README.md) · English

---

## What this is

A set of collaboration rules for people who can't read code but want to build real products with AI.

AI coding tools are optimized to make the demo work. For a developer that's a productivity win; for someone who can't read code it's a risk — you can't tell whether what it wrote is correct, or whether it quietly expanded the scope of changes. **Security boundaries are the one part that produces no visible result**: a database table that's locked and one that's wide open render an identical page.

These rules keep **the judgment with the human**, without requiring the human to understand code. They don't try to cover everything; instead, each rule maps to a class of real failure.

## Who it's for

- People who can't code but want to ship a prototype or a small tool with AI
- Non-technical users worried about the AI "changing things," "shipping without asking," or "leaking secrets"
- Anyone who wants a collaboration baseline they can copy and apply immediately

If you're a professional developer, parts of this (e.g. "translate the jargon," "try before asking") will feel redundant — follow your team's own conventions.

## Quick start

**Simplest path: copy `AGENTS.md`**

Drop the root `AGENTS.md` into your project directory. Tools that support AGENTS.md (Cursor, Codex, Copilot, Gemini CLI, Aider, Windsurf, and others) load it automatically before work begins.

> Note: Claude Code doesn't read AGENTS.md by default when its own config file exists — you need to import it. A safe pattern is to use AGENTS.md as the shared baseline, then add a thin tool-specific file (e.g. put `@AGENTS.md` inside `CLAUDE.md`).

**Look things up as needed**

| What you're doing | Read this |
|---|---|
| Who decides what; the try-vs-ask test | `references/01-协作哲学与判断归属.md` (English: `.en.md`) |
| About to ship | `references/02-上线前安全自查.md` (English: `.en.md`) |
| Writing a README / picking a license / keeping numbers from going stale | `references/03-文档、局限披露与事实维护.md` |
| Not sure how to phrase a request | `references/04-提示词库.md` |

## Repository structure

SPN uses a **universal layer + personal layer** structure:

```
SPN/
├── AGENTS.md        ← universal rules, for everyone (what the AI actually loads)
├── SKILL.md         ← skill entry point and full documentation
├── references/      ← universal rules in detail (4 docs; 01/02 also in English)
└── personal/        ← the author's own layer, safe to skip
```

`personal/` is **not** part of the rules. It's just the author keeping private context in the same repo — one push, one version, and the case studies above stay traceable.

- Only want the rules? Read the root directory and ignore `personal/`.
- Want your own copy? Duplicate `personal/`, fill in your context, and let `AGENTS.md` inherit the universal rules — you only add your own layer. See `personal/README.md`.

## Where the rules come from

This isn't a template. Behind every rule is a real failure, drawn from a non-coder shipping multiple projects with AI:

| What actually happened | What the AI did | What the human did |
|---|---|---|
| Shipping a project for the first time | Recommended several static-hosting platforms | It gave a candidate list, not a command; the human picked the platform |
| Whether two visual styles could merge | Said it couldn't guarantee a merge | The human just tried it — and the result became the project's visual foundation |
| Drawing a security boundary for a crypto app | Wrote key agreement and signing code cleanly | But the "not audited" / "not for sensitive use" disclaimer was written by the human, into the README |

The common thread: **the AI supplies capability and options; the human makes the call and draws the boundary.**

The full narrative and the try-vs-ask test are in `references/01-协作哲学与判断归属.md`.

## Core content

### Three authorization tiers (test: who pays the cost of undoing it)

- **Allowed (just do it)** — reading files, running tests, locally reversible changes
- **Ask first** — changing DB schema, deploying, publishing, outward-facing actions, bulk operations, anything that changes Git state
- **Never** — committing secrets, putting service-role keys in frontend code, doing authorization only in the frontend, string-concatenating SQL, silently swallowing errors, fabricating test results

### Three moves that matter most for non-coders

1. **Translate before you decide.** Never approve something using words you don't understand. Not understanding is not your fault — it failed to explain.
2. **Try first or ask first?** One test: can it be undone with one click? If yes, try it. If no, ask.
3. **Capability is not a guarantee.** The AI can write crypto code. The phrase "not professionally audited" is yours to write, not its.

### Standard workflow (the five-step handshake)

State the goal → AI restates the acceptance criteria → AI gives options with tradeoffs → deliver in small verifiable steps → human verifies, and AI states honestly what it did and didn't confirm

### Important decisions: three-perspective analysis

For important calls (architecture, whether to ship, etc.), require the AI to analyze from three perspectives — **full rebuttal → switch to support → neutral comparison** — instead of handing you a single conclusion.

Paired with the **debug three-step rule**: describe the error → explain the cause in plain language → give fix steps; no rewriting blindly before the root cause is found.

## How this differs from typical AGENTS.md templates

| Typical template | These rules |
|---|---|
| Lists commands and code style | Defines who decides and when to stop |
| Assumes the reader knows tech | **Assumes the reader knows nothing about tech** |
| Lists what you can do | Half the content is **what you must not do, and what it can't do** |
| Gives a conclusion | Requires the AI to present tradeoffs for a human to decide |
| Generic best practices | Every rule maps to a real failure mode |

## Three things most worth remembering

1. Never approve something using words you don't understand. Stop, ask it to translate into plain language, then decide.
2. Can it be undone with one click? If yes, try it; if no, ask. This single test resolves most "should I ask first?" hesitation.
3. "Done" from the AI is not the same as actually done. Use the "self-check five" to hold it accountable (see `AGENTS.md`).

## Known limitations

- Optimized for users who can't read code. Professional developers will find parts redundant and should follow their team's own conventions.
- The SQL and shell commands in `02` target Supabase/Postgres. Firebase, Cloudflare D1, and other backends need adjustment (adaptation notes are in that doc).
- Security incidents and free-tier figures cited here were verified in October 2026 and will drift. Re-check before relying on them.
- **These rules are not a substitute for a professional security audit.** Apps handling other people's genuinely sensitive data (medical, financial, identity) should still get one.
- References `01` and `02` are available in English. `03`, `04`, and `personal/` are Chinese-only for now — translations welcome.

## Contributing

Issues and pull requests are welcome.

- For bugs and ideas: state what you did, what you expected, and what actually happened.
- For structural changes (architecture, dependencies, security): open an issue first to align on direction.
- Chinese or English both work; simple English is fine.
- For the boundary between universal and personal rules, and how to add a new rule, see `CONTRIBUTING.md`.

## License

This repo uses **separate licenses for code and documentation**:

| Content | License | File |
|---|---|---|
| **Code** (scripts, CI config, executable tooling) | **MIT** | `LICENSE` |
| **Documentation** (all rules, prompts, references) | **CC BY 4.0** (attribution) | `LICENSE-DOCS.md` |

You may use, redistribute, and modify the documentation freely with attribution (required under CC BY 4.0), including commercially; code is used under the MIT License. Full terms are in the respective license files.

> Note: `LICENSE` (MIT) is auto-recognized by GitHub and shown as a badge in the repo sidebar; the documentation's CC BY 4.0 terms are authoritative in `LICENSE-DOCS.md`.
