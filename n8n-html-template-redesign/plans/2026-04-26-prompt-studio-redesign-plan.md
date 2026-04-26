# Prompt Studio Redesign Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task after user approval.

**Goal:** Redesign the HTML Redesign Dashboard Prompt Studio popup into a professional, intuitive, responsive pipeline launcher with AI prompt generation and one-click Hermes 5-agent execution.

**Architecture:** Implement in small approval-gated phases inside the existing dashboard codebase. The current dashboard is a production single-file SPA, so each batch must be backed up to Obsidian, patched additively, verified locally, synced to Obsidian, pushed only after approval, and smoke-tested live after Render deploy.

**Tech Stack:** Existing HTML Redesign Dashboard at `https://html-redesign-dashboard.maximo-seo.ai/`, repo `maximoseo/webs-html-improvements-files`, likely single-file `index.html` plus `server.py`. No broad rewrite; prefer additive CSS/JS and backend endpoints.

---

## Safety Gates

- Do not touch production dashboard code until user approves Phase 1 implementation.
- Before any code edit: back up `index.html`, `server.py`, and `n8n-workflow-map.json` to Obsidian under `HTML REDESIGN/dashboard/backup-YYYY-MM-DD-HHMM/`.
- Local/Obsidian plan files are allowed now; GitHub push, dashboard deployment, webhook setup, and n8n updates require explicit approval.
- Never expose API keys in frontend code. AI prompt generation must run through backend endpoints.

---

## Phase 1: Popup Foundation

### Task 1: Inspect Current Prompt Studio Implementation

**Objective:** Locate existing Prompt Studio markup, styles, JS handlers, and backend routes.

**Files:**
- Read: `/mnt/c/Users/seoadmin/webs-html-improvements-files-clean/index.html`
- Read: `/mnt/c/Users/seoadmin/webs-html-improvements-files-clean/server.py`

**Steps:**
1. Search for `Prompt Studio`, `prompt-studio`, prompt modal functions, and related routes.
2. Record exact line ranges and current behavior.
3. Produce a short implementation note before editing.

**Verification:** Existing dashboard still unchanged; note includes target patch locations.

### Task 2: Add Professional Modal Shell

**Objective:** Replace/extend the popup shell with a 900px desktop / full-screen mobile modal.

**Files:**
- Modify: `index.html`

**Implementation requirements:**
- `.prompt-studio-overlay`
- `.prompt-studio`
- `.prompt-studio-header`
- `.prompt-studio-tabs`
- `.prompt-studio-content`
- `.prompt-studio-footer`
- close button with accessible label
- Esc-to-close behavior
- no production data mutation

**Verification:**
- Modal opens/closes.
- Esc closes.
- Mobile viewport shows full-screen modal.
- No browser console errors.

### Task 3: Add Accessible Tab System

**Objective:** Add Builder, AI Generate, Templates, Config tabs.

**Files:**
- Modify: `index.html`

**Implementation requirements:**
- `role="tablist"`, `role="tab"`, `role="tabpanel"`
- `aria-selected`, `aria-controls`, `hidden`
- keyboard navigation: ArrowLeft/ArrowRight, Home/End

**Verification:**
- Mouse and keyboard tab switching works.
- Screen reader attributes update.

---

## Phase 2: Builder Tab

### Task 4: Build Structured Builder Form

**Objective:** Add form sections for template source, brand/site, article schema, output target, and approval.

**Files:**
- Modify: `index.html`

**Fields:**
- template source type: paste HTML / file path / n8n workflow export
- template textarea/path
- brand name, domain, logo URL
- primary/accent/background/text colors
- tone/style
- title, subtitle, author, date, hero image, campaign id, source URL
- tags input
- article body textarea
- output checkboxes: local, Obsidian, GitHub, dashboard, n8n
- approval checkboxes: auto-approve GitHub, dashboard, n8n

**Verification:** Form state can be serialized to a JS object.

### Task 5: Generate Hermes Prompt from Builder Form

**Objective:** Convert form state into the canonical Hermes pipeline prompt.

**Files:**
- Modify: `index.html`

**Requirements:**
- Default output target: local + Obsidian only.
- Manual approval required unless explicitly checked.
- Include current provider limitations:
  - Copilot ready.
  - Gemini ready.
  - Kimi needs runtime verification.
  - GLM/Z.ai not configured until key is added.

**Verification:** Clicking Preview Prompt fills editable prompt preview with a complete pipeline command.

---

## Phase 3: AI Generate Tab

### Task 6: Add Backend Prompt Generation Endpoint

**Objective:** Create a secure backend route for AI prompt generation.

**Files:**
- Modify: `server.py`

**Endpoint:**
- `POST /api/prompt-studio/generate`

**Request:**
```json
{
  "provider": "copilot",
  "model": "gpt-5.5",
  "description": "Redesign the newsletter template...",
  "templatePath": "/home/seoadmin/projects/n8n/current-template.html",
  "brandUrl": "https://maximo-seo.ai",
  "formState": {}
}
```

**Response:**
```json
{
  "ok": true,
  "prompt": "Run the n8n template redesign pipeline...",
  "provider": "copilot",
  "model": "gpt-5.5",
  "warnings": []
}
```

**Security:**
- API keys from environment/server-side config only.
- Never return secrets.
- Add timeout and clear error messages.
- If provider unavailable, return `ok:false` with actionable warning.

**Verification:** Endpoint returns a generated prompt or safe error using configured provider.

### Task 7: Build AI Generate UI

**Objective:** Add quick input, provider/model selector, generate button, editable generated prompt preview.

**Files:**
- Modify: `index.html`

**Requirements:**
- Provider choices: Copilot, OpenRouter if key exists.
- Models must come from backend/status where possible, not a hardcoded tiny list.
- Buttons: Generate, Regenerate, Copy, Run Pipeline.
- Loading/error states.

**Verification:** Generate button calls backend endpoint and renders prompt safely.

---

## Phase 4: Templates & Config

### Task 8: Add Saved Prompt Templates

**Objective:** Provide reusable prompt templates.

**Files:**
- Modify: `index.html`

**Default templates:**
- Full Pipeline — all 5 agents, local + Obsidian, manual approval.
- Design Only — Agents 1 and 2.
- Accessibility Audit Only — Agent 3.
- Performance Only — Agent 4.
- Quick Auto Deploy — visible but gated with explicit warning.

**Verification:** Load/edit/delete works in local storage or existing dashboard storage pattern.

### Task 9: Add Provider Config/Status UI

**Objective:** Show readiness for prompt-generation and sub-agent providers.

**Files:**
- Modify: `index.html`
- Modify: `server.py` if status endpoint is missing

**Endpoint:**
- `GET /api/prompt-studio/status`

**Status targets:**
- Agent 1 GPT 5.5 / Copilot: configured
- Agent 2 Opus 4.7 / Copilot: exact model runtime check
- Agent 3 Gemini 3.1 / Gemini API: configured
- Agent 4 Kimi K2.6 / Moonshot: needs runtime verification
- Agent 5 GLM 5.1 / Z.ai: not configured unless key exists

**Verification:** Status bar renders green/yellow/red with text labels.

---

## Phase 5: Pipeline Execution

### Task 10: Add Pipeline Run Endpoint Stub

**Objective:** Add a safe backend endpoint that accepts a generated prompt but does not mutate production until approved.

**Files:**
- Modify: `server.py`

**Endpoint:**
- `POST /api/prompt-studio/run`

**Initial behavior:**
- Save request to prompt history/log.
- Return a `run_id` and staged status.
- Do not update GitHub/dashboard/n8n unless approvals are explicit.

**Verification:** Endpoint creates a run record and returns `queued`/`started` status.

### Task 11: Add Live Progress UI

**Objective:** Show per-agent running states.

**Files:**
- Modify: `index.html`
- Modify: `server.py` if SSE endpoint is added

**Preferred endpoint:**
- `GET /api/prompt-studio/runs/{run_id}/events` using SSE

**Fallback:** Poll `GET /api/prompt-studio/runs/{run_id}`.

**Verification:** UI progresses through Agent 1..5 with done/running/waiting/error states.

---

## Phase 6: Polish and QA

### Task 12: Accessibility and Responsive QA

**Objective:** Ensure Prompt Studio itself is production-quality.

**Checks:**
- desktop, laptop, tablet, mobile
- keyboard-only usage
- Esc close and focus return
- visible focus states
- no color-only statuses
- modal traps focus while open
- form labels tied to inputs
- no console errors

### Task 13: Dashboard Smoke and Deployment Verification

**Objective:** Push only after approval, then verify live dashboard.

**Commands:**
- PowerShell git push workflow per dashboard skill.
- Obsidian sync for `index.html`, `server.py`, `n8n-workflow-map.json`.
- Live URL HTTP 200.
- Browser smoke test on `https://html-redesign-dashboard.maximo-seo.ai/`.

**Verification:** Prompt Studio popup works live and does not regress existing dashboard features.

---

## Acceptance Criteria

- Prompt Studio looks professional and matches dashboard style.
- Builder tab creates a complete Hermes pipeline prompt without manual typing.
- AI Generate tab can create an improved prompt through backend provider endpoint.
- Provider status clearly shows ready/warning/offline.
- Run Pipeline button has safe states and manual approval gates.
- Progress UI shows Agent 1-5 status.
- All changes are backed up to Obsidian and mirrored after implementation.
- No secrets are exposed in frontend.
- Dashboard remains mobile-friendly and accessible.
