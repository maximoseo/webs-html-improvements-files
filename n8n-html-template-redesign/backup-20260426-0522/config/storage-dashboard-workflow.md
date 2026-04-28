# Template Storage, Versioning & Dashboard Workflow

## Canonical Requirements

Every sub-agent output must be saved to Obsidian, synced to GitHub, and displayed on the HTML Redesign Dashboard.

Dashboard URL: https://html-redesign-dashboard.maximo-seo.ai/
Repository target: maximoseo/webs-html-improvements-files unless a separate repo is explicitly approved.

## Local/GitHub Structure

```text
templates/
  gpt-5.5-agent/{YYYY-MM-DD}-template.html
  gpt-5.5-agent/latest.html
  opus-4.7-agent/{YYYY-MM-DD}-template.html
  opus-4.7-agent/latest.html
  gemini-3.1-agent/{YYYY-MM-DD}-template.html
  gemini-3.1-agent/latest.html
  kimi-k2.6-agent/{YYYY-MM-DD}-template.html
  kimi-k2.6-agent/latest.html
  glm-5.1-agent/{YYYY-MM-DD}-template.html
  glm-5.1-agent/latest.html
  hermes-final/{YYYY-MM-DD}-template.html
  hermes-final/latest.html
reports/
  {agent-slug}/{YYYY-MM-DD}-report.md
```

## Obsidian Structure

```text
HTML-Redesign/
  GPT-5.5-Agent/{YYYY-MM-DD}-template.html
  GPT-5.5-Agent/latest.html
  Opus-4.7-Agent/
  Gemini-3.1-Agent/
  Kimi-K2.6-Agent/
  GLM-5.1-Agent/
  Hermes-Final/
```

## Git Workflow

Use the existing dashboard repo workflow:

```bash
cd /path/to/repo
git pull --rebase origin main
git add templates reports dashboard config
git commit -m "feat(html-templates): sync agent templates YYYY-MM-DD"
git push origin main
```

From WSL, use PowerShell for push if the repo requires Windows credential access.

## Dashboard Verification

After push/deploy:

1. Open https://html-redesign-dashboard.maximo-seo.ai/
2. Confirm six cards exist: five agents plus Hermes final.
3. Confirm each populated agent card shows latest date and score.
4. Confirm Preview renders in iframe.
5. Confirm HTML view is copyable.
6. Confirm compare mode can compare two template versions.
7. Check browser console for errors.

## Approval Gate

Saving local files and Obsidian backups is allowed as a normal backup step.
GitHub push, dashboard deployment, webhook setup, and n8n production updates require explicit approval.
