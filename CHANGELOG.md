# Changelog

## [6.0.0] — 2026-04-22 — Round 6

### Added
- **Telegram alerts** (`r6_features.py`) — auto-alert on `kwr_error`, `deploy_error`, `backup_error` SSE events. Per-key throttling (5 min default) prevents alert storms.
- **Cloud backup** — S3-compatible (Backblaze B2 / Cloudflare R2 / AWS S3). Uses `boto3` if installed, falls back to manual SigV4. Endpoint: `POST /api/cloud-backup`.
- **AI run summaries** via OpenRouter (`gpt-4o-mini` default, configurable) — Hebrew bullet points, falls back to heuristic if no API key.
- **CSRF hard-enforce mode** — set `DASH_CSRF=2` to return 403 on missing/invalid tokens (was log-only).

### Configuration (env vars)
- `TG_BOT_TOKEN`, `TG_CHAT_ID` — Telegram alerts (use existing `@hermesvps64bot` if you want).
- `S3_BUCKET`, `S3_KEY`, `S3_SECRET`, `S3_ENDPOINT`, `S3_REGION` — cloud backup.
- `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` — AI summaries.
- `DASH_CSRF=2` — hard-enforce CSRF.

### Files
- New: `r6_features.py` (~7 KB).
- Modified: `server.py` (+~30 lines).

## [5.0.0] — 2026-04-22 — Round 5

### Added
- **Multi-user auth** with `viewer/editor/admin` roles (`/api/users`, `/api/auth/login`).
- **Audit log** (SQLite) — every mutating action recorded (`/api/audit`).
- **Analytics aggregator** — total/success rate/avg duration, 30-day time series, top errors (`/api/analytics`).
- **Bulk operations** — `delete`, `tag`, `archive` over multiple run IDs (`/api/bulk`).
- **Saved views** — per-user table filter/sort presets.
- **Webhook history** — last 500 outbound/inbound webhook calls.
- **Auto-summary** — heuristic per-run summary + recommendation.
- **Prometheus `/metrics`** — request counters, error counters, status breakdown.
- **Graceful shutdown** — SIGTERM/SIGINT hooks.
- **Sentry hook** — auto-init when `SENTRY_DSN` present.
- **Frontend R5 bundle** — floating Tools panel with 5 tabs, bulk action bar.
- **Docker** — `Dockerfile` + `docker-compose.yml`.
- **OpenAPI spec** — `openapi.yaml`.
