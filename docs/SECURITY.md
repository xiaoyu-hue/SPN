# Security Policy (SECURITY)

This project itself is a **documentation set of AI collaboration rules and prompts**; it contains no executable runtime service. But precisely because its theme is "security boundaries" and "pre-ship self-checks," we take the **safety of its advisory content** just as seriously.

---

## 1. What to report

If you find any of the following, responsible disclosure is welcome:

1. **A security flaw in the rules themselves** — e.g. a suggestion that, in practice, would lead to key leakage, permission misconfiguration, or data exposure.
2. **An incorrect command / example in the references** — e.g. the SQL / curl / grep examples in `references/02` no longer apply to the current server version and could mislead readers.
3. **Severely outdated cited data** — e.g. security-incident statistics, platform free-tier quotas that now diverge greatly from reality.

> Note: this repo is **not** the security contact channel for the app you built with AI.
> If your own project has a vulnerability, use your own project's / hosting platform's security process.

---

## 2. How to report

- **Preferred**: submit a **Private Security Advisory** in the repo (GitHub → Security → Report a vulnerability).
- **Alternative**: open a normal issue and clearly mark it "security-related; please don't post sensitive details in public comments."

Please include if possible:

- The file and section where the problem is
- Steps to reproduce or a specific description
- Your suggested fix direction (optional)

We will give an initial response within **7 business days** of receiving it.

---

## 3. Security best practices (for users)

The red lines this repo repeats — please follow them:

- Don't commit `.env`, keys, certificates, or tokens to any repo
- Don't put `service_role` / `sk_live` / private keys into frontend code or build artifacts
- Authorization can't live only in the frontend (hiding a button is not authorization)
- Before shipping, attack yourself once per `references/02`

---

## 4. Dependency and secret scanning

It is recommended to enable (free) in the repo **Settings → Code security**:

- **Secret scanning**
- **Dependency alerts**
- **Dependabot**

The repo's root `.github/workflows/doc-lint.yml` also checks on every push whether any suspicious hardcoded sensitive numbers have leaked into the docs.
