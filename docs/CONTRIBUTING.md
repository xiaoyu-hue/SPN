# Contributing Guide (CONTRIBUTING)

Thanks for wanting to make SPN better. This guide explains the repo's structure and boundaries, so we don't accidentally drift into two contradictory sets of rules.

---

## 1. The repo's two-layer structure (read this first)

```
SPN/
├── AGENTS.md        ← universal rules, for everyone (what the AI actually loads)
├── SKILL.md         ← skill entry point / full documentation
├── references/      ← universal rules (6 docs)
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

- The full narrative of the three cases → only in `references/01-collaboration-philosophy.md`
- Pre-done self-check / honest reporting → authoritative in `AGENTS.md`; `SKILL.md` and `references/04` link or point to it
- When other files mention it, **link to it**, don't re-copy the whole passage

---

## 5. Change here → sync there (or CI turns red)

**The repository root is the single source of truth.** `docs/` (the English mirror) and
`skills/` (the installable packages) are **release copies**. Don't edit them directly —
your change will be overwritten, and worse, it will fork "what users install" from
"what the repository shows".

| You edited the source | Must be synced to | Who syncs it |
|---|---|---|
| `AGENTS.md` | `skills/spn/AGENTS.md` | **automatically** (`sync_snapshots.py`) |
| `docs/AGENTS.md` | `skills/spn-en/AGENTS.md` | **automatically** |
| `SKILL.md` | `skills/spn/SKILL.md` | **automatically** |
| `docs/SKILL.md` | `skills/spn-en/SKILL.md` | **automatically** |
| `references/01`–`08` (Chinese) | `docs/references/*` (English) | **manually** (it's a translation) |

One command handles everything automatic:

```bash
python3 scripts/sync_snapshots.py --apply   # write the copies
python3 scripts/sync_snapshots.py --check   # verify only; CI runs this every push
```

> The package-specific wording (version banner, "30-second version", the note above the
> reference table) lives in the `HEADER_*` / `SECTION_*` constants in
> `scripts/sync_snapshots.py`. **If you change a sentence it anchors on, the script fails
> loudly instead of silently skipping the replacement** — update the constant as told.

### What's in `scripts/`

| Script | What it does | When it runs |
|---|---|---|
| `release.py` | One-command release (dry-run by default; `--yes` actually writes and pushes) | manually, at release time |
| `sync_snapshots.py` | Source → release copies, plus consistency check | every push (CI) + release |
| `doc_lint.py` | Catches hardcoded numbers that will go stale | every push (CI) |
| `check_facts.py` | Flags registered facts in `FACTS.md` that are due for re-verification | every push (CI, non-blocking) |
| `check_links.py` | Relative links and anchors across the repo | every push + release |
| `run_tests.py` | Unit tests for `scripts/` | every push (CI, on three OSes) |
| `validate_skills.py` | Validates skill packages against the Agent Skills spec | every push (CI) |

**If you add functionality to `scripts/`, add tests too** — `AGENTS.md` rule 92 applies to
this repository as well. Any time-sensitive figure (survey numbers, platform quotas, prices)
belongs in `FACTS.md`, not scattered through the docs.

---

## 6. License layering

- Code (scripts, CI config) → **MIT** (`LICENSE`)
- Documentation (rules, prompts, references) → **CC BY 4.0** (`LICENSE-DOCS.md`)

By contributing, you agree your contribution is published under the same layered license, with appropriate attribution to the original author.

---

## 7. Translation

All references (01–08), plus `AGENTS.md`, `SKILL.md`, `SECURITY.md`, and `CONTRIBUTING.md`, now have English versions under `docs/`. Translations should preserve the original style: plain-language-first, bracket-explained jargon, honest disclosure.

---

## 8. Pre-submit self-check

Run these locally before pushing — much faster than waiting for red CI:

```bash
python3 scripts/run_tests.py                # unit tests for scripts/
python3 scripts/sync_snapshots.py --check   # are release copies in sync with the source?
python3 scripts/doc_lint.py                 # any hardcoded numbers that will go stale?
python3 scripts/check_links.py              # links and anchors
python3 scripts/check_facts.py              # any facts due for re-verification?
```

Checklist:

- [ ] The change lands in the correct layer (universal / personal)
- [ ] No passage is duplicated across files
- [ ] **Only source files were edited — not the release copies under `docs/` or `skills/`**
- [ ] `sync_snapshots.py --apply` was run (if `AGENTS.md` / `SKILL.md` changed)
- [ ] No hardcoded numbers; time-sensitive figures are registered in `FACTS.md`
- [ ] Changes to `scripts/` came with tests
- [ ] If it touches a security red line, an issue was opened first to align
- [ ] The PR description states: what you did, why, expected effect
