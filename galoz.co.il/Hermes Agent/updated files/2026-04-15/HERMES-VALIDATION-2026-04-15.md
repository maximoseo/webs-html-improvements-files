# Galoz Article System Rebuild Validation

Date: 2026-04-15
Agent: Hermes Agent
Site: `galoz.co.il`
Real site: `https://www.galoz.co.il/`
Staging topic: `industrial-control-and-command-equipment`

## Deliverables
- `Hermes_Improved_HTML_Template.html`
- `Hermes_Improved_N8N_Prompt.txt`
- `Hermes_Improved_N8N_Workflow.json`
- `HERMES-SOURCE-MAP-2026-04-15.md`

## Live-site findings applied
- The real homepage is a Hebrew RTL industrial catalog/ecommerce supplier with deep navy + industrial blue and restrained red accents.
- Header/search/contact prominence and practical supplier tone were treated as brand constraints.
- The live article page already carries floating WhatsApp/back-to-top behavior, so the article template avoids redundant floating clutter.

## Improvements vs earlier output
- Removed inline JavaScript hover handlers from the HTML template.
- Replaced grid-dependent inline layout with flex-based safer structure in the main redesign file.
- Upgraded the prompt with live-site brand cues and stricter WordPress-safe rules.
- Replaced masked phone CTA with the real main phone from the live site: `0795805040`.
- Updated workflow-embedded prompt metadata to Hermes Agent and synced the revised prompt text.

## Validation checks
- No H1 tags inside the article.
- Root article uses `lang="he"` and `dir="rtl"`.
- HTML contains FAQ using `<details>` blocks.
- HTML contains no inline `onmouseover` / `onmouseout` handlers.
- HTML contains no `display:grid` inline layout rules after Hermes patch.
- Contact page CTA present.
- Main phone CTA present with `tel:0795805040`.
- WhatsApp CTA present.
- Author/trust closure present.
- Workflow JSON parses successfully.
- Prompt and workflow metadata updated to Hermes Agent.

## Export note
Target Obsidian folder for this run:
`galoz.co.il/Hermes Agent/2026-04-15/`
