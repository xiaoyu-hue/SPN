# Documentation & Version Sync Spec (DOC SYNC)

> Purpose: an **execution checklist** to keep "what the docs say" consistent with "what the code actually does" after code / CI / feature changes.
> Pairs with the Decision Review Checklist (DECISION_REVIEW, pre-decision questions) and decision records / CHANGELOG (post-decision沉淀).
> This template is de-project-ified and applies to any project (any language, any framework).
>
> **Single Source of Truth principle**:
> - The version number's single source of truth is the **version metadata** (e.g. `package.json` / `pyproject.toml` / `VERSION` / git tag); all other docs derive from it.
> - Counts like test numbers / file counts have the **actual test / build output** as their single source of truth.
> - Feature / architecture descriptions have the **code implementation** as their single source of truth; docs must not exceed the implementation.

---

## 1. Trigger conditions (any one triggers a sync)

- [ ] Feature added / changed / removed
- [ ] Security or CI flow change (scanning, gate, workflow)
- [ ] Dependency change (added / removed / upgraded)
- [ ] Release (bump version + tag + Release)
- [ ] New doc / decision record added

## 2. Sync checklist (check each item)

### A. Version number (single source of truth: version metadata)

| Location | Action | How to verify |
|----------|--------|---------------|
| Version metadata file (e.g. `package.json` / `pyproject.toml`) | bump version | — |
| Lockfile (e.g. `package-lock.json` / `poetry.lock`) | sync version | grep |
| `CHANGELOG.md` | new version entry ("Unreleased" → released) | grep |
| Requirements / design docs (e.g. PRD / ARCHITECTURE) | version header + status line + version history table | grep |
| `README.md` | version statement / badge | grep |
| Author / project statement doc | current version narrative | grep |
| Release + tag | consistent with version metadata | confirm |

### B. Numbers & facts (single source of truth: actual output)

| Data | True source | Where it must be synced |
|------|-------------|--------------------------|
| Test count / test file count | test command output (e.g. `npm test` / `pytest`) | README table, requirements doc acceptance section |
| E2E case count | E2E test command output | README, requirements doc |
| Dependency count / vulnerability count | dependency / security scan output (e.g. `npm audit` / `pip-audit` / OSV) | README acknowledgements, security section |
| Dependency list (added / removed / upgraded) | version metadata file | README acknowledgements |
| Feature / architecture description | code implementation | README, requirements doc, architecture doc, decision record |
| Branch protection / CI gate | repo settings + workflow file | README security section, CHANGELOG |
| Multi-language docs | the base-language version is authoritative (when you change the base-language doc, sync the others) | each language doc |

### C. Doc index

- [ ] Repo doc index (e.g. `README.md` or `docs/README.md`) registers the new doc
- [ ] Decision record index registers the new record
- [ ] Multi-language docs touched by this change are synced (check "N/A" if no other language exists)

## 3. Version number rules (SemVer)

| Change type | Version action | Example |
|-------------|----------------|---------|
| New user-visible feature | minor | X.Y.0 → X.(Y+1).0 |
| Bug fix / security fix | patch | X.Y.Z → X.Y.(Z+1) |
| Docs / CI / engineering only | patch (or no bump) | X.Y.Z → X.Y.(Z+1) |
| Breaking change | major | X.0.0 → (X+1).0.0 |

**Rule of thumb**: user-perceptible new thing → minor; fixed a bug → patch; just cleanup → patch or no bump. If unsure, run the three decision questions from the Decision Review Checklist first.

## 4. Pre-release verification (must run)

1. **Stale version check**: `grep -rn "old-version" --include="*.md" --include="*.json" .` → should return nothing, or only hits that are clearly historical (e.g. version history table, CHANGELOG past entries).
2. **Test count check**: run the full test suite; the output number matches what README claims (if not, fix README — never fake the number to match).
3. **Version consistency**: version metadata = lockfile = latest CHANGELOG entry = doc headers = tag.
4. **CHANGELOG**: "Unreleased" entry promoted to released; content covers all user-visible changes this time.
5. **Multi-language check**: each language doc touched by this change is synced; if a language version is missing, create it or note "N/A".

## 5. Sync check template (fill before the release PR)

```markdown
## Sync Check (DOC SYNC CHECK)

- New version: ____ (version metadata is the single source of truth)
- Test count: ____ / test file count: ____ (actual output)
- [ ] version metadata + lockfile consistent
- [ ] CHANGELOG promoted to released
- [ ] doc version headers synced (requirements / architecture, all languages)
- [ ] README version statement / table numbers synced
- [ ] no stale version number (grep verified)
- [ ] doc index updated
- [ ] multi-language docs synced (language versions touched by this change updated)
- [ ] dependencies ↔ README acknowledgements consistent (added/removed deps reflected)
- [ ] Release / tag created and consistent with version number
```

## 6. Relationship to the rest of the system

- **AGENTS.md**: references this spec; a required check before release.
- **Decision Review Checklist (DECISION_REVIEW.md)**: before release, run the three decision questions first (especially "breaking change" and "version strategy").
- **CHANGELOG / decision records (ADR)**: record major changes first, then sync the descriptions this doc covers.
- **README / each doc**: the user-visible output of changes, synced with the version number.

> One line: **ask the version metadata for the version, the test output for the numbers, the code for the description — grep once before release, then ship.**
