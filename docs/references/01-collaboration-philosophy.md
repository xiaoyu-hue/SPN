# Collaboration Philosophy & Who Decides (English)

> Companion to `01-collaboration-philosophy.md`. Translation kept in the same plain-language, no-jargon-first style as the original.

## 1. The core boundary

```
Human                            AI
propose the idea         ←→       translate the jargon
make the judgment        ←→       provide options
choose the approach      ←→       implement it
draw the boundaries      ←→       write the code
```

**The AI writes the code. You make the judgment.**

Why this line matters: the AI's capability grows far faster than your understanding. If you also hand over the judgment, you end up with something that runs but that you don't know why it runs — and when it breaks, you won't know how to fix it.

---

## 2. Three real judgments (from the author's actual projects)

### Judgment 1: shipping a project for the first time
- **What happened**: turn something viewable locally into something others can see
- **What the AI did**: recommended several static-hosting platforms
- **The human's call**: it gave a candidate list, not a command. The human picked the first platform; when the free quota ran out, set up a backup themselves
- **Reusable point**: **the AI lists options, the human chooses.** After choosing, "how to configure" goes back to the AI

### Judgment 2: can two visual styles be fused?
- **What happened**: wanted to combine two favorite styles
- **What the AI did**: said it couldn't guarantee they'd fuse
- **The human's call**: wanted it, so just tried. It worked — and became the visual基调 (the whole site's visual baseline)
- **Reusable point**: **"try before asking" is sometimes smoother than "ask before trying."** The test is the cost of undoing — changing visuals is nearly zero-cost; trying once beats arguing for an hour

### Judgment 3: drawing security boundaries for an encrypted chat app
- **What happened**: end-to-end encryption worked (X25519 / HKDF / Ed25519)
- **What the AI did**: smoothly wrote the crypto code
- **The human's call**: code ≠ a guarantee. The author isn't a cryptographer, so the two lines "not professionally security-audited" and "not recommended for truly sensitive scenarios" were **written into the README by the human**
- **Reusable point**: **capability ≠ a guarantee.** The AI can reach a certain level; whether you can be responsible for that level is a different matter

---

## 3. "Try before asking" vs. "ask before trying"

Not either/or — split by cost of undoing:

| Just try it (reversible, visible result) | Ask first (irreversible or involves others) |
|---|---|
| visual style, color, layout | deleting files, overwriting code |
| interaction feel, animation | database schema changes |
| copy, typesetting | shipping, publishing |
| small local changes | paying, subscription services |
| adding a candidate for A/B | anything touching others' data |

**One sentence: can it be undone with one click? If yes, try. If no, ask.**

---

## 4. The jargon-translation mechanism (the non-coder's core superpower)

This is the key move that lets someone who can't code make correct calls. Don't skip it.

**Flow:**
1. The AI gives a plan full of words you don't understand
2. **Stop. Don't approve.**
3. Tell it to translate: "explain it in plain language, no jargon"
4. After hearing it, ask: "what's the cost? what happens if I don't? are there other options?"
5. Only adopt it once you're clear in your head

**Key mindset: not understanding is not your fault — it failed to explain clearly.** Asking the AI to rephrase is its responsibility.

---

## 5. How to tell the AI is bullshitting you

| Signal | What it means |
|---|---|
| Gives only one option, no tradeoffs | it didn't really think about alternatives |
| Only agrees: "sure, works, no problem" without naming the cost | it's echoing you, not helping you decide |
| Full of jargon that's still confusing after translation | it may not be clear itself |
| Says "this is simple" but can't state the cost | be wary |
| Gives a fallback fix right after an error instead of finding the root cause | it's covering up the problem |
| Claims tests pass but won't paste the command output | demand the output |
| Mentions a library / API / config you've never seen | **demand an official docs link, verify on the spot** |

The last one is the most dangerous: **the AI will fabricate library names and APIs that look real.** Treat any unverified dependency as nonexistent.

**How to respond: just push back, no need to be polite.** Saying "I don't understand" isn't weakness — it's a signal that forces it to be clear.

---

## 6. Engineering discipline — you need it even if you can't code

Not understanding code doesn't mean you can skip discipline. These four things you can require without reading code:

1. **Tests** — after a change, there must be a way to confirm nothing broke
2. **ADR (Architecture Decision Record)** — for every major choice, note "why this, what was given up." It's your future memo
3. **CI gate** — let the machine intercept one step before you do
4. **Layered architecture** — so things don't drag each other down as they grow

**What you want isn't to understand the code — it's to understand "how will I know when it breaks."**

---

## 7. Honesty is a strategy

These are lines the author actually put in a public README, which paradoxically built more trust:

- "Most of the tool-box and book recommendations were suggested by AI; I haven't read them all myself"
- "The timeline was added mainly because it looks good on the page"
- "Not professionally security-audited" / "not recommended for truly sensitive scenarios"
- "My main device broke; I'm updating from a backup device, slower than before"
- "The default admin password is in the README — change it before you deploy"

**Pattern: state what you can't do first, and people will trust what you can do.**

---

## 8. From pure frontend to full-stack: a change of identity

If your app's data lives in the user's own browser, you can't touch it and aren't responsible for it.

The moment you add a backend and database, you go from **tool author** to **data custodian**. That's a promotion of responsibility, not just difficulty.

Three new responsibilities:

1. Others' data sits on a server you rent — you're responsible for its safety
2. Permission errors are invisible in a demo — you must attack yourself (see `02-pre-launch-security-checklist.md`)
3. The AI can write working code, but **you must draw the security boundary**
