# Pre-Ship Security Self-Check (English)

> Companion to `02-pre-launch-security-checklist.md`.
> For any project with a backend, database, or user login.
> **Why this list exists: permission errors are completely invisible in a demo.** A locked table and an open table render the exact same page — so you must attack yourself on purpose.

## Why you must do this

This isn't theoretical risk — it has happened at scale (all publicly reported; **exact counts, ratios and their verification dates are logged in `FACTS.md`, which CI checks for staleness**):

- **CVE-2025-48757**: scanning 1,645 AI-generated apps, 170 had Supabase tables readable/writable unauthenticated, exposing emails, addresses, third-party API keys
- **UpGuard survey**: ~16,000 Supabase-hosted projects with varying degrees of personal-data exposure — names, addresses, phones, and some passwords and auth tokens
- **RedAccess (2026-05)**: scanning ~380,000 publicly reachable AI-generated apps, ~5,000 leaking sensitive data
- **Wiz**: among orgs using such platforms, about one in five has at least one systemic vulnerability

**Same root cause every time: the AI optimizes for "the demo works," and the security boundary is the one part that produces no visible result.**

---

## 1. Database permissions (highest priority — do this first)

Examples use Supabase / Postgres. Adapt to your backend's equivalent.

### Check 1: which tables have RLS off
In the SQL editor:
```sql
select tablename from pg_tables
where schemaname = 'public' and not rowsecurity;
```
Any row returned = that table is currently world-readable and world-writable.

### Check 2: are existing policies fake?
```sql
select tablename, policyname, qual
from pg_policies where schemaname = 'public';
```
Watch for `qual` being `(true)` or not referencing `auth.uid()` at all — **that's as good as no lock.**
`auth.role() = 'authenticated'` also fails: it only verifies "logged in," not "is this your own data."

### Check 3: try it like an attacker
The project URL and anon key are readable right in the browser (the anon key is public by design, not a secret):
```bash
curl "https://YOUR-PROJECT.supabase.co/rest/v1/profiles?select=*" \
  -H "apikey: YOUR_ANON_KEY"
```
Getting data back while not logged in = you're leaking. An empty array or a permission error is what's correct.

### Correct写法 (correct写法)
```sql
alter table public.documents enable row level security;

create policy "Users read own docs" on public.documents
  for select to authenticated
  using ( (select auth.uid()) = user_id );
```
`auth.uid()` returns null for anonymous users, so they get zero rows. Wrapping with `(select auth.uid())` makes Postgres compute it once per query instead of per row.

### Four easy-to-miss points
1. **First table got a policy, the later ones didn't** — the most common failure
2. **anon role's grant not revoked** — adding a policy without revoking the grant leaves a write path
3. **`USING (true)`** — looks like permission, actually equals public
4. **Views and SECURITY DEFINER functions** — bypass the underlying table's RLS

---

## 2. Secret checks

Search your frontend build output:
```bash
grep -r "service_role\|sk_live\|AKIA[0-9A-Z]\{16\}" dist/ build/ .next/ 2>/dev/null
```
**Any hit is a serious problem.** An anon key in the frontend is normal (it's public); service_role there is fatal.

Also:
- `.env` must be in `.gitignore`, and **added before your first commit**
- A secret in git history can't be undone by deleting the line — it's still in history; you must **rotate** it
- Run `gitleaks detect` before pushing to a public repo
- Free on public GitHub: turn on **Secret Scanning** and **Dependabot**

---

## 3. Privilege-escalation test (you must do this yourself)

1. Register **two** accounts, A and B
2. Have A create a record
3. Have B try to read it — change the id in the request, change the URL param, whatever
4. **B can read it = permission misconfigured, go back**
5. Fully log out, then open a page that requires login directly — if it opens, the server isn't checking

Public audits show ~24% of AI-generated apps have reversed auth logic: anonymous visitors have full access while real users are blocked.

---

## 4. Other must-check items

| Item | How |
|---|---|
| Server-side validation | validate all input server-side, no SQL concatenation. The AI almost never adds this on its own — say it explicitly |
| Rate limiting | "money-burning" endpoints (signup, login, email, AI calls) must be rate-limited |
| CORS | lock to your own domain, no `*` |
| Dependency vulnerabilities | run `npm audit`. AI-generated projects almost never do |
| Error messages | don't return stack traces, SQL, or internal paths to the frontend |
| Backups | free tiers usually have no auto-backup — set an export plan and **verify it restores** |
| Logging | at least record failed logins and errors, or you'll only learn from users |

---

## 5. Free security scanners

| Tool | Finds | Free? |
|---|---|---|
| `npm audit` | dependency vulnerabilities | free, ships with Node |
| Gitleaks | secrets in git history | free, local |
| Semgrep | logic bugs (IDOR, injection) | free tier |
| Snyk Code | deps + code, flags "actually triggerable" bugs | free tier |
| GitHub Secret Scanning | secrets pushed to GitHub | free for public repos |
| GitHub Dependabot | dep auto-update + alerts | free |
| Supabase linter | RLS off / over-broad policy | free (Supabase only) |

**⚠️ Important limit**: these are **static** checks. They can't catch runtime logic like "user A reads user B's data" — that requires the E1 prompt in `04-prompt-library.md` to attack yourself, or dynamic tests.

---

## 6. Minimal experiment: six steps to learn full-stack boundaries

Don't build the whole app at once. A "login + message board" is enough:

1. Create table + enable RLS + write policy
2. Email login
3. After login, post and see your own
4. Deploy
5. **Register a second account, read the first account's data** ← most critical step
6. If you can read it = permission misconfigured, redo

**Step 5 is not optional.**

---

## 7. Hard rules to paste into AGENTS.md

1. Every table must enable RLS and have a policy; ban `USING (true)` pseudo-permissions
2. Secrets only server-side; stop immediately if service_role / sk_live appears in frontend code
3. Permission checks must be server-side; hiding a button is not permission
4. All input validated server-side; no SQL concatenation
5. Irreversible ops (drop table, change schema, ship, pay) must ask me first
6. Back up before schema changes; never let the AI write directly to the production DB

Precedent for rule 6: in July 2025, Replit's agent deleted a user's production database during a code freeze.

---

## 8. Non-coder friendly: let the AI run the checks for you (no terminal / no SQL)

> This section resolves a contradiction: this list asks you to run SQL / curl / grep, but the audience "can't read code." **You don't need to know how** — have the AI run them in your project environment and just read what it reports back.

Send this to your AI (replace the brackets):
```
I'm about to ship. Please self-check against this security list (my backend is [Supabase/Postgres, or yours]):
1. DB permissions: list tables without row-level security (RLS); check whether existing policies are fake (qual is true, or doesn't reference the user ID)
2. Attack yourself: can any data be read without logging in?
3. Secret check: are there service_role, sk_live, AWS keys, or similar in the build output / code that shouldn't be there?
4. Privilege test: if there's a login, simulate user B reading user A's data
5. Other: rate limiting, CORS, whether internal details leak to the frontend
For each: what you actually ran, what you saw, the conclusion (safe / problem), and how to fix a problem.
Don't fabricate results — if you didn't actually run something, say so.
```

The parts you only need to click (zero terminal):
- **Privilege test (Section 3)**: register two accounts, have B read A's data — all in the browser.
- **Read the AI's report**: after it runs SQL / curl / grep, just confirm it gave you the "what I ran / what I saw / conclusion" trio, and didn't brush you off with "looks fine."

> Same principle: **you judge, the AI does the work.** Security checks included — you don't need to know the commands, but you must see the results and make the call.

---

## 9. Adapting to other backends (Supabase / Neon / Cloudflare D1)

The SQL and commands here use Supabase / Postgres. Other backends differ in mechanism, but **the items to check are identical** (RLS equivalent, secrets never in frontend, privilege test, rate limiting). Tradeoffs of three common backends (quotas and prices change often — they're logged in `FACTS.md` with verification dates; re-check before relying on them):

| Option | Free quota | First wall you hit |
|---|---|---|
| **Supabase** | 2 active projects, 500MB DB, 50k MAU | auto-pauses after a week idle, manual resume |
| **Neon** | 100 projects, 0.5GB each | 0.5GB per branch, 20GB total cap; sleeps when idle but doesn't pause |
| **Cloudflare D1** | 5M reads / 100k writes per day | hard error (not slowdown) past the limit |

**Mainland China access**: Supabase and Cloudflare can be unstable there. For stable direct access you'd look at Tencent CloudBase, but its free trial is a one-time redemption code from Jan 2026, 3000 resource points/month with limited features, personal tier ¥19.9/month from then.

**So "free + hassle-free + stable in China" only satisfies two of three.** Which to pick is your call; the AI only gives the candidate list.
