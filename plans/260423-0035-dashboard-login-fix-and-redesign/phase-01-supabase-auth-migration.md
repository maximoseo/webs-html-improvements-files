# Phase 01 — Supabase Auth Migration

## Overview
- **Priority:** P0
- **Status:** pending
- Move login + user store from local `data/users.json` (sha256, ephemeral Render disk) to Supabase Auth.

## Context
- Production backend: `webs-html-improvements-files-clean/server.py` (Python `BaseHTTPRequestHandler`).
- Supabase is already wired for comments (`supabase_comments_config`, service-role key). Reuse the same env vars.
- User directive: "keep the login data and users in supabase account".

## Architecture
```
Browser ──POST /api/auth/login (user, password)──▶ Python server
                                                      │
                                                      ▼
                                  POST supabase.co/auth/v1/token?grant_type=password
                                  { email, password }
                                                      │
                                                      ▼
                                  200 { access_token, user: { id, email, user_metadata } }
                                                      │
                                                      ▼
                                  Python validates + optionally reads public.dashboard_users(role, username)
                                  Issues dash_auth cookie (signed HMAC, 7d) + returns JWT in body
                                                      │
                                                      ▼
                              Browser redirects to next|/ with cookie set
```

## Supabase schema
```sql
create table if not exists public.dashboard_users (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  role text not null default 'viewer' check (role in ('admin','editor','viewer')),
  display_name text,
  last_login timestamptz,
  created_at timestamptz not null default now()
);

alter table public.dashboard_users enable row level security;
create policy "self_read"    on public.dashboard_users for select using (auth.uid() = id);
create policy "service_full" on public.dashboard_users for all to service_role using (true);

-- Seed admin (run once manually):
-- 1. In Supabase dashboard → Authentication → Add user:
--    email=service@maximo-seo.com, password=[REDACTED_PASSWORD], email_confirmed=true
-- 2. Run:
-- insert into public.dashboard_users (id, username, role, display_name, email)
-- select id, 'admin', 'admin', 'Admin', email from auth.users where email='service@maximo-seo.com';
```

## Related files
- **Modify:** `webs-html-improvements-files-clean/server.py` — add `supabase_auth.py` helpers (or inline).
- **New:** `webs-html-improvements-files-clean/auth/supabase_auth.py` (module split, optional but recommended).
- **Modify:** `webs-html-improvements-files-clean/login-page.html` — use email field, single endpoint.
- **Modify:** `render.yaml` — no change (envs already declared).

## Implementation steps
1. Create `dashboard_users` table in Supabase (SQL editor).
2. Seed admin user via Supabase dashboard (manual one-time).
3. Add Python helper `verify_supabase_password(email, password) -> dict|None`:
   ```python
   def verify_supabase_password(email, password):
       cfg = supabase_comments_config()   # reuses url + anon key
       if not cfg['configured']:
           return None
       body = json.dumps({'email': email, 'password': password}).encode()
       req = urllib.request.Request(
           f"{cfg['url']}/auth/v1/token?grant_type=password",
           data=body,
           headers={
               'apikey': cfg['key_anon'],
               'Content-Type': 'application/json',
           },
           method='POST',
       )
       try:
           with urllib.request.urlopen(req, timeout=10) as r:
               data = json.loads(r.read().decode())
               return {
                   'id': data['user']['id'],
                   'email': data['user']['email'],
                   'access_token': data['access_token'],
               }
       except urllib.error.HTTPError:
           return None
   ```
4. Add `load_dashboard_user_profile(user_id)` that queries `public.dashboard_users` via service-role key for role + username.
5. Update `_dashboard_validate_credentials(identifier, password)` to try Supabase first, then fall back to `users.json` only if Supabase is unconfigured (transitional).
6. Keep `_stage8_make_token` / `dash_auth` cookie unchanged (good UX).
7. Delete `users.json` fallback after 1 week of green production metrics.

## Todo
- [ ] Confirm Supabase project + paste URL/service-role key.
- [ ] Create table + RLS policies.
- [ ] Seed admin user.
- [ ] Add `supabase_comments_config` alias `supabase_config` (rename for clarity — it's not just comments).
- [ ] Implement `verify_supabase_password`.
- [ ] Implement `load_dashboard_user_profile`.
- [ ] Wire into `_dashboard_validate_credentials`.
- [ ] Update `login-page.html` field from `username` → `email`.
- [ ] Add Google OAuth option (phase 3).
- [ ] Add password-reset route using Supabase `/auth/v1/recover`.

## Success criteria
- Admin can log in with email `service@maximo-seo.com` + `[REDACTED_PASSWORD]` via Supabase.
- `last_login` updates in `dashboard_users`.
- `users.json` can be deleted and login still works.

## Risks
- Supabase free tier rate limits — only relevant if >30 logins/second.
- Service-role key leaks in logs → never log full response bodies.
- If Supabase is down → fallback mechanism needed; temporarily keep `DASHBOARD_USER/DASHBOARD_PASSWORD` env vars as break-glass admin.

## Security
- Password never logged.
- `dash_auth` cookie: `HttpOnly; Secure; SameSite=Lax; Max-Age=604800`.
- Service-role key only used server-side, never sent to browser.
