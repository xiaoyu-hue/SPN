# SPN · AI Collaboration Rules for Non-Coders (English)

> **Self-precipitation**: amid the many options the AI hands you, let your own judgment precipitate and take shape.
> The whole idea fits in one line: **the AI writes the code; you make the calls.**

[![docs CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-blue)](../LICENSE-DOCS.md)
[![code MIT](https://img.shields.io/badge/code-MIT-green)](../LICENSE)
[![lang 中文 / English](https://img.shields.io/badge/lang-中文%20%2F%20English-orange)](./README.md)
[![doc-lint](https://github.com/xiaoyu-hue/SPN/actions/workflows/doc-lint.yml/badge.svg)](https://github.com/xiaoyu-hue/SPN/actions/workflows/doc-lint.yml)
[![doc-quality](https://github.com/xiaoyu-hue/SPN/actions/workflows/doc-quality.yml/badge.svg)](https://github.com/xiaoyu-hue/SPN/actions/workflows/doc-quality.yml)
[![secret-scan](https://github.com/xiaoyu-hue/SPN/actions/workflows/secret-scan.yml/badge.svg)](https://github.com/xiaoyu-hue/SPN/actions/workflows/secret-scan.yml)

[简体中文](../README.md) · English

---

## Table of contents

- [What this is](#what-this-is)
- [Who it's for](#who-its-for)
- [Quick start](#quick-start)
- [Look things up as needed](#look-things-up-as-needed)
- [Repository structure](#repository-structure)
- [Core content](#core-content)
- [Workflow standards](#workflow-standards)
- [How this differs from typical AGENTS.md templates](#how-this-differs-from-typical-agentsmd-templates)
- [Three things most worth remembering](#three-things-most-worth-remembering)
- [Where the rules come from](#where-the-rules-come-from)
- [Acknowledgments](#acknowledgments)
- [Known limitations](#known-limitations)
- [License](#license)
- [Contributing](#contributing)

---

## What this is

SPN (Self-precipitation) is a set of AI collaboration rules for people with **zero programming background**: amid the many options the AI hands you, let your own judgment precipitate and take shape.

AI coding tools are optimized to make the demo work. For a developer that's a productivity win; for someone who can't read code it's a risk — you can't tell whether what it wrote is correct, or whether it quietly expanded the scope of changes. **Security boundaries are the one part that produces no visible result**: a database table that's locked and one that's wide open render an identical page.

These rules keep **the judgment with the human**, without requiring the human to understand code. They don't try to cover everything; instead, each rule maps to a class of real failure.

## Who it's for

- People who can't code but want to ship a prototype or a small tool with AI
- Non-technical users worried about the AI "changing things," "shipping without asking," or "leaking secrets"
- Anyone who wants a collaboration baseline they can copy and apply immediately

If you're a professional developer, parts of this (e.g. "translate the jargon," "try before asking") will feel redundant — follow your team's own conventions.

## Quick start

### For users: three steps

1. **Copy `AGENTS.md`** into your project directory. Tools that support AGENTS.md (Cursor, Codex, Copilot, Gemini CLI, Aider, Windsurf, and others) load it automatically before work begins.
2. **Look up `references/` as needed**: when a concrete question arises (about to ship, writing a README, not sure how to phrase a request), open the matching doc.
3. **Before shipping or any irreversible decision**, run through [`references/07-decision-review.md`](references/07-decision-review.md) — think through downside / cost of not doing it / when you'd regret it before acting.

> Note: Claude Code doesn't read AGENTS.md by default when its own config file exists — you need to import it. A safe pattern is to use AGENTS.md as the shared baseline, then add a thin tool-specific file (e.g. put `@AGENTS.md` inside `CLAUDE.md`).

### For developers: local preview and CI

- After cloning, `skills/spn/` is a self-contained, installable skill package — see [`skills/spn/INSTALL.md`](../skills/spn/INSTALL.md).
- Documentation and quality gates are enforced in CI: secret scan **gitleaks**, dead-link check **lychee**, terminology **vale**, and hardcoded-number check **doc-lint** (see `.github/workflows/`).
- To change the rules: edit the **root directory** (the source of truth), then let the publish flow sync to `docs/` (English) and `skills/spn/` (package).
- To bring the rules into your own Agent: load `skills/spn/`, or copy the root `AGENTS.md` into your project.

## Look things up as needed

| What you're doing | Read this (English, this folder) |
|---|---|
| Who decides what; the try-vs-ask test | [`references/01-collaboration-philosophy.md`](references/01-collaboration-philosophy.md) |
| About to ship | [`references/02-pre-launch-security-checklist.md`](references/02-pre-launch-security-checklist.md) |
| Writing a README / picking a license / keeping numbers from going stale | [`references/03-documentation-disclosure-maintenance.md`](references/03-documentation-disclosure-maintenance.md) |
| Not sure how to phrase a request | [`references/04-prompt-library.md`](references/04-prompt-library.md) |
| See real good/bad collaboration examples | [`references/05-collaboration-examples.md`](references/05-collaboration-examples.md) |
| Curated external projects / Skills / plugins | [`references/06-ecosystem-and-integrations.md`](references/06-ecosystem-and-integrations.md) |
| Decision review before irreversible / paid / public calls | [`references/07-decision-review.md`](references/07-decision-review.md) |
| Doc-and-code sync after changes | [`references/08-doc-sync.md`](references/08-doc-sync.md) |

> Everything above, plus `AGENTS.md`, `SKILL.md`, `SECURITY.md`, and `CONTRIBUTING.md`, is available in English right here under `docs/`.

## Repository structure

SPN uses a **universal layer + personal layer** structure, plus an English edition and a ready-to-load skill package:

```
SPN/
├── README.md              ← 简体中文，规范源 (this file's Chinese original)
├── AGENTS.md              ← universal rules, for everyone (what the AI actually loads)
├── SKILL.md               ← skill entry point and full documentation (Chinese)
├── references/            ← universal rules in detail (8 docs, Chinese)
│   ├── 01-collaboration-philosophy.md
│   ├── 02-pre-launch-security-checklist.md
│   ├── 03-documentation-disclosure-maintenance.md
│   ├── 04-prompt-library.md
│   ├── 05-collaboration-examples.md
│   ├── 06-ecosystem-and-integrations.md
│   ├── 07-decision-review.md        ← workflow template: pre-decision questions
│   └── 08-doc-sync.md               ← workflow template: pre-release sync
├── docs/                  ← English edition: full mirror (README + AGENTS + SKILL + references)
├── skills/spn/            ← self-contained, installable skill package (Chinese)
├── personal/              ← the author's own layer, safe to skip
└── LICENSE-DOCS.md        ← CC BY 4.0 terms for all documentation
```

- Only want the rules? Read the root directory and ignore `personal/`.
- Want the English version? Everything is mirrored under `docs/`.
- Want to load the rules into an AI Agent directly? Use `skills/spn/` — see [`skills/spn/INSTALL.md`](../skills/spn/INSTALL.md).
- Want your own copy? Duplicate `personal/`, fill in your context, and let `AGENTS.md` inherit the universal rules — you only add your own layer. See `personal/README.md`.

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

## Workflow standards

Two reusable workflow standards you can drop into any project (each ships with fill-in checklists and log templates):

- **`references/07-decision-review.md`** — a pre-decision questioning tool: the three decision questions (downsides / cost of not doing it / regret conditions) + five layers of follow-up + regret-scenario quick reference + a decision-log template. Complements post-decision records like ADR / CHANGELOG.
- **`references/08-doc-sync.md`** — an execution checklist to keep "what the docs say" consistent with "what the code actually does" after code / CI / feature changes: the Single Source of Truth principle + sync checklist + SemVer rules + pre-release verification + a sync-check template.

> Chinese originals: [`references/07-决策审查清单.md`](../references/07-决策审查清单.md) and [`references/08-文档同步规范.md`](../references/08-文档同步规范.md).

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

## Where the rules come from

This isn't a template. Behind every rule is a real failure, drawn from a non-coder shipping multiple projects with AI:

| What actually happened | What the AI did | What the human did |
|---|---|---|
| Shipping a project for the first time | Recommended several static-hosting platforms | It gave a candidate list, not a command; the human picked the platform |
| Whether two visual styles could merge | Said it couldn't guarantee a merge | The human just tried it — and the result became the project's visual foundation |
| Drawing a security boundary for a crypto app | Wrote key agreement and signing code cleanly | But the "not audited" / "not for sensitive use" disclaimer was written by the human, into the README |

The common thread: **the AI supplies capability and options; the human makes the call and draws the boundary.**

The full narrative and the try-vs-ask test are in [`references/01-collaboration-philosophy.md`](references/01-collaboration-philosophy.md).

## Acknowledgments

SPN stands on the shoulders of many open-source specs, tools, and communities. The following are **directly referenced, aligned with, or inspired this project**, all used under their respective licenses, and **no source code is copied in** (per the "link, don't vendor" principle in `references/06`):

- **Anthropic Agent Skills** — `skills/spn/` adopts its official Agent Skills spec (frontmatter + description-based trigger). See [`anthropics/skills`](https://github.com/anthropics/skills).
- **Creative Commons** — all documentation is released under **CC BY 4.0** (Attribution 4.0 International); the license text is published by CC.
- **Keep a Changelog / Semantic Versioning** — `CHANGELOG.md` and the version scheme follow their conventions.
- **Curated ecosystem index (`references/06`)** — the same-type projects, skill collections, security/doc tools, and plugins/MCPs listed there are the sources of this repo's research and further reading; see that doc.
- **CI tooling** — secret scanning [`gitleaks`](https://github.com/gitleaks/gitleaks), dead-link checking [`lychee`](https://github.com/lycheeverse/lychee), and terminology checking [`vale`](https://github.com/errata-ai/vale) back this repo's quality gates.

> The rules themselves (including the two workflow standards `references/07` and `references/08`) are the author's original work, shared under CC BY 4.0. If we've used your work, open an issue and we'll add proper attribution.

## Known limitations

- Optimized for users who can't read code. Professional developers will find parts redundant and should follow their team's own conventions.
- The SQL and shell commands in `02` target Supabase/Postgres. Firebase, Cloudflare D1, and other backends need adjustment (adaptation notes are in that doc).
- Security incidents and free-tier figures cited here were verified in October 2026 and will drift. Re-check before relying on them.
- **These rules are not a substitute for a professional security audit.** Apps handling other people's genuinely sensitive data (medical, financial, identity) should still get one.
- All references (01–08), plus `AGENTS.md`, `SKILL.md`, `SECURITY.md`, and `CONTRIBUTING.md`, are available in English under `docs/`. `personal/` remains Chinese-only.

## License

This repo uses **separate licenses for code and documentation**:

| Content | License | File |
|---|---|---|
| **Code** (scripts, CI config, executable tooling) | **MIT** | `LICENSE` |
| **Documentation** (all rules, prompts, references) | **CC BY 4.0** (attribution) | `LICENSE-DOCS.md` |

You may use, redistribute, and modify the documentation freely with attribution (required under CC BY 4.0), including commercially; code is used under the MIT License. Full terms are in the respective license files.

> Note: `LICENSE` (MIT) is auto-recognized by GitHub and shown as a badge in the repo sidebar; the documentation's CC BY 4.0 terms are authoritative in `LICENSE-DOCS.md` (GitHub's sidebar only auto-detects CC0-1.0, not CC BY 4.0).

## Contributing

Issues and pull requests are welcome.

- For bugs and ideas: state what you did, what you expected, and what actually happened.
- For structural changes (architecture, dependencies, security): open an issue first to align on direction.
- Chinese or English both work; simple English is fine.
- For the boundary between universal and personal rules, and how to add a new rule, see `CONTRIBUTING.md`.
