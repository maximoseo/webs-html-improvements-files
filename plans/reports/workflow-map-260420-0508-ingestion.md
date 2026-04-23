# Workflow Map — Post-Ingestion Integration

## Article redesign pipeline (full chain)

```
┌────────────────────────────────────────────────────────────────────┐
│ 1. DOMAIN ONBOARDING                                                │
│   User gives URL → skillui-cli (ultra mode) + hue-brand-extractor  │
│   Output: domain-brand-map.json entry (colors, font, socials, CTA) │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 2. BRIEF INTAKE                                                     │
│   Article topic + target keyword + N8N PRODUCTS_JSON (if ecom)     │
│   Existing: /redesign-html-template slash command                   │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 3. DESIGN-SYSTEM RESOLUTION                                         │
│   Pull tokens from domain-brand-map → CSS custom properties        │
│   Theme Token Engine (html-ppt-skill pattern)                      │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 4. CONTENT GENERATION                                               │
│   N8N Writing Blog node → raw Hebrew content                        │
│   Inject brand rules (RTL engine, Author trust, CTA hierarchy)     │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 5. MODULE ASSEMBLY (new this batch)                                 │
│   • Products grid (6 cards, e-com domains only)                     │
│   • Mid + End CTA blocks (Button & CTA Hierarchy Fixer)             │
│   • TOC + FAQ (Interaction System)                                  │
│   • Tips / How-To / Did-You-Know (Content modules)                  │
│   • Figure Router: numeric → Chart.js; conceptual → AI image       │
│   • Optional: Illustration Layer (svg-hand-drawn)                   │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 6. FLOATING BUTTONS + SCRIPT                                        │
│   3-button stack (WhatsApp + Contact + Scroll-top)                  │
│   RTL-aware left/right via domain-brand-map.layout.side             │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 7. QA GATE (new hard stop)                                          │
│   agentic-seo-audit → A–F grade (10 checks)                         │
│   compose-style-rubric → scorecard with ceilings                    │
│   Accessibility & Contrast Fixer → WCAG AA                          │
│   FAIL if grade < B or ceiling violated                             │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 8. DEPLOY                                                           │
│   Local: webs-html-improvements-files-clean/{domain}/{agent-ver}/   │
│   Obsidian VPS REST: PUT /vault/{domain}/{agent-ver}/               │
│   Obsidian local: C:/Obsidian/HTML REDESIGN/HTML REDESIGN/{domain}/ │
│   GitHub: commit + push → auto-deploy Render                        │
│   n8n-workflow-map.json: register workflowId                        │
└────────────────────────────────────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 9. POST-PUBLISH MONITOR (new — friday-showcase pattern)             │
│   Nightly cron → fetch live WP post → re-grade                      │
│   Drift ≥ 1 letter → auto-open PR with diff + fix recommendations  │
└────────────────────────────────────────────────────────────────────┘
```

## Skill chain (by slug)

```
skillui-cli → hue-brand-extractor → (domain-brand-map.json)
                                    │
                                    ▼
/redesign-html-template ───► theme-token-engine ───► rtl-hebrew-engine
                                    │
                                    ▼
                           module-assembly
                           ├ products-grid
                           ├ cta-hierarchy (email-campaigns blocks)
                           ├ toc-faq-interaction
                           ├ figure-router (engineering-figure-banana)
                           └ illustration-layer (svg-hand-drawn)
                                    │
                                    ▼
                           compose-style-rubric
                           agentic-seo-audit
                                    │
                                    ▼ (PASS)
                           deploy-obsidian + deploy-github
                                    │
                                    ▼
                           post-publish-monitor (friday-showcase cron)
```

## Integration with existing tooling

| Existing | New dependency | Effect |
|---|---|---|
| `~/.claude/commands/redesign-html-template.md` | Reads domain-brand-map.json | Per-domain token injection |
| `wordpress-html-template-builder` SKILL | Adopts token-swap | Multi-theme output |
| `article-system-rebuild` SKILL | Calls compose-style-rubric | Quality gate at build |
| `n8n-workflow-map.json` | Unchanged | Dashboard Deploy-to-n8n still one-key |
| Existing `/preview` command | Can render themes via ?preview=N | Token-swap preview URLs |
