# Hermes Multi-Agent Git Collaboration — Dashboard Implementation Guide

**Source:** User-provided `hermes-multi-agent-git-collaboration-plan.md`
**Adapted for repo:** `maximoseo/webs-html-improvements-files`
**Dashboard:** https://html-redesign-dashboard.maximo-seo.ai/
**Status:** Active project guidance for future parallel-agent work

---

## 1. Why this exists

This repository can be edited by multiple Hermes agents, but the dashboard is not a clean multi-package app. It has a large monolithic `index.html`, Python backend files, project data/artifact folders, and Render deployment from `main`.

The objective is:

- zero silent overwrites;
- minimal merge conflicts;
- no broken dashboard functionality;
- clear ownership for every agent;
- sequential, verified merges.

---

## 2. Actual repo structure

Do **not** blindly apply a generic React `/src/components` ownership map here.

Current repo reality:

| Area | Files/Folders | Notes |
|---|---|---|
| Monolithic dashboard UI | `index.html` | Shared danger file. Edit with tiny, marker-based patches only. |
| Python backend/API | `server.py`, `kwr_backend.py`, `backup.py`, `r5_features.py`, `r6_features.py`, `n8n_*.py`, `openapi.yaml` | Backend/data logic. |
| Tests and QA | `tests/`, `scripts/`, `.github/` | Regression tests, CI, smoke scripts. |
| Project index/data | `data.json`, domain folders (`galoz.co.il/`, etc.) | One writer at a time. |
| Deployment | `Dockerfile`, Render auto-deploy from `main` | Any deploy-affecting change requires production smoke. |
| Project instructions | `AGENTS.md`, this doc | Edit intentionally only. |

---

## 3. Agent roles and ownership

### Agent Alpha — UI / dashboard behavior

**Primary scope:**

- assigned sections inside `index.html`;
- UI behavior for specific tabs;
- UI CSS/JS blocks in `index.html`;
- static visual assets if later added.

**Special rule:** `index.html` is shared and dangerous. Alpha does not get unlimited ownership of the whole file. Each task must identify exact tab/function/marker ownership.

### Agent Beta — backend / API / data logic

**Primary scope:**

- `server.py`;
- `kwr_backend.py`;
- `backup.py`;
- `r5_features.py`, `r6_features.py`;
- `n8n_*.py`;
- `openapi.yaml`;
- backend state, validation, APIs, provider logic.

### Agent Gamma — tests / QA / docs / CI

**Primary scope:**

- `tests/`;
- `scripts/`;
- `.github/`;
- `docs/`;
- QA reports, smoke tests, CI workflows.

Gamma may add tests for Alpha/Beta work, but should not modify implementation files unless explicitly assigned as the single implementer for that task.

---

## 4. Locked and danger files

These files require special coordination:

| File | Rule |
|---|---|
| `index.html` | One active writer at a time unless exact non-overlapping sections are assigned and merge order is controlled. |
| `data.json` | One writer at a time; always re-read current state immediately before edit. |
| `Dockerfile` | One writer at a time; Render smoke required. |
| `.github/workflows/*` | Gamma-owned but affects all agents; run CI-relevant checks. |
| `AGENTS.md` | Edit between work sessions when possible; preserve existing project rules. |
| Credentials/config | Never commit real secrets; never print tokens. |

---

## 5. Worktree architecture

Use git worktrees for simultaneous work:

```bash
cd /home/seoadmin/webs-html-improvements-files
git fetch origin main

git worktree add ../webs-html-improvements-files-alpha -b alpha/workspace origin/main
git worktree add ../webs-html-improvements-files-beta  -b beta/workspace  origin/main
git worktree add ../webs-html-improvements-files-gamma -b gamma/workspace origin/main

git worktree list
```

Each agent works inside its own folder:

- Alpha: `/home/seoadmin/webs-html-improvements-files-alpha`
- Beta: `/home/seoadmin/webs-html-improvements-files-beta`
- Gamma: `/home/seoadmin/webs-html-improvements-files-gamma`

---

## 6. Branch naming

Format:

```text
{agent}/{category}/{short-description}
```

Examples:

```text
alpha/fix/projects-filter-layout
alpha/feature/prompt-studio-mobile-polish
beta/fix/kwr-download-timeout
beta/feature/n8n-fixer-api-hardening
gamma/test/fixer-leak-regression
gamma/ci/render-smoke-gate
```

Allowed categories:

- `feature`
- `fix`
- `refactor`
- `style`
- `test`
- `ci`
- `docs`
- `chore`
- `data`

---

## 7. Session workflow

At the start of every agent session:

```bash
git status --short
git fetch origin main
git rebase origin/main
```

If unrelated changes exist, stop and report.

Before editing:

1. Identify the exact files and ownership scope.
2. Confirm the task does not touch another agent's active scope.
3. For `index.html`, identify exact functions/markers/selectors to patch.
4. For `data.json`, re-read immediately before writing.

Before push/PR:

```bash
python3 -m py_compile server.py kwr_backend.py
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile
html = Path('index.html').read_text(encoding='utf-8')
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, flags=re.S|re.I)
for i, code in enumerate(scripts):
    p = Path(tempfile.gettempdir()) / f'dashboard-inline-{i}.js'
    p.write_text(code, encoding='utf-8')
    subprocess.run(['node', '--check', str(p)], check=True)
print('all inline scripts OK')
PY
pytest tests/ -q
git diff --check
```

For UI changes, add browser QA when applicable:

- desktop/laptop/tablet/mobile widths;
- target tab;
- neighboring tabs to catch leakage;
- production smoke after deploy.

---

## 8. Merge order

Even when agents work in parallel, merge sequentially:

1. locked/config/dependency changes — full stop, all agents rebase after;
2. Beta backend/API/data contracts;
3. Alpha UI using the backend/contracts;
4. Gamma tests/CI/docs;
5. production smoke after every `main` deploy.

---

## 9. Cross-agent change requests

If an agent needs a change outside its scope, create a request under:

```text
.github/change-requests/{requesting-agent}-{date}-{id}.md
```

Template:

```markdown
---
Requesting Agent: Alpha
Target Agent: Beta
Priority: Normal
Status: Open
---

## Request
Need backend function/endpoint: ...

## Acceptance Criteria
- ...
```

---

## 10. Locks for shared files

For shared files that cannot be split, reserve before editing:

```bash
mkdir -p .github/locks
cat > .github/locks/index-html.lock <<'LOCK'
Agent: Alpha
File: index.html
Since: 2026-04-28T00:00:00Z
Reason: Projects tab sort/filter UI patch
LOCK
```

Release the lock in the same branch/PR once done.

Do not leave stale locks. If a lock exists, stop and inspect before editing.

---

## 11. PR checklist

Every PR or direct maintainer change must be able to answer:

- [ ] Which agent/scope owns these files?
- [ ] Did I avoid unrelated files?
- [ ] Did I avoid locked files, or follow the locked-file protocol?
- [ ] Did I add or update regression tests?
- [ ] Did inline JS syntax pass?
- [ ] Did Python compile checks pass?
- [ ] Did pytest pass?
- [ ] Did browser QA pass for UI changes?
- [ ] Did production smoke pass after deploy?

---

## 12. Render production smoke gate

Do not say “deployed” just because GitHub push succeeded. Confirm production:

- `/api/health` returns `200`;
- login/auth smoke succeeds using secure store credentials only;
- root page contains expected marker(s) when applicable;
- relevant API endpoint returns `200`;
- UI behavior works in production or is covered by authenticated smoke.

Never print secrets while doing this.

---

## 13. Emergency rollback

If production breaks:

```bash
git revert <bad-commit>
# or for merge commits:
git revert -m 1 <merge-commit>
```

Then push, wait for Render, smoke production, and reopen the original task as a tested branch.

---

## 14. Hebrew reporting format

Use this format for this user:

```text
מה נעשה:
- ...

מה נשאר:
- ...

בדיקות:
- ...

סטטוס:
- ...
```
