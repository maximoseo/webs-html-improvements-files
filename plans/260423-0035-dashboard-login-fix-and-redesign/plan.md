# Plan — Dashboard Login Fix + Supabase Migration + Redesign
**Created:** 2026-04-23 00:35 PT  •  **Target:** html-redesign-dashboard.maximo-seo.ai

Master report: `../../plans/reports/cto-260423-0035-dashboard-login-fix-and-redesign.md`

## Phases

| # | Phase | Owner | Status | Depends on |
|---|---|---|---|---|
| 01 | Supabase Auth migration (users + login in Supabase) | Sonnet 4.6 | pending | — |
| 02 | Server auth hardening (gate, race, secrets, rate-limit) | Sonnet 4.6 | pending | 01 |
| 03 | Design system + login page redesign | Opus 4.7 spec → Sonnet 4.6 exec | pending | 02 |
| 04 | Dashboard modularization + UX polish | Opus 4.7 spec → Sonnet 4.6 exec | pending | 03 |
| 05 | Verification + deploy | Sonnet 4.6 | pending | 01–04 |
| 06 | Future features backlog (P1–P3) | product | ongoing | 05 |

## Key dependencies
- Supabase project URL + service-role key (user to confirm).
- Render env vars editable (`DASHBOARD_USERS`, `DASHBOARD_JWT_SECRET`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`).
- GitHub push access on `maximoseo/webs-html-improvements-files` (auto-deploys to Render).

## Success criteria
- admin logs in with Supabase-backed credentials.
- `/` requires auth — unauthenticated requests redirect to `/login`.
- No race condition between cookie set and dashboard load.
- Design tokens applied; login + nav + Prompt Studio + Keyword Research visibly improved.
- No regressions in radar, comments, deploy flows.
