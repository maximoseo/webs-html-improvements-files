# Sync Template Artifact Procedure

Inputs:
- `agent_slug`
- `agent_obsidian_folder`
- `date` in YYYY-MM-DD
- `template_html_path`
- `report_md_path`

Steps:

1. Copy HTML to local dated path:
   `templates/{agent_slug}/{date}-template.html`
2. Copy HTML to local latest path:
   `templates/{agent_slug}/latest.html`
3. Copy report to:
   `reports/{agent_slug}/{date}-report.md`
4. Mirror to Obsidian using the Hostnox wrapper:
   ```bash
   bash ~/.hermes/skills/note-taking/obsidian-vps/scripts/obsidian.sh put "HTML-Redesign/{Agent-Name}/{date}-template.html" "templates/{agent_slug}/{date}-template.html"
   bash ~/.hermes/skills/note-taking/obsidian-vps/scripts/obsidian.sh put "HTML-Redesign/{Agent-Name}/latest.html" "templates/{agent_slug}/latest.html"
   bash ~/.hermes/skills/note-taking/obsidian-vps/scripts/obsidian.sh put "HTML-Redesign/{Agent-Name}/{date}-report.md" "reports/{agent_slug}/{date}-report.md"
   ```
5. If user approves GitHub sync:
   ```bash
   git pull --rebase origin main
   git add templates/{agent_slug} reports/{agent_slug}
   git commit -m "feat({agent_slug}): HTML template redesign {date}"
   git push origin main
   ```
6. Verify dashboard card after deploy/refresh.
