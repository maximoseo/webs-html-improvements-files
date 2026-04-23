# Phase 02 — Server Auth Hardening

## Overview
- **Priority:** P0
- **Status:** pending
- Fix the silent-disable auth gate, unify login endpoints, add rate limiting, fix secrets.

## Context
See master report §1 Root Cause and §3 Code Review Findings.

## Implementation steps

### 2.1 Always enforce auth when configured
```python
# server.py  (~L2176-2180)
# BEFORE
_auth_users_env = os.environ.get('DASHBOARD_USERS', '').strip()
if _auth_users_env and not _stage8_check_auth(self, parsed):
    return

# AFTER
if _dashboard_auth_enabled() and not _stage8_check_auth(self, parsed):
    return
```
Same change in the POST handler at ~L2841.

### 2.2 Unify login endpoints
Alias `/api/login` → same handler as `/api/auth/login`. Both must:
- Accept `{user|username|email, password}`.
- Set `dash_auth` cookie with `Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=604800`.
- Return `{ok, user, role, token, jwt}` body for front-end convenience.

### 2.3 Secret hygiene
```python
_JWT_SECRET_KEY = os.getenv('DASHBOARD_JWT_SECRET')
if not _JWT_SECRET_KEY and os.getenv('RENDER') == 'true':   # production guard
    raise RuntimeError('DASHBOARD_JWT_SECRET must be set in production')
_JWT_SECRET_KEY = _JWT_SECRET_KEY or 'maximo-dashboard-secret-2025-DEV-ONLY'
```

### 2.4 Rate limiting
Reuse `_R2_RATE_BUCKETS` token-bucket:
```python
def _rate_limit_login(handler, ip, capacity=10, refill_per_sec=0.1):
    now = time.time()
    bucket = _R2_RATE_BUCKETS.setdefault(ip, {'tokens': capacity, 'last': now})
    bucket['tokens'] = min(capacity, bucket['tokens'] + (now - bucket['last']) * refill_per_sec)
    bucket['last'] = now
    if bucket['tokens'] < 1:
        json_response(handler, 429, {'ok': False, 'error': 'rate_limited', 'retry_after': 60})
        return False
    bucket['tokens'] -= 1
    return True
```
Invoke at start of login handler.

### 2.5 do_HEAD stub
```python
def do_HEAD(self):
    # Keep health checkers happy; write headers only.
    try:
        self.do_GET_head_only = True
        self.do_GET()
    finally:
        self.do_GET_head_only = False
```
(Or simpler: return 200 for known public paths, 401 for protected.)

### 2.6 Cookie Secure flag
```python
handler.send_header('Set-Cookie',
    f'dash_auth={token}; Path=/; Max-Age={86400*7}; HttpOnly; Secure; SameSite=Lax')
```

### 2.7 Module split (optional but recommended)
Move to `auth/` package:
- `auth/stage8.py` — cookie session
- `auth/jwt.py`    — JWT issue/verify
- `auth/supabase.py` — Supabase password verification
- `auth/users.py`  — user profile lookup
- `auth/ratelimit.py`

## Todo
- [ ] Apply gate-enforcement fix (§2.1).
- [ ] Unify login endpoints (§2.2).
- [ ] Secret guard (§2.3).
- [ ] Rate limiter (§2.4).
- [ ] HEAD stub (§2.5).
- [ ] Secure cookie (§2.6).
- [ ] (Optional) Split into modules (§2.7).
- [ ] Regression test radar + comments + deploy endpoints.

## Success criteria
- V1–V6 from master report §7 all pass.
- No secrets in code.
- `curl -X POST .../api/login -d '...'` 6× in <60s → last call 429.

## Risks
- Gate enforcement may expose pre-existing broken routes — smoke-test radar/comments/deploy before shipping.
- Cookie `Secure` requires HTTPS (Cloudflare terminates TLS before Render → still works).
