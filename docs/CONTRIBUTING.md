# Contributing Guide (CONTRIBUTING)

Thanks for wanting to make SPN better. This guide explains the repo's structure and boundaries, so we don't accidentally drift into two contradictory sets of rules.

---

## 1. The repo's two-layer structure (read this first)

```
SPN/
├── AGENTS.md        ← universal rules, for everyone (what the AI actually loads)
├── SKILL.md         ← skill entry point / full documentation
├── references/      ← universal rules (4 docs)
└── personal/        ← the author's own layer, ⚠️ NOT part of the universal rules
```

- **Universal layer** (`AGENTS.md` / `SKILL.md` / `references/`): for everyone; should stay tech-stack-agnostic and free of "personal context."
- **Personal layer** (`personal/`): holds only context that is true *for that author* (their projects, their tech stack, their to-dos). Skip it for general tasks.

---

## 2. The only defense line: promote rules upward

> **Any rule that holds for a different person too must be written into the universal layer at the root, not into `personal/`.**

If we skip this, the two layers overlap and we end up with two contradictory rule sets. If you contribute a new rule, first judge whether it's universal:

- Universal → add to `AGENTS.md` (or the relevant `references/` doc)
- True only for one person → put it in `personal/`, don't pollute the universal layer

---

## 3. How to add a new rule

The repo's own principles apply here too:

1. **Add one per real pitfall; don't pre-stock.** Each rule should map to a class of real problem that actually happened, not "sounds reasonable."
2. **Before adding, ask whether it can merge with an existing item.** Avoid fragmentation.
3. **Write into `AGENTS.md` in a tone the AI can load and execute** (orders to the AI); `references/` may use a human-facing explanatory tone.
4. **Changes touching security, authorization, or red lines: open an issue first to align direction**, then submit a PR.
5. **Don't hardcode numbers**: numbers that change with code (test counts, version numbers, item counts) use relative descriptions and stay in sync.

---

## 4. Content de-duplication convention

The same passage (e.g. the three real cases, the pre-done self-check five) should keep **one authoritative narrative**:

- The full narrative of the three cases → only in `references/01-协作哲学与判断归属.md`
- Pre-done self-check / honest reporting → authoritative in `AGENTS.md`; `SKILL.md` and `references/04` link or point to it
- When other files mention it, **link to it**, don't re-copy the whole passage

---

## 5. License layering

- Code (scripts, CI config) → **MIT** (`LICENSE`)
- Documentation (rules, prompts, references) → **CC BY 4.0** (`LICENSE-DOCS.md`)

By contributing, you agree your contribution is published under the same layered license, with appropriate attribution to the original author.

---

## 6. Translation

All four references, plus `AGENTS.md`, `SKILL.md`, `SECURITY.md`, and `CONTRIBUTING.md`, now have English versions under `docs/`. Translations should preserve the original style: plain-language-first, bracket-explained jargon, honest disclosure.

---

## 7. Pre-submit self-check

- [ ] The change lands in the correct layer (universal / personal)
- [ ] No passage is duplicated across files
- [ ] No hardcoded numbers in the docs (or labeled "as of version X")
- [ ] If it touches a security red line, an issue was opened first to align
- [ ] The PR description states: what you did, why, expected effect
