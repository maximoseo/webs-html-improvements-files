# Hermes Orchestrator: Multi-Model Sub-Agents for n8n HTML Template Redesign

Purpose: Coordinate a staged, production-safe redesign pipeline for n8n HTML email/article templates.

Operating rule for this user: run small approval-first batches, one writer at a time, with additive non-destructive changes and QA before deployment.

## Orchestration Policy

1. Receive request with article schema, brand guidelines, current template, and target n8n workflow details.
2. Classify request into pipeline type (see Pipeline Routing below).
3. Create a versioned run folder under `templates/v{YYYY}.{MM}.{DD}.{variant}/`.
4. Run only the agents required for the pipeline type, in staged handoffs:
   - Phase 1: Agent 1 creates structure.
   - Phase 2a: Agent 2 generates design tokens JSON (creative, expensive).
   - Phase 2b: Agent 2b or local script applies tokens as inline CSS (cheap, mechanical).
   - Phase 3: Agent 3 audits accessibility against checklist.
   - Phase 4: Agent 4 optimizes performance (pre-scanned metrics provided in prompt).
   - Phase 5: Local `scripts/agent-5-local.py` handles variable swap, UTM, pixel. Agent 5 AI only called for smart decisions (conditionals, A/B).
5. Between phases, strip handoff context to HTML-only plus 2-line delta (see Handoff Rules).
6. Hermes reviews Agent 3 audit report, Agent 4 performance report, and Agent 5 integration notes.
7. Validate final template before use:
   - n8n placeholder syntax check.
   - HTML size under 80KB target and definitely under Gmail 102KB clipping threshold.
   - Required fields present.
   - No broken unsubscribe/source/tracking placeholders.
8. Save final artifacts and summary to the run folder.

## Pipeline Routing

Not every request needs all agents. Classify at intake:

| Pipeline Type | Agents Used | When to Use |
|---|---|---|
| `full` | 1, 2a, 2b, 3, 4, 5-local (+5-AI if smart decisions needed) | New template or new brand |
| `designUpdate` | 2a, 2b | Brand colors, typography, spacing changed |
| `contentUpdate` | 5-local | New article, same template, no design changes |
| `accessibilityFix` | 3, 4 | Accessibility audit failed, needs fixes |
| `perfFix` | 4 | Size/Outlook/Gmail clipping issues |
| `quickRefresh` | 1, 4, 5-local | Minor structural tweaks + re-optimize |
| `tokensOnly` | 2a | User wants new design tokens JSON only |

If `contentUpdate` is detected, skip ALL AI agents. Run `scripts/agent-5-local.py` only.

### Routing Logic

```python
def classify_pipeline(request):
    if request.is_new_template or request.is_new_brand:
        return "full"
    if request.is_new_article and not request.design_changed:
        return "contentUpdate"
    if request.design_changed and not request.structure_changed:
        return "designUpdate"
    if request.audit_failed:
        return "accessibilityFix"
    if request.size_issue or request.outlook_issue:
        return "perfFix"
    if request.minor_tweak:
        return "quickRefresh"
    return "full"
```

## Handoff Rules (Context Stripping)

To minimize input tokens, never pass full reports between agents. Only pass:

1. The HTML artifact itself.
2. A 2-line delta summary in a comment at the top of the HTML:
   ```html
   <!-- HANDOFF: from=agent-1 | delta=responsive table skeleton, dark mode meta -->
   ```
3. If the next agent needs specific context, add a second comment line:
   ```html
   <!-- CONTEXT: watch Outlook 2019 button rendering in CTA section -->
   ```

Agents MUST NOT output reports, explanations, or markdown fences. Only HTML + summary comment.

## Current Provider Readiness

- Agent 1 GPT 5.5 / Copilot: configured.
- Agent 2 Opus 4.7 / Copilot: depends on Copilot model availability; use the closest available Claude Opus model if exact `Opus 4.7` is unavailable.
- Agent 2b GPT 5.5 or GPT 4o-mini / Copilot: configured; handles mechanical CSS application.
- Agent 3 Gemini 3.1 Pro Preview / Gemini API: configured.
- Agent 4 Kimi K2.6 / Moonshot: Kimi credential exists as `kimi-coding`; exact Kimi K2.6 availability must be checked at run time.
- Agent 5-local: local Python script, zero API cost.
- Agent 5-AI GLM 5.1 / Z.ai: not yet verified/configured in Hermes credential pool. Only used for conditional logic / A/B variants when needed.

## Safe Fallback Policy

If an exact model is unavailable, do not silently pretend. Record the fallback in `analytics.json` and the run summary:
- GPT 5.5 fallback: current Copilot default or strongest Copilot model available.
- Opus 4.7 fallback: strongest Claude Opus/Sonnet model available via Copilot/Claude.
- Agent 2b fallback: GPT 4o-mini (90% cheaper, handles mechanical CSS fine).
- Gemini 3.1 fallback: gemini-3-pro-preview or gemini-2.5-pro.
- Kimi K2.6 fallback: kimi-k2.5, kimi-k2-thinking, or available Kimi coding model.
- GLM 5.1 fallback: skip Agent 5-AI entirely; use local script + orchestrator review.

## Required Run Inputs

- Current template HTML or workflow export.
- Brand guidelines.
- Article data schema.
- Tracking endpoint details.
- n8n workflow node where template should be inserted.
- Pipeline type (auto-detected if not provided).
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
| Agent 2b | CSS Applicator | css-apply-agent | HTML-Redesign/CSS-Apply-Agent |
| Agent 3 | Gemini 3.1 Agent | gemini-3.1-agent | HTML-Redesign/Gemini-3.1-Agent |
| Agent 4 | Kimi K2.6 Agent | kimi-k2.6-agent | HTML-Redesign/Kimi-K2.6-Agent |
| Agent 5 | GLM 5.1 Agent | glm-5.1-agent | HTML-Redesign/GLM-5.1-Agent |
| Agent 5-local | Local Integrator | local-integrator | HTML-Redesign/Local-Integrator |
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

## Cost Optimization Summary

| Strategy | Status | Estimated Savings |
|---|---|---|
| Prompt compression (agent files rewritten) | Done | 30-50% input |
| Strict output format rules | Done | 20-40% output |
| Agent 2 token split (Opus JSON only) | Done | 60-85% Agent 2 |
| Agent 5 local replacement | Done | 80-100% Agent 5 |
| Pipeline routing | Done | 40-80% overall |
| Handoff context stripping | Done | 20-30% input on handoffs |
| Design token caching | Scaffold ready | 60-85% on repeat runs |
| Agent 4 pre-compute | Script ready | 30-50% Agent 4 |
| Response caching | Script ready | Variable |
| Cost tracking | JSON contract ready | Visibility only |

## Credits Monitoring Contract

Each run must append to `runs/credits-log.jsonl`:

```json
{
  "run_id": "v2026.04.26.a",
  "timestamp": "2026-04-26T05:30:00Z",
  "pipeline_type": "full",
  "agents_used": ["agent-1","agent-2a","agent-2b","agent-3","agent-4","agent-5-local"],
  "tokens_in": {"agent-1": 1200, "agent-2a": 800, "agent-2b": 1500, "agent-3": 2000, "agent-4": 1800},
  "tokens_out": {"agent-1": 1200, "agent-2a": 300, "agent-2b": 1400, "agent-3": 600, "agent-4": 1000},
  "est_cost_usd": 0.14,
  "skipped": ["agent-5-ai"],
  "cached": false
}
```
