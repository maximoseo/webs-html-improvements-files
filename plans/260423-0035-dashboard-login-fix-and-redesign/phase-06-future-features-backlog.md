# Phase 06 — Future Features Backlog

See master report §5 for detailed rationale. This file is the shippable tracker.

## P1 — Next 2–4 weeks
- [ ] **F5** Role-based access (admin/editor/viewer) wired to Supabase `dashboard_users.role`.
- [ ] **F6** Audit log page (reuse `r5.audit_log`).
- [ ] **F7** Version history for Prompt Studio deliverables (port `revisions.ts` from Next repo).
- [ ] **F8** Device preview toggle in Prompt Studio (mobile/tablet/desktop iframe).
- [ ] **F9** HTML diff viewer for revisions (side-by-side, monaco-diff).
- [ ] **F10** Keyword batch export (CSV/JSON + n8n push).
- [ ] **F11** n8n deploy confirm + rollback (snapshot before update).

## P2 — Next 1–2 months
- [ ] **F12** Comments/collab surfaced inline + notifications.
- [ ] **F13** Skills Radar UI view with charts.
- [ ] **F14** Agent run tracer (model / latency / tokens / cost).
- [ ] **F15** Template quality scoring (port `lib/validator/*` from Next repo).
- [ ] **F16** Per-domain dashboard (quick-switch context, recent deploys).
- [ ] **F17** WordPress sync preview (dry-run before push).

## P3 — Strategic 2–4 months
- [ ] **F18** Multi-tenant workspaces (Supabase RLS per tenant).
- [ ] **F19** Embeddings + semantic search over skills/prompts (pgvector).
- [ ] **F20** BYO model — OpenRouter key per user; cost reporting.
- [ ] **F21** Slack app (deploy/approve/comment).
- [ ] **F22** Accessibility scoring gate (WCAG AA block deploys).
- [ ] **F23** LLM evaluations dashboard (prompt A/B over time).

## Sequencing recommendation
F5 first (unblocks everyone else's scoped work). Then F7–F9 as a bundle (revisions + diff + preview form a coherent feature). F11 parallel with F5.
