# Dashboard Auth Runbook

One-command auth diagnostics for the HTML Redesign Dashboard.

## Commands

### 1. Safe production check
Public endpoints only. No password required.

```bash
scripts/auth-runbook.sh safe-prod
```

Checks:
- `/login`
- `/api/auth/status`
- `/api/health`

Use this after deploys to confirm the auth runtime is present before attempting a full login flow.

---

### 2. Full production check
Requires runtime env vars, especially `TEST_ADMIN_PASSWORD`.

```bash
TEST_ADMIN_PASSWORD='***' scripts/auth-runbook.sh full-prod
```

Defaults:
- user: `admin`
- email: `service@maximo-seo.com`
- forwarded IP: `203.0.113.77`
- base URL: `https://html-redesign-dashboard.maximo-seo.ai`

Checks:
- safe production checks
- `POST /api/auth/login`
- `POST /api/login`
- email alias login
- `GET /api/auth/me`
- bad-credentials path
- rate-limit path with forwarded IP headers

---

### 3. Full local check
Requires a local server and `TEST_ADMIN_PASSWORD`.

```bash
PORT=18113 TEST_ADMIN_PASSWORD='***' scripts/auth-runbook.sh local
```

If the server is not running, the wrapper now fails with a short startup hint instead of a Python traceback.

Defaults:
- base URL: `http://127.0.0.1:${PORT:-8010}`
- user: `admin`
- email: `service@maximo-seo.com`

---

### 4. Custom target
Use this for staging or ad-hoc URLs.

```bash
scripts/auth-runbook.sh custom https://example.com
TEST_ADMIN_PASSWORD='***' scripts/auth-runbook.sh custom https://example.com --forwarded-ip 203.0.113.88
```

If `TEST_ADMIN_PASSWORD` is set, the wrapper runs the full auth flow. Otherwise it falls back to public checks only.

## Raw diagnostic script
The wrapper calls:

```bash
python3 scripts/auth_doctor.py <base_url> [...args]
```

Useful options:
- `--user`
- `--email`
- `--password`
- `--forwarded-ip`
- `--bad-attempts`

## Expected success signals

### Safe production
- `/login` → `200`
- `/api/auth/status` → `200`
- `/api/health` → `200`

### Full production / local
- login endpoints → `200`
- bad credentials → `401 invalid_credentials`
- repeated bad attempts from the same forwarded IP → `429 rate_limited`
- `Retry-After` present on the rate-limited response

## Notes
- `auth_doctor.py` redacts tokens/JWTs in output.
- Local HTTP runs may use bearer fallback for `/api/auth/me` because the dashboard cookie is `Secure`.
- Forwarded-IP checks rely on:
  - `CF-Connecting-IP`
  - `X-Forwarded-For`
  - `X-Real-IP`

## Minimal post-deploy flow

```bash
scripts/auth-runbook.sh safe-prod
TEST_ADMIN_PASSWORD='***' scripts/auth-runbook.sh full-prod
```
