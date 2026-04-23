# Deployment Checklist — Supabase Auth Ready
**Date:** 2026-04-23 00:53 PT
**Status:** All local/API tests green. Awaiting push + Render env var set.

## What's Done (locally)

- ✅ Supabase project confirmed (`wtpczvyupmavzrxisvcm`, ACTIVE_HEALTHY, PG 17.6).
- ✅ `public.dashboard_users` table created with RLS (self_read + service_full).
- ✅ Admin user in Supabase Auth: `service@maximo-seo.com` / `Supermario60@!` (id `4c990bfc-4576-4587-8fdc-3a48047b17f2`, role=admin, username=maximoseo).
- ✅ Wrong-ID row in `dashboard_users` removed; correct row seeded.
- ✅ `_supabase_verify_password` live-tested against real Supabase Auth — returns full user dict.
- ✅ `_dashboard_validate_credentials` accepts email OR username; Supabase-first, local fallback.
- ✅ Patched `server.py` + `login-page.html` compile clean; 5 local tests pass.
- ✅ `.env.local` + `.env.example` + strong `DASHBOARD_JWT_SECRET`/`DASHBOARD_AUTH_SECRET` (generated via `secrets.token_hex(32)`).
- ✅ `scripts/seed-supabase-admin.sh` — idempotent re-runnable seed script.

## Render env vars to set

Open Render dashboard → `html-improver` service → Environment. Add / update:

| Key | Value source |
|---|---|
| `SUPABASE_URL` | `https://wtpczvyupmavzrxisvcm.supabase.co` |
| `SUPABASE_ANON_KEY` | (from `.env.local`) |
| `SUPABASE_SERVICE_ROLE_KEY` | (from `.env.local`) |
| `DASHBOARD_JWT_SECRET` | (from `.env.local` — generated, 64 hex chars) |
| `DASHBOARD_AUTH_SECRET` | (from `.env.local` — generated, 64 hex chars) |
| `DASHBOARD_USER` | `maximoseo` |
| `DASHBOARD_PASSWORD` | `Supermario60@!` |

Do NOT set `DASHBOARD_USERS` (legacy var) — new logic uses `_dashboard_auth_enabled()`.

## Git push

```bash
cd C:/Users/seoadmin/webs-html-improvements-files-clean
git add server.py login-page.html tests/ scripts/ .gitignore .env.example \
        plans/ plan.md
git status
git commit -m "fix(auth): enforce gate, unify login, add supabase, rate-limit

- Auth gate now fires whenever any credential store is configured
  (was silently disabled when DASHBOARD_USERS env was missing).
- /api/login and /api/auth/login unified via _stage8_login — both
  set the dash_auth cookie atomically and return JWT in the body.
- login-page.html now makes a single fetch with credentials:same-origin
  and defers redirect to the next animation frame — eliminates the
  cookie-vs-navigation race.
- _dashboard_validate_credentials now tries Supabase password grant
  first (when email identifier is used); falls back to local users.json
  and break-glass env admin.
- Added per-IP rate limit (10 attempts, refill 1/10s) on login.
- Secure + HttpOnly + SameSite=Lax on dash_auth cookie.
- tests/test_auth_smoke.py covers login + rate limit + 401."
git push origin main
```

## Post-deploy verification

After Render finishes redeploying (~60–90s):

```bash
# Should now 302 redirect (gate enforced):
curl -sS -I https://html-redesign-dashboard.maximo-seo.ai/ | grep -E "HTTP|Location"

# Login via email:
curl -sS -X POST https://html-redesign-dashboard.maximo-seo.ai/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"service@maximo-seo.com","password":"Supermario60@!"}' \
  -D - | head -15

# Run the smoke suite:
python tests/test_auth_smoke.py https://html-redesign-dashboard.maximo-seo.ai
```

Expected:
- `/` → `HTTP/1.1 302 Found`, `Location: /login?next=/`
- `/api/auth/login` → `200 OK`, `Set-Cookie: dash_auth=...; Secure; HttpOnly`
- Smoke suite: `All smoke tests passed.`

## Rollback

If anything breaks:
1. Render dashboard → Deploys → click previous successful deploy → "Rollback to this deploy".
2. Or `git revert HEAD && git push`.

## Security follow-ups

1. The `DASHBOARD_PASSWORD` break-glass is fine for now but rotate after 30 days.
2. Enable Supabase Email confirmations + rate limiting in Auth settings (Dashboard → Auth → Rate Limits).
3. Optional: enable Supabase MFA (TOTP) for the admin account.

## Unresolved questions

1. Should `maximoseo` work as username in addition to the email at login? **Currently yes** via the env-var break-glass path when `DASHBOARD_USER=maximoseo` is set on Render.
2. Do we need a non-admin `maximoseo-editor` or `maximoseo-viewer` account seeded too?
3. Enable Google OAuth on Supabase? (Would then light up the "Continue with Google" button in the redesigned login page.)
