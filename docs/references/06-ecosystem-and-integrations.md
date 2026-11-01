# references/06 · Ecosystem & Integrations

> A curated index of external **open-source projects, Skills, plugins, and toolchains** that relate to SPN.
> Core idea: **reference, don't copy** — we only link, annotate, and explain. We never move third-party code or content into this repo.
> This keeps SPN's own curated voice intact and **fully preserves each project's original open-source license**.

## 1. Integration principles (read first)

1. **Reference, don't copy**: every entry below is an external link plus a usage note. To use a project's capability, install it into your Agent per its official docs — don't copy it into SPN.
2. **Keep the original license**: each entry notes its license (stars and licenses are a **point-in-time snapshot**; verification records live in `FACTS.md`). When using third-party components, honor their license: MIT / Apache-2.0 usually only require keeping the copyright and license notice; **GPL-family licenses are strong copyleft — never copy wholesale**.
3. **Don't dilute the positioning**: SPN is a "non-technical users × AI collaboration rules" knowledge pack. These resources are extensions and corroboration only; they are not merged into the core rules.
4. **Data is a snapshot**: star counts reflect popularity on the research date only, not a quality guarantee.

## 2. Peer projects (similar to SPN: "non-technical × AI collaboration")

| Project | Stars | License | Relation to SPN | Tier |
|---|---|---|---|---|
| [yuanlalaini-bit/ai-4u](https://github.com/yuanlalaini-bit/ai-4u) | 0 | MIT | Near-isomorphic rival: same philosophy/structure/Skill format; stronger on harness breadth (6) and teaching examples | ② link |
| [daoyi2026/vibe-coding-zero-to-ship](https://github.com/daoyi2026/vibe-coding-zero-to-ship) | 94 | MIT | Truly isomorphic: for non-technical builders, stresses "irreversible actions left to the user"; a single runnable Skill | ② link |
| [Protocol-Wealth/pw-learnai-core](https://github.com/Protocol-Wealth/pw-learnai-core) | 0 | Apache-2.0 | "AI Operator" graded learning path with AGENTS.md / CHANGELOG loop | ② link |

> Note: when I looked (2026-10-31, recorded in `FACTS.md`) I found only **ai-4u** and **daoyi2026** in this niche, both very early.
> **This reflects my search, not a market census** — GitHub may well have projects I missed. Found one? Open an issue and I'll add it.
> SPN leads on documentation depth and engineering; treat them as peers to cross-link, not to merge.

## 3. Skill collections (marketplaces & specs)

| Project | Stars | License | What it offers | How SPN uses it |
|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 185,700 | Official | Official Agent Skills spec & examples (docx / pdf / pptx / xlsx) | `skills/spn/` aligns to its spec |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 112,099 | MIT | Production-grade engineering skills (TDD / Code Review / API design) | Advanced external link |
| [wshobson/agents](https://github.com/wshobson/agents) | 42,035 | MIT | Multi-harness plugin marketplace (Claude / Codex / Cursor / Copilot …) | Multi-harness reference |
| [littleben/awesomeAgentskills](https://github.com/littleben/awesomeAgentskills) | 192 | MIT | Bilingual (zh/en) Skill index, Chinese-friendly | Index / navigation |
| [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | 580 | MIT | 50+ vetted Skills curation | Index / navigation |

## 4. Security & documentation tools (SPN already uses some)

SPN's CI already runs: **gitleaks** (secret scan), **lychee** (dead-link check), **vale** (terminology consistency), **doc-lint** (hardcoded-number check). Below are advanced or complementary options:

| Project | Stars | License | What it does | Relation to SPN |
|---|---|---|---|---|
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | 35,329 | Apache-2.0 | 817 structured security Skills mapped to MITRE ATT&CK and 5 other frameworks | Advanced security reference (**too large to copy wholesale**) |
| [upstash/context7](https://github.com/upstash/context7) | 64,001 | MIT | MCP: gives Agents up-to-date docs, reducing stale-API hallucination | Echoes "don't hardcode numbers" |
| [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) | — | AGPL-3.0 | Scans git history for leaked secrets | Leak triage (optional) |

> Note: `trufflehog` is AGPL-3.0 — watch its strong copyleft if you deploy it server-side; local / CI use is generally fine.

## 5. Plugins & MCP (extend Agent capability)

| Project | Stars | License | What it does | How SPN uses it |
|---|---|---|---|---|
| [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community) | 4,799 | Apache-2.0 | Official community plugin marketplace (Claude Cowork / Claude Code) | SPN could publish as a plugin |
| [shaneholloman/mcp-knowledge-graph](https://github.com/shaneholloman/mcp-knowledge-graph) | 886 | MIT | Local knowledge-graph persistent memory | Echoes `personal/` cross-session memory idea |

## 6. License-conflict warnings (do NOT copy wholesale)

- [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) (144,376★, **GPL-3.0**): collects system prompts of many harnesses; fine to link for research, but **copying wholesale would contaminate SPN's MIT / CC license — forbidden**.
- `obra/superpowers`, `affaan-m/everything-claude-code`, etc. are far too large/complex for a non-technical audience; reference methodology only, don't merge.

## 7. How to propose a new entry

Follow `CONTRIBUTING.md`: a new entry must —

1. Be a repo **verified to exist** via `gh api` or an official source;
2. Note its stars and license;
3. State which SPN rule it strengthens and its integration tier (② link / ③ don't integrate).

Entries with **no license** or **unverified quality** (e.g. 0★ with no LICENSE file) are not accepted.
