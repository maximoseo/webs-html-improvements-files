# Hermes Orchestrator: Multi-Model Sub-Agents for n8n HTML Template Redesign

Purpose: Coordinate a staged, production-safe redesign pipeline for n8n HTML email/article templates.

Operating rule for this user: run small approval-first batches, one writer at a time, with additive non-destructive changes and QA before deployment.

## Orchestration Policy

1. Receive request with article schema, brand guidelines, current template, and target n8n workflow details.
2. Create a versioned run folder under `templates/v{YYYY}.{MM}.{DD}.{variant}/`.
3. Run the pipeline as staged handoffs, not broad parallel edits to the same file:
   - Phase 1: Agent 1 creates structure; Agent 2 may prepare design tokens in parallel only if no shared file edits occur.
   - Phase 2: Agent 2 styles Agent 1 output.
   - Phase 3: Agent 3 audits accessibility/content.
   - Phase 4: Agent 4 optimizes performance/compatibility.
   - Phase 5: Agent 5 adds n8n variables, tracking, metadata, and final assembly.
4. Hermes reviews Agent 3 audit report, Agent 4 performance report, and Agent 5 integration notes.
5. Validate final template before use:
   - n8n placeholder syntax check.
   - HTML size under 80KB target and definitely under Gmail 102KB clipping threshold.
   - Required fields present.
   - No broken unsubscribe/source/tracking placeholders.
6. Save final artifacts and summary to the run folder.

## Current Provider Readiness

- Agent 1 GPT 5.5 / Copilot: configured.
- Agent 2 Opus 4.7 / Copilot: depends on Copilot model availability; use the closest available Claude Opus model if exact `Opus 4.7` is unavailable.
- Agent 3 Gemini 3.1 Pro Preview / Gemini API: configured.
- Agent 4 Kimi K2.6 / Moonshot: Kimi credential exists as `kimi-coding`; exact Kimi K2.6 availability must be checked at run time. Known direct Kimi model names may differ.
- Agent 5 GLM 5.1 / Z.ai: not yet verified/configured in Hermes credential pool. Needs GLM/Z.ai key before true model-specific execution.

## Safe Fallback Policy

If an exact model is unavailable, do not silently pretend. Record the fallback in `analytics.json` and the run summary:
- GPT 5.5 fallback: current Copilot default or strongest Copilot model available.
- Opus 4.7 fallback: strongest Claude Opus/Sonnet model available via Copilot/Claude.
- Gemini 3.1 fallback: gemini-3-pro-preview or gemini-2.5-pro.
- Kimi K2.6 fallback: kimi-k2.5, kimi-k2-thinking, or available Kimi coding model.
- GLM 5.1 fallback: hold Agent 5 for user-provided Z.ai key, or run with orchestrator only after explicit approval.

## Required Run Inputs

- Current template HTML or workflow export.
- Brand guidelines.
- Article data schema.
- Tracking endpoint details.
- n8n workflow node where template should be inserted.
- Approval for production deployment.

## Output Contract

Each completed run must produce:
- `template.html`
- `audit-report.md`
- `performance-report.md`
- `integration-notes.md`
- `analytics.json`
- `run-summary.md`

## Template Storage, Versioning, GitHub Sync, and Dashboard Display

Every generated or improved template must be stored in three places before it is considered complete:

1. Obsidian vault mirror.
2. GitHub repository mirror.
3. Dashboard display at `https://html-redesign-dashboard.maximo-seo.ai/`.

### Agent Slugs

| Agent | Display | Slug | Obsidian Folder |
|---|---|---|---|
| Agent 1 | GPT 5.5 Agent | gpt-5.5-agent | HTML-Redesign/GPT-5.5-Agent |
| Agent 2 | Opus 4.7 Agent | opus-4.7-agent | HTML-Redesign/Opus-4.7-Agent |
| Agent 3 | Gemini 3.1 Agent | gemini-3.1-agent | HTML-Redesign/Gemini-3.1-Agent |
| Agent 4 | Kimi K2.6 Agent | kimi-k2.6-agent | HTML-Redesign/Kimi-K2.6-Agent |
| Agent 5 | GLM 5.1 Agent | glm-5.1-agent | HTML-Redesign/GLM-5.1-Agent |
| Hermes | Final Merged Template | hermes-final | HTML-Redesign/Hermes-Final |

### Required Post-Generation Workflow

After each sub-agent finishes a template:

1. Save dated HTML locally: `templates/{agent-slug}/{YYYY-MM-DD}-template.html`.
2. Copy same HTML locally: `templates/{agent-slug}/latest.html`.
3. Save report locally: `reports/{agent-slug}/{YYYY-MM-DD}-report.md`.
4. Mirror dated HTML to Obsidian: `HTML-Redesign/{Agent-Name}/{YYYY-MM-DD}-template.html`.
5. Mirror latest HTML to Obsidian: `HTML-Redesign/{Agent-Name}/latest.html`.
6. Mirror report to Obsidian: `HTML-Redesign/{Agent-Name}/{YYYY-MM-DD}-report.md`.
7. Commit and push local repo changes to GitHub only after approval.
8. Trigger or wait for dashboard refresh.
9. Verify the template appears on `https://html-redesign-dashboard.maximo-seo.ai/` under the right agent name and date.

### Dashboard Data Contract

Dashboard cards must show:
- Agent display name.
- Role.
- Latest date.
- Score.
- Preview action.
- Raw HTML action.
- Version history.

API target:
`GET /api/templates`

Response shape:
```json
{
  "agents": [
    {
      "name": "GPT 5.5 Agent",
      "slug": "gpt-5.5-agent",
      "role": "Layout Architect",
      "latest_date": "2026-04-26",
      "template_url": "/templates/gpt-5.5-agent/latest.html",
      "score": 92,
      "status": "Live",
      "history": [{"date": "2026-04-26", "score": 92, "status": "Live"}]
    }
  ]
}
```

### Deployment Safety

- Do not push to GitHub or n8n without explicit approval.
- Before dashboard code changes, back up current state to Obsidian under `HTML REDESIGN/dashboard/backup-YYYY-MM-DD-HHMM/`.
- After dashboard code changes, verify GitHub push, Obsidian sync, and live dashboard smoke test.
- Secrets/API keys must never be committed or mirrored to Obsidian.

