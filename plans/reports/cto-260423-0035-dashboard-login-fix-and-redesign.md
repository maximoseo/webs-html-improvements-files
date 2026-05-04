# CTO Review — html-redesign-dashboard.maximo-seo.ai
**Date:** 2026-04-23 00:35 PT  •  **Branch:** main  •  **Audited by:** Claude Opus 4.7 (design) + plan for Sonnet 4.6 (execution)

---

## 0. Executive Summary

| Item | Finding |
|---|---|
| Login API | **Works**. `admin/[REDACTED_PASSWORD]` → 200 + JWT on both `/api/login` and `/api/auth/login`. |
| Auth enforcement | **Silently bypassed in production.** Unauthenticated GET `/` returns full 820KB dashboard. |
| User store | Local file `data/users.json` on Render (ephemeral, weak sha256) **→ will migrate to Supabase.** |
| Dual login endpoints | Race between `/api/login` (localStorage) + `/api/auth/login` (cookie). |
| Deployed stack | Custom Python `BaseHTTPRequestHandler` 4591 LOC. Next.js repo at `html-redesign-vps/` is **dead code**. |
| Design | Functional but inconsistent — mixed dark themes, unscaled typography, no design tokens, modal/expand UX fragile. |
| Scope to fix | Auth migration (Supabase) + security hardening + design system + login redesign + dashboard polish. |

## 1. Login Root Cause

### What the user experiences
User submits `admin / [REDACTED_PASSWORD]` at `/login` → appears to fail.

### What actually happens on the wire
```
POST /api/login   { username:"admin", password:"[REDACTED_PASSWORD]" }
→ 200 { ok:true, token:"eyJ…JWT…", user:"admin", role:"admin" }
   (NO Set-Cookie)

// login-page.html then fires-and-forgets:
POST /api/auth/login { user:"admin", password:"[REDACTED_PASSWORD]" }
→ 200 Set-Cookie: dash_auth=...; HttpOnly; SameSite=Lax; Max-Age=604800
    (but result is discarded in try/catch{})

window.location.href = '/';   // redirects before cookie lands reliably
```

### Why it fails (three concurrent bugs)
1. **Race condition** — The redirect to `/` happens before the second POST (`/api/auth/login`) completes, so the `dash_auth` cookie may not be set by the time the browser requests `/`. The `try { await } catch {}` pattern means any failure is swallowed silently.
2. **localStorage vs cookie confusion** — First endpoint saves JWT in localStorage; app code inconsistently checks cookie-only vs localStorage-only, depending on route.
3. **Auth gate silent-disable** — `server.py:2178-2180` only enforces auth if `DASHBOARD_USERS` env var is set on Render. It is not, so the middleware allows unauthenticated access to all pages. This masks the cookie-race bug (user lands on a "kind of" working dashboard where protected API calls 401 randomly).

### Supporting evidence (captured 2026-04-23 07:37 UTC)
```bash
$ curl -I https://html-redesign-dashboard.maximo-seo.ai/
HTTP/1.1 200 OK
x-render-origin-server: DashboardHTTP/1.0 Python/3.11.15

$ curl https://html-redesign-dashboard.maximo-seo.ai/ | wc -c
820962    # Full dashboard served to anonymous user

$ curl -X POST .../api/login -d '{"username":"admin","password":"[REDACTED_PASSWORD]"}'
{"ok":true,"user":"admin","role":"admin","token":"eyJ..."}   # Login API works
```

## 2. The Fix — Three Layers

### Layer A — Supabase-backed user store (per your direction)

Move credentials & users from `data/users.json` into Supabase. Two viable paths:

#### Path A1 (Recommended) — Supabase Auth as source of truth
- Seed admin user in Supabase Auth (email=`service@maximo-seo.com`, password=`[REDACTED_PASSWORD]`).
- Python backend calls `POST https://<proj>.supabase.co/auth/v1/token?grant_type=password` with email+password to verify credentials.
- On success, Supabase returns an access_token (Supabase JWT). Python verifies signature with Supabase JWKS (or trusts it and immediately re-issues its own session JWT tied to the Supabase user id).
- Dashboard uses existing `dash_auth` cookie for session (unchanged UX), but the cookie's underlying identity claim is a Supabase user id.
- Future: free password reset, email confirmation, MFA, Google OAuth — all toggled in Supabase dashboard.

**Schema addition** (optional, for role metadata and audit):
```sql
create table if not exists public.dashboard_users (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  role text not null default 'viewer' check (role in ('admin','editor','viewer')),
  display_name text,
  last_login timestamptz,
  created_at timestamptz not null default now()
);

-- RLS: users can read own row; service role full access
alter table public.dashboard_users enable row level security;
create policy "self_read" on public.dashboard_users for select using (auth.uid() = id);
create policy "service_full" on public.dashboard_users for all to service_role using (true);
```

#### Path A2 (Lighter) — Custom `users` table with bcrypt
- Create `public.dashboard_users` with `password_hash` (bcrypt/argon2, NOT sha256).
- Python backend queries via service-role key: `SELECT id,role,password_hash FROM dashboard_users WHERE username=?`.
- Verify with bcrypt. Issue `dash_auth` cookie as today.
- Cheaper change but reinvents password-reset, MFA, OAuth.

**Recommendation: Path A1.** Lower long-term cost. See `plans/260423-0035-dashboard-login-fix-and-redesign/phase-01-supabase-auth-migration.md`.

### Layer B — Server-side auth hardening (ship today)

Patch `server.py` and `login-page.html` to eliminate race + silent-disable:

```python
# server.py — replace lines 2177-2180
_auth_enforced = _dashboard_auth_enabled()           # users.json OR env OR supabase cfg
if _auth_enforced and not _stage8_check_auth(self, parsed):
    return
```

```python
# server.py — update `_stage8_login` to ALWAYS be the canonical entrypoint
# and make /api/login an alias that returns the same response shape WITH the cookie.
```

```html
<!-- login-page.html — collapse two calls into one -->
async function doLogin(){
  ...
  const r = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type':'application/json' },
    credentials: 'same-origin',            // explicit — ensures cookie captured
    body: JSON.stringify({ user:u, password:p })
  });
  const d = await r.json();
  if (!r.ok || !d.ok) { show(d.error || 'Invalid credentials'); return; }
  localStorage.setItem('dashboard_token', d.jwt || d.token);   // for fetch() Bearer calls
  // Wait one animation frame so Set-Cookie is committed before navigation
  requestAnimationFrame(() => location.replace(new URLSearchParams(location.search).get('next') || '/'));
}
```

### Layer C — Session persistence + logout

- `/` and all `/api/*` (except `/api/health`, `/api/auth/*`, `/api/login`) gated by `_stage8_check_auth`.
- `/api/auth/logout` clears cookie + returns 200; front-end clears localStorage.
- On 401 from any XHR, redirect client to `/login?next=${pathname}` (Axios-style interceptor in the dashboard shell — currently missing).

## 3. Code Review Findings

Severity key: **C** = critical, **H** = high, **M** = medium, **L** = low.

### Backend (`webs-html-improvements-files-clean/server.py`, 4591 LOC)

| Sev | Issue | Location | Fix |
|---|---|---|---|
| C | SHA-256 password hashing (no salt, fast, GPU-friendly) | `_dashboard_validate_credentials` | Move to Supabase Auth or bcrypt/argon2. |
| C | Auth gate silently disabled if `DASHBOARD_USERS` empty | L2178 | Enforce whenever `_dashboard_auth_enabled()`. |
| C | `_JWT_SECRET_KEY` defaults to hard-coded string | L268 | Require env; refuse to boot if missing in prod. |
| H | Dual login endpoints with divergent cookie behavior | L199, L270 | Unify under `/api/auth/login`. |
| H | `users.json` on ephemeral disk → lost on Render redeploy | L267 | Supabase-backed users. |
| H | `open(_USERS_JSON_PATH, 'w')` without atomic write lock across workers | L282 | Use single-process lock or Supabase (preferred). |
| H | No rate-limiting on `/api/login` or `/api/auth/login` | — | Add token-bucket per IP (existing `_R2_RATE_BUCKETS` pattern). |
| H | `_STAGE8_LOGIN_HTML` is hardcoded Hebrew `<html lang="he" dir="rtl">` fallback | L220 | Fix lang/dir, or remove the fallback. |
| M | 4591-line monolith → unmaintainable; violates 200-LOC rule | file-wide | Split into modules: `auth.py`, `radar.py`, `workflow.py`, `prompt.py`, `web.py`. |
| M | `handler.headers.get('X-User','anon')` — no server-side binding | L2169 | Derive from validated token. |
| M | CSP allows `'unsafe-inline'` + `'unsafe-eval'` + 3 unpinned CDNs | default policy | Tighten: pin to specific CDN hashes, drop `unsafe-eval`. |
| M | No HTTPS-only cookie flag (`Secure`) on `dash_auth` | L215 | Add `Secure` when behind Cloudflare. |
| M | No CSRF protection on state-changing POSTs (SameSite=Lax helps but POST JSON from other origins still hits) | all `/api/*` POST | Add CSRF double-submit token or require custom header. |
| L | HEAD returns 501 (framework default) | `BaseHTTPRequestHandler` | Implement `do_HEAD = do_GET` stub for health-checkers. |
| L | `reactStrictMode` turned off in unused Next.js repo | `next.config.mjs` | Delete unused Next.js repo OR adopt it (see §6). |

### Front-end (`login-page.html` + `index.html`, 15,659 LOC)

| Sev | Issue | Fix |
|---|---|---|
| C | `index.html` is a **15,659-line single file** with inline `<style>`/`<script>` | Split: `shell.html`, `styles/tokens.css`, `styles/components.css`, `js/router.js`, `js/auth.js`, `js/prompt-studio.js`, `js/keyword-research.js`, `js/radar.js`. |
| H | No central auth interceptor on `fetch()` — each feature handles 401 itself | Create `js/api.js` with `authedFetch()` that auto-redirects on 401. |
| H | `localStorage.setItem('dashboard_token', d.token)` — token exposed to any XSS | With cookie-based session + fetch using `credentials: 'same-origin'`, drop localStorage token. |
| H | No route-level guard before render — the full dashboard is sent to anonymous users | Server-side gate (Layer B fix). |
| M | No design tokens; colors/spacing hard-coded throughout | Introduce CSS custom properties (§4). |
| M | Modal/popup stacking uses z-index arithmetic (30, 50, 9999) | Single `--z-modal`, `--z-toast` scale. |
| M | Expand/collapse sections use `max-height` animation — content clips below viewport | Switch to flex + `overflow:auto` panels, or use `<details>` native. |
| L | No `prefers-reduced-motion` handling | Gate animations. |

## 4. Design / UX Review (Opus-led)

### Global problems
1. **No design tokens.** Hex codes duplicated across the file. Mixing `#0a0a0f`, `#0b0d12`, `#0a0a0a` as "background."
2. **Typography unscaled.** Font-size values: `.75rem, .8, .82, .85, .88, .9, .95, 1, 1.05, 1.1rem`. No systematic scale.
3. **Spacing arbitrary.** Padding values 6/8/10/11/12/14/16/18/20/24/28/32/40 intermixed.
4. **Button hierarchy unclear** — primary/secondary/ghost styles visually similar; destructive and neutral actions often same size.
5. **RTL/LTR mixed** — the Stage-8 fallback login is RTL Hebrew; production page is LTR English → confusing if one ever leaks.
6. **Main nav** — overflows on laptop-height screens; sections collapse unpredictably when Prompt Studio opens.
7. **Prompt Studio modal** — no sticky action bar; Deploy/Save buttons disappear when content is long.
8. **Keyword Research** — table row heights inconsistent; action buttons not aligned to right edge on narrow screens.
9. **Expand/collapse** — large sections push important actions off-screen; user has to scroll back up to find Deploy.
10. **Empty/loading states** — mostly missing; user sees blank panels during fetches.

### Proposed design tokens
```css
:root {
  /* Color — dark mode primary */
  --bg-0: #09090b;   /* app background */
  --bg-1: #121218;   /* surface / card */
  --bg-2: #1a1a22;   /* elevated */
  --line:  #27272f;  /* hairline */
  --line-strong: #3a3a45;

  --fg-1: #f4f4f5;   /* primary text */
  --fg-2: #a1a1aa;   /* secondary */
  --fg-3: #71717a;   /* tertiary / meta */

  --accent: #7c3aed;         /* brand purple */
  --accent-hover: #8b5cf6;
  --accent-soft: rgba(124,58,237,.12);
  --success: #10b981;
  --warn:    #f59e0b;
  --danger:  #ef4444;

  /* Typography */
  --fs-xs: .75rem;   /* 12 */
  --fs-sm: .875rem;  /* 14 */
  --fs-md: 1rem;     /* 16 */
  --fs-lg: 1.125rem; /* 18 */
  --fs-xl: 1.25rem;  /* 20 */
  --fs-2xl: 1.5rem;  /* 24 */
  --lh-tight: 1.25;
  --lh-normal: 1.5;

  /* Spacing — 4px base */
  --s-1: .25rem;  --s-2: .5rem;   --s-3: .75rem;
  --s-4: 1rem;    --s-5: 1.25rem; --s-6: 1.5rem;
  --s-8: 2rem;    --s-10: 2.5rem; --s-12: 3rem;

  /* Radii */
  --r-sm: 6px; --r-md: 10px; --r-lg: 14px; --r-xl: 20px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,.4);
  --shadow-md: 0 6px 16px rgba(0,0,0,.5);
  --shadow-lg: 0 20px 60px rgba(0,0,0,.55);

  /* Motion */
  --ease-out: cubic-bezier(.22,.61,.36,1);
  --dur-fast: 120ms;
  --dur-base: 200ms;

  /* Z-scale */
  --z-nav: 10; --z-dropdown: 30; --z-modal: 100; --z-toast: 200;
}
```

### Login page redesign (spec)
- Two-column: left hero (value prop, feature bullets), right form card. Collapses to single column `<900px`.
- Single `email` field (shifts from `username` once Supabase Auth migration ships).
- Error panel pinned above form; success panel inline.
- CTA button: full-width, 44px min-height, loading state with spinner + disabled prev state.
- "Continue with Google" below the primary form (Supabase OAuth provider). Divider `or`.
- Forgot password → inline reveal (no modal) with single email input.
- Hover states, focus rings (`--accent` 2px outline + 1px offset), reduced-motion friendly.

### Prompt Studio redesign (spec)
- Modal replaced by **full-screen workspace** (route: `/prompt-studio`) — escapes modal scroll traps.
- Top bar: `← Back | Title | status chip (draft/ready/deployed) | Save | Deploy | •••`  (sticky).
- 3-panel layout: left = prompt tree/history, center = editor, right = preview.
- Preview is iframe sandbox with device toggle (Mobile / Tablet / Desktop) and a "Copy URL" button for the rebuilt HTML on GitHub raw.
- Comments panel collapsible on the right; resolved comments auto-hidden.

### Keyword Research redesign (spec)
- Filter bar sticky at top with 4 pills: domain / intent / volume / status.
- Results as a virtualized table (>1000 rows without lag) — use CSS container queries for card mode on narrow widths.
- Row-level actions menu (`⋮`) collapses into a popover at `<1024px`.
- Batch-select header with "Deploy selected" / "Export CSV" / "Add to prompt".

### Main nav redesign (spec)
- Horizontal top bar with 5–7 primary entries max; overflow collapses into a `⋯` menu.
- Logo (left) + sections (center, tab-style) + user menu (right with avatar + dropdown for Logout/Settings/API keys).
- Height fixed at 56px desktop / 48px mobile; contents use `--s-4` gap.
- Active tab has 2px `--accent` underline, 150ms slide.

## 5. Future Features — Prioritized Roadmap

### P0 — Ship within next sprint
- **F1. Supabase Auth migration** — primary fix (§2 Layer A1).
- **F2. Login hardening + design** (§2 Layer B + §4 login spec).
- **F3. Single-file → module split** for `index.html` + `server.py` (top 3 modules: auth, prompt-studio, keyword-research).
- **F4. Auth interceptor in fetch wrapper** — redirects on 401.

### P1 — Near-term (2–4 weeks)
- **F5. Role-based access (admin/editor/viewer)** — fully wired to Supabase `dashboard_users.role`.
- **F6. Audit log page** — uses existing `r5.audit_log` but surfaces in UI with filters/export.
- **F7. Version history for Prompt Studio deliverables** — already partially in backend (`revisions.ts` in Next repo); bring forward.
- **F8. Device preview in Prompt Studio** (mobile/tablet/desktop iframe toggle).
- **F9. Diff viewer for template revisions** (before/after HTML side-by-side with syntax highlighting).
- **F10. Keyword batch export** (CSV + JSON + direct n8n workflow push).
- **F11. n8n deploy confirmation + rollback** — snapshot before update, 1-click revert.

### P2 — Mid-term (1–2 months)
- **F12. Comments/collaboration** — existing `/api/comments` → surface inline + email/slack notify.
- **F13. Daily Skills Radar dashboard view** — currently email-only; bring to UI with charts (recharts already a dep).
- **F14. Agent run tracer** — for each Prompt Studio generation, show which model, latency, token spend, cost.
- **F15. Template quality scoring** — wire the existing validator (`lib/validator/*` in Next repo) to show score + top 3 issues.
- **F16. Per-domain dashboard** (dtapet/hondabike/galoz/jacknows): quick-switch domain context, recent deploys, last error.
- **F17. WordPress sync preview** — dry-run preview for HTML → WP REST API pushes.

### P3 — Strategic (2–4 months)
- **F18. Multi-tenant workspaces** (Supabase RLS) — per client/agency.
- **F19. Embeddings + semantic search over skills/prompts** — already have `.claude/skills` tree; index with pgvector.
- **F20. Bring-your-own model** — OpenRouter key per user; cost center reporting.
- **F21. Slack app** — deploy/approve/comment on templates from Slack.
- **F22. Accessibility scoring gate** — block deploys with WCAG AA failures.
- **F23. LLM evaluations dashboard** — track quality over time; A/B prompts.

## 6. Repo Hygiene — Dead Code Decision

The Next.js repo at `C:/Users/seoadmin/html-redesign-vps/` (Next 14, Supabase SSR, TypeScript, Vitest) is NOT deployed. Options:

- **Option R1 (recommended):** Archive it. Keep as reference (some lib files — `validator/*`, `revisions.ts`, `pipeline-progress.ts` — contain useful code worth porting).
- **Option R2:** Revive it as the canonical front-end; proxy API calls to the Python backend (which would become headless). 6–8 week effort.

Marking R1 for now. We'll cherry-pick good modules during §5 F7/F15.

## 7. Verification Plan

| # | Test | Pass criterion |
|---|---|---|
| V1 | `curl -X POST .../api/auth/login` with admin creds | 200, body `ok:true`, `Set-Cookie: dash_auth=...` present |
| V2 | `curl https://.../` without cookie | 302 → `/login?next=/` (after §2 Layer B fix) |
| V3 | Login in browser, hard-refresh `/` | Dashboard loads; no 401 in console |
| V4 | Logout, refresh `/` | Redirect to `/login` |
| V5 | 6 bad passwords in 60s | 429 rate-limited |
| V6 | `/api/kwr/*` protected routes | 401 when no cookie |
| V7 | Responsive smoke: 360 / 768 / 1024 / 1440 / 1920 | No overlap, no horizontal scroll, CTA visible |
| V8 | Lighthouse perf `/login` | ≥ 90 perf, ≥ 95 a11y |
| V9 | `npm run test` in any repo touched | All green |
| V10 | Supabase Auth flow end-to-end | Admin logs in; Google OAuth one-click; reset-password email delivered |

## 8. Unresolved Questions

1. **Supabase project ID** for this domain — confirm which Supabase project ( `supabase_comments_config()` uses envs but the URL isn't committed). Need this to seed admin user. → **Please provide `SUPABASE_URL` + service-role key (or paste current Render env settings).**
2. **Existing user list** — is there anyone beyond `admin`? If yes, provide email list so migration seeds them.
3. **RTL/Hebrew requirement** — the Stage-8 fallback login is Hebrew. Is Hebrew a first-class requirement for the dashboard UI, or English-only is fine?
4. **OAuth providers** — enable Google? Microsoft? Magic-link email only?
5. **Session TTL** — currently 7 days. Keep, or switch to sliding 24h + refresh?
6. **Logout destination** — `/login` (current) or a branded landing page?
7. **Next.js revival** (R2) — is the user open to this later, or commit to Python backend + vanilla HTML long-term?

---

**See also:**
- `plans/260423-0035-dashboard-login-fix-and-redesign/plan.md` — phase breakdown
- `plans/260423-0035-dashboard-login-fix-and-redesign/phase-01-supabase-auth-migration.md`
- `plans/260423-0035-dashboard-login-fix-and-redesign/phase-02-server-auth-hardening.md`
- `plans/260423-0035-dashboard-login-fix-and-redesign/phase-03-design-system-and-login-redesign.md`
- `plans/260423-0035-dashboard-login-fix-and-redesign/phase-04-dashboard-modularization-and-ux.md`
- `plans/260423-0035-dashboard-login-fix-and-redesign/phase-05-verification-and-deploy.md`
- `plans/260423-0035-dashboard-login-fix-and-redesign/phase-06-future-features-backlog.md`
