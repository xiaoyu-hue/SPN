# Install the SPN skill package

This directory is a **self-contained, installable** skill package for AI Agents. The core rules are fully inlined in `SKILL.md`; deep references are pinned to a version tag on GitHub, so being offline only affects "clicking through."

## What's inside

| File | Purpose | Read by |
|---|---|---|
| `SKILL.md` | The skill: metadata + complete rules | The Agent (loaded when it detects the `spn-en` skill) |
| `AGENTS.md` | Trimmed rules you can drop into a project root | The Agent (auto-loaded before work starts) |
| `INSTALL.md` | This file, for humans | You |

`SKILL.md` passes the official Agent Skills validator (`agentskills validate`).

## Pick one method

| Your situation | Use | Time |
|---|---|---|
| Your tool supports a skills directory (Claude Code, CodeBuddy, …) | **Method 1** | 1 min |
| Your tool reads `AGENTS.md` (Cursor, Codex, Aider, Windsurf, …) | **Method 2** | 30 s |
| You use Gemini CLI or GitHub Copilot | **Method 3** | 1 min |
| Not sure what your tool supports | **Method 2** (most portable) | 30 s |

---

## Method 1: install as an Agent Skill

Copy the whole `spn-en/` directory into your tool's skills directory. **Keep the directory name `spn-en`** — the spec requires `name` to match the parent directory, or validation fails.

**Claude Code**

```bash
# User level: applies to all projects
cp -r skills/spn-en ~/.claude/skills/spn-en

# Project level: travels with the repo, shared with the team
mkdir -p .claude/skills
cp -r skills/spn-en .claude/skills/spn-en
```

Windows PowerShell:

```powershell
Copy-Item -Recurse skills\spn-en "$env:USERPROFILE\.claude\skills\spn-en"
```

**CodeBuddy**

```bash
cp -r skills/spn-en ~/.codebuddy/skills/spn-en
```

**Other tools**: the path is usually `~/.<tool>/skills/` or `.<tool>/skills/` inside a project. Check that tool's documentation.

> Only want the Chinese package? Use [`skills/spn/`](../spn/INSTALL.md) instead.

## Method 2: use it as an AGENTS.md baseline (most portable)

`AGENTS.md` is the trimmed rule set the Agent actually loads. Drop it into **any project root**:

```bash
cp skills/spn-en/AGENTS.md your-project/AGENTS.md
```

Tools that read AGENTS.md (Cursor, Codex, Copilot, Gemini CLI, Aider, Windsurf, …) load it automatically before work begins.

> **Claude Code note**: when a `CLAUDE.md` exists, Claude Code does not read `AGENTS.md` by default. Keep `AGENTS.md` as the shared baseline and add a thin tool-specific file:
>
> ```bash
> echo "@AGENTS.md" > CLAUDE.md
> ```

## Method 3: Gemini CLI / GitHub Copilot dedicated files

These tools look for their own filenames. **Create a thin file that points at the rules — never keep a second copy.**

```bash
# Gemini CLI
cp skills/spn-en/AGENTS.md GEMINI.md

# GitHub Copilot
mkdir -p .github
cp skills/spn-en/AGENTS.md .github/copilot-instructions.md
```

---

## Verify it works

Open a fresh session and say:

> I don't code, but I want to build a web app with AI. Don't write code yet — follow the SPN rules.

**Three observable behaviors** — two or more mean it's active:

1. It first confirms the goal and "what done looks like" instead of writing code
2. When you hit unfamiliar jargon, it translates into plain language
3. On delete / deploy / pay, it stops and waits for your confirmation

If it just starts writing code, the rules weren't loaded — check that the files landed in the right place.

## Upgrade

The package version matches a repository tag (see `metadata.version` in `SKILL.md`). Upgrade by copying over:

```bash
cp -r skills/spn-en ~/.claude/skills/spn-en
```

To pin a specific version, download the repo snapshot for that tag from the Releases page rather than using `main`.

## Uninstall

Delete the directory. The package writes no global config, makes no network calls, and leaves nothing behind:

```bash
rm -rf ~/.claude/skills/spn-en
```

## FAQ

**Q: The `references/` links don't open.**
They are pinned to the release tag and need network access. All core rules are inlined in `SKILL.md`; offline only affects "clicking through."

**Q: Can I edit the rules?**
Yes — edit `AGENTS.md` / `references/` at the **repository root**, then sync into the package. CI enforces that the two copies stay identical (`doc-lint`). Editing the copy inside the package will fail CI.

**Q: Why does the bundled `AGENTS.md` start with a comment line?**
It's a "release snapshot" marker telling you to edit at the root. CI ignores that line when comparing.

## License

Everything in this package is provided under **CC BY 4.0** (Creative Commons Attribution 4.0 International), same as the repository. Free to use, redistribute, and modify with attribution. See `LICENSE-DOCS.md` at the repository root.
