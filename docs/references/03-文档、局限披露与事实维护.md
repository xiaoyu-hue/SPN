# Documentation, Limitation Disclosure & Fact Maintenance

> Core principle: **better to state boundaries clearly than to sound modest.**
> The pattern is — state first what you can't do, and only then will people trust what you can.
> Corollary — **every number you write in must always be accurate.** A stale number is worse than none.

---

## Zero. Solve the numbers problem first (the easiest part to go stale)

### Why this is a real problem

You'll want to write "573 tests" "v6.5.1" "192 timelines" in your README — these numbers are persuasive. But change the code and tests may become 601, the version rises to v6.6.0, timelines grow to 200.

**Once a number goes stale, "disclose limits honestly" becomes "disclose honestly… that we once were honest."** That hurts trust more than not writing it.

### But don't just stop writing numbers

Changing "573 tests" to "lots of tests" is a **regression** — a vague number carries no information; readers will just think you're being evasive. Honesty needs specificity; specificity carries cost.

### Correct approach: three categories

| Type | Example | What to do |
|---|---|---|
| **Structural fact** (rarely changes) | "data stored locally in browser" "zero runtime dependencies" "no payment loop" | **Write directly.** This is positioning, not quantity |
| **Process number** (may change every commit) | test count, version, item count, module count | **Don't hardcode.** See the three ways below |
| **External cited data** (others' research) | CVE numbers, statistics in a survey | **Keep but must label the verification date**, and remind to re-check |

### Three ways to write process numbers (rough to good)

**Way 1: relative description (least effort, recommended first)**

Replace precise numbers with "magnitude + trend"; persuasion is mostly preserved but it won't go stale:

| ❌ Hardcoded | ✅ Relative |
|---|---|
| 573 tests | tests have accumulated into the hundreds |
| v6.5.1 | iterated to the sixth major version |
| 11 modules | module count has grown into double digits |
| 192 timelines | nearly two hundred timelines |
| 7 sections · 8 themes | multiple sections and several themes |

**Key**: a relative description is still specific ("hundreds" is more specific than "many"), it just doesn't promise an exact value.

**Way 2: single source of truth (more rigorous)**

Define the number in **one place**; other docs reference it instead of each handwriting a copy.

```
PROJECT_FACTS.md        ← only true source: version, test count, item count
    ↓ reference
README.md              ← references the file above, doesn't repeat the numbers
```

When code changes, edit only `PROJECT_FACTS.md`.

**Way 3: auto-generated (least worry, but needs CI setup)**

- Version: read automatically from `package.json` or git tag
- Test count: CI writes it back to README after tests run
- Item count: count from the data file with a script

**⚠️ My advice**: if you already have a CI gate, start with "auto-read version"; don't go full automation at once — the config itself is maintenance cost. **Use Way 1 first; it's enough for a long time.**

### Hard rule for the AI

```
Don't hardcode in docs numbers that change with code (test counts, version numbers, item counts, module counts).
Use relative descriptions instead: "hundreds of tests" not "573 tests".
If you must give an exact value, label the date or say "as of version X".
If a code change affects any number in the docs, you must sync the update and call it out separately in your delivery report.
```

---

## 1. README skeleton

Write in this order; the first four blocks decide whether anyone reads further:

```
1. One-line positioning (what this is, who it's for)
2. 🔗 Live URL (a link they can try beats any description)
3. 🛠 Tech stack + test count + license (one line)
4. Quick start (try online / run locally)
5. The specific problem it wants to solve
6. Known limitations        ← cannot omit
7. What it's NOT for        ← cannot omit
8. Maintenance status (with update date)
9. Contact & feedback (what's accepted, what isn't)
```

---

## 2. How to write "what it can't do" (three sentence patterns)

### Pattern A: state the fact directly
> No cross-device auto-sync (manual backup import/export needed), no team collaboration, not a native app, browser data may be cleared

### Pattern B: reason first, then conclusion
> Although it uses cutting-edge tech (X25519 key agreement, per-message HKDF, Ed25519 signcryption), I'm just standing on giants' shoulders to realize my own idea — I'm not a cryptographer. All known limitations are written honestly in the README, nothing hidden.

### Pattern C: proactively prevent misreading
> To be honest, lest it be misread as an authority endorsement: the timeline was added mainly to make the page prettier; most of the lists in the toolbox and reading recommendations were recommended by the AI for me, and I haven't read them all myself. So the intent is personal use, not an "I read, used, and judged every item" expert list.

**Pattern C is the hardest yet most powerful: proactively tear down the trust others might give you that you shouldn't have.**

---

## 3. Writing examples by project type (copy-adapt)

### Local-first app (data in browser)
```
NOT FOR / Known limitations
- No cross-device auto-sync; switching devices needs manual export/import of backup
- Data lives in browser local storage; clearing browser data clears it too
- Not a native app; no system-level notifications
- Depends on a fairly recent Chrome / Edge / Safari
```

### Crypto / privacy project
```
⚠️ About [project name]
- Not professionally security-audited; not recommended for real sensitive use
- Author is not from a professional dev background; code was implemented with AI assistance
- Security discussion welcome, but that constitutes no guarantee
- Please don't use it for anything truly sensitive
```

### Template project with backend
```
NOT FOR / Known limitations
- Single-password auth, no multi-admin
- No CSRF protection
- Single-process file read/write; not suited for high concurrency
- No SSR / SEO
- Not suited for payment sites
⚠️ The default admin password is written in the README; be sure to change it before deploying
```

### Content-aggregation project
```
- Content hand-curated by the author (not full auto-scrape)
- Lists are mostly AI-recommended, not all personally tested
- Some external links depend on third-party availability
- Update frequency depends on the author's time
```

---

## 4. Maintenance status: how to write "I've slowed down"

```
Maintenance status (updated 2026-10): still maintained, but at a slower pace than before —
my main device broke; I'm updating from a backup device now, will resume once I buy a new one.
It hasn't been abandoned. If you plan to use it seriously, read the README first.
```

Three elements: **fact + reason + actual impact on the user.** Don't just say "been busy lately."

---

## 5. Write "what I won't take" clearly too

```
🙅 NOT taking
paid custom development, doing security audits for others, homework, "help me fix my code"
```

Writing this saves ~80% of future useless communication.

---

## 6. How to pick a license

Common approach: **code and documentation use different licenses.**

| License | Trait | When to pick |
|---|---|---|
| **MIT** | most permissive, almost no limits | want maximum adoption |
| **Apache-2.0** | permissive, but with patent clause, enterprise-friendly | enterprise scenarios, patent worries |
| **AGPL-3.0** | strongest copyleft, network services must open-source too | want to block "take it, tweak it, make a commercial service" (common for privacy projects) |
| **CC BY** | for docs, attribution only, commercial OK | want docs widely spread |
| **CC BY-NC** | for docs, no commercial use | don't want docs resold |
| **CC BY-NC-SA** | for docs, no commercial + share-alike | strictest doc license |

**Note**: GitHub's auto-recognized SPDX currently supports only 13 licenses; the CC family only recognizes CC0-1.0. So a repo using CC BY-NC shows no license badge in the sidebar (API returns `NOASSERTION`) — that's not an error; just state "LICENSE file is authoritative" in the README.

---

## 7. Prompt for having the AI write a README

```
Write a README for this project. Requirements:
1. Open with one line saying what it is and who it's for
2. Must include "Known Limitations" and "What it's NOT for" sections, written honestly, no sugarcoating
3. If some part is AI-recommended/generated rather than personally tested, label it clearly
4. Separate the live URL from the local-run instructions
5. Write the maintenance status truthfully, with an update date
6. Don't use words like "powerful" "revolutionary" "ultimate experience"
```
