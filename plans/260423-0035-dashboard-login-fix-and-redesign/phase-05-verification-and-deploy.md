# Phase 05 — Verification + Deploy

## Overview
- **Priority:** P0 gate before merge
- **Status:** pending

## Pre-deploy checklist
- [ ] Phase 01 applied + Supabase seeded.
- [ ] Phase 02 applied (gate, unify, secret, rate-limit, HEAD, Secure cookie).
- [ ] Phase 03 login redesign live.
- [ ] Phase 04 module split at least for tokens + nav + authedFetch.

## Env vars (Render dashboard)
| Key | Value source | Required |
|---|---|---|
| `SUPABASE_URL` | Supabase project settings | ✅ |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase API settings | ✅ |
| `SUPABASE_ANON_KEY` | Supabase API settings | ✅ |
| `DASHBOARD_JWT_SECRET` | `openssl rand -hex 32` | ✅ |
| `DASHBOARD_AUTH_SECRET` | `openssl rand -hex 32` | ✅ |
| `DASHBOARD_USER` | `admin` | ✅ (break-glass only) |
| `DASHBOARD_PASSWORD` | strong password | ✅ (break-glass only) |
| `OPENROUTER_API_KEY` | existing | ✅ |
| `N8N_API_KEY` | existing | ✅ |
| `GITHUB_TOKEN` | existing | ✅ |
| `RENDER` | `true` | auto by Render |

## Deploy
1. Commit on `main` → Render auto-deploys.
2. Watch Render logs for `_mu_init_users` skipping (users.json ignored because Supabase is primary).
3. Smoke-test V1–V10 (master report §7).

## Verification tests (reuse master report §7)
```bash
# V1 — login API
curl -sS -X POST https://html-redesign-dashboard.maximo-seo.ai/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"service@maximo-seo.com","password":"Maximo2025!"}' \
  -D - | grep -E "Set-Cookie|HTTP"

# V2 — gate enforced
curl -sS -I https://html-redesign-dashboard.maximo-seo.ai/ | grep -E "HTTP|Location"
# Expect: 302, Location: /login?next=/

# V5 — rate limit
for i in 1 2 3 4 5 6 7 8 9 10 11; do
  curl -sS -X POST https://html-redesign-dashboard.maximo-seo.ai/api/auth/login \
    -H 'Content-Type: application/json' -d '{"email":"a@b.c","password":"bad"}' -w '%{http_code}\n' -o /dev/null
done
# Expect: last 1-2 return 429
```

## Rollback plan
- Previous release tag preserved by Render (1-click revert).
- Break-glass admin env var `DASHBOARD_USER/PASSWORD` still honored by fallback path.
- Feature flag: `DASHBOARD_AUTH_BACKEND=supabase|local` for A/B.

## Todo
- [ ] Seed Supabase admin.
- [ ] Set all envs on Render.
- [ ] Commit + push.
- [ ] Run V1–V10.
- [ ] Announce in internal Slack/email.
- [ ] Monitor logs 24h post-deploy.

## Success criteria
- All V tests pass.
- No 5xx in 24h.
- Login latency p50 < 500ms (Supabase round-trip + cookie set).
