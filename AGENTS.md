# Maximo SEO Dashboard — Project Context (AGENTS.md)

> This file is the active project overlay for Hermes.
> It defines workflow rules, repo conventions, and the KWR execution contract.
> Identity and personality are handled separately in the agent's SOUL layer — do not repeat them here.

---

## Repo Overview

- Single-page app: `index.html` (tab-based navigation)
- Backend: `server.py` (custom HTTP server, Flask-style routing)
- KWR backend: `kwr_backend.py` (state machine + LLM pipeline)
- Deployment: Render, auto-deploys from `main` branch push, ~40s
- Docker: `Dockerfile` — must explicitly `COPY` every new Python file into the image
- Live site: https://html-redesign-dashboard.maximo-seo.ai/

## Git Push Rule

WSL HTTPS push times out. Always push from:
`/mnt/c/Users/seoadmin/webs-html-improvements-files-clean`

Pattern:
```
git remote set-url origin https://<PAT>@github.com/maximoseo/webs-html-improvements-files.git
git push origin main
git remote set-url origin https://github.com/maximoseo/webs-html-improvements-files.git
```

Clean the remote URL immediately after push. Never leave the PAT in the remote URL.

## LLM Provider

`server.py` exposes `call_with_fallback(messages, model, timeout)`.
Provider chain: copilot -> gemini -> venice -> fireworks -> kimi -> openrouter -> anthropic.
`kwr_backend.py` receives this as a callback — it never imports or calls providers directly.

---

## Keyword Research Automation (KWR) — Execution Contract

<role>
In this repository, act as the implementation and execution agent for the "Keyword Research Automation" feature in the Maximo SEO dashboard. Your job is to implement the dashboard flow, run the research pipeline, produce a reviewable payload, and deploy only after explicit approval. Preserve any user-specified tone, constraints, or locale requirements; otherwise use concise, direct en-US. Treat this prompt as project workflow guidance, not as a personality definition.
</role>

<inputs>
Required slots: <website_url>, <sitemap_url>, <about_url>, <brand_name>, <target_language>, <target_market>, <spreadsheet_target>.
Optional slots: <worksheet_prefix>, <competitor_urls>, <notes_exclusions>, <prior_research_file>, <regenerate_feedback>.
Runtime slots: <connection_ok>, <job_state>, <preview_payload>, <error_message>.

If any required slot is missing, invalid, unreachable, or ambiguous, use clarify to request only the missing item.
If a required tool, credential, webhook, API path, or repo convention is unavailable, stop and report the exact blocker instead of improvising a substitute.
</inputs>

<preflight>
Before editing any file or invoking any live integration, verify the environment and the repo: confirm the required toolchain, install dependencies only when the repo clearly requires it, inspect existing implementation patterns, reuse existing auth and webhook helpers, and check whether target files contain unrelated uncommitted user edits. Keep the diff minimal and scoped to this feature. Do not duplicate existing pages, services, keyword-research modules, or auth flows. Do not overwrite unrelated user changes. If preflight fails, halt with a precise blocker message and the smallest required next action.
</preflight>

<implementation_and_research>
Implement or extend the dashboard tab named "Keyword Research Automation" with the required inputs, connection test, run action, editable preview, approval action, reject/regenerate action, last-run status widget, and a server-persisted state machine. Use the exact workflow order: validate inputs, analyze the about page and home page, parse the sitemap into an existing-pages index, research competitors in the target market, apply exclusions, validate demand, generate the preview payload, and then run anti-cannibalization checks.

The review payload must use exactly six columns in this order:
Existing Parent Page | Pillar | Cluster | Intent | Primary Keyword | Keywords

Pillar rows: use "-" in column A and repeat the pillar in column C.
Cluster rows: point column A to the pillar slug.

Do not invent services the business does not actually offer, do not duplicate existing pages, do not create semantic cannibalization, do not emit duplicate primary keywords, and do not mix languages in the output except where brand or URL requirements force it.

Target 200-250 rows. If real site scope and deduplication constraints make that impossible, return the honest lower count with a short explanation rather than filler.
</implementation_and_research>

<approval_deploy_and_tests>
Never write to the live spreadsheet before explicit approval.
"Run" may generate only the in-app preview payload.
"Approve and Deploy" must send the current edited preview state, create a new uniquely named worksheet only, apply the required formatting and hyperlink behavior, persist job metadata, and update the last-run widget.

If deployment fails for permissions, quota, validation, or remote errors: preserve the preview, store the exact error, keep the state truthful, and do not mark the job as deployed.

Deploy goes via N8N_KWR_WEBHOOK_URL only — no direct Google Sheets API calls in Python.

Ship backend and frontend tests for validation, state transitions, preview editing, approve/deploy flow, regenerate flow, and mocked spreadsheet writes. Then run the repo's relevant test commands and report a concise completion summary using:

<state>, <actions_taken>, <blockers_or_errors>, <artifacts>, <next_step_if_any>
</approval_deploy_and_tests>

---

## Expected State Report Format

```
State: <queued|validating|analyzing_site|parsing_sitemap|researching_competitors|generating_rows|deduplicating|ready|complete|failed|cancelled>
Actions taken: <short list>
Blockers/errors: <exact message or "none">
Artifacts: <preview row count, sheet URL if deployed, or "none">
Next step: <what the user should do now, or "none">
```

---

## Open Questions (resolve before evals)

See `prompts/kwr/KWR-OPEN-QUESTIONS.md` for the full list.
Key unresolved items:
- N8N_KWR_WEBHOOK_URL not yet set in Render (user must create the N8N workflow and provide the URL)
- Row-count vs pillar-count precedence when constraints conflict (current rule: honest lower count wins)
- Language mixing behavior for Hebrew content + English brand terms
- Connection test scope: reachability only, or verify write permission before enabling Run
