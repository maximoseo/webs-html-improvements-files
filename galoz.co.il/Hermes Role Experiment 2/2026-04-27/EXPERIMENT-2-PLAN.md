# Galoz Role-Based Model Experiment 2 Plan

Objective: Force each model to produce a meaningfully different role/style so model performance can be compared more sharply.

## Safety rules
- Do not delete or merge existing agents
- Create separate Experiment 2 artifacts
- Each model keeps a distinct role
- All HTML must remain full Hebrew RTL WordPress-ready with real images and no scripts
- QA before push/deploy

## Model roles
- **Hermes GPT 5.5 Operational Balanced** (`openai/gpt-5.5`): Operational balanced template: safest default for employees, clean structure, simple WordPress paste, balanced SEO/CRO.
- **Hermes Opus 4.7 Conversion Copy** (`anthropic/claude-opus-4.7`): High-conversion copy and narrative: stronger persuasive copy, trust, authority, CTAs, FAQ depth, but still WordPress-safe.
- **Hermes Gemini 3.1 SEO IA** (`google/gemini-3.1-pro-preview`): SEO and information architecture: stronger headings, semantic clusters, internal links, FAQ/snippet readiness, source traceability.
- **Hermes Kimi K2.6 Workflow Technical** (`moonshotai/kimi-k2.6`): Technical workflow and engineering: stronger n8n JSON/prompt operational detail, variable mapping, QA steps, technical accuracy.
- **Hermes GLM 5.1 WordPress QA** (`z-ai/glm-5.1`): WordPress-safe QA focus: minimal fragile constructs, mobile/RTL/inline CSS safety, acceptance checklist, failure prevention.

## Baseline
- Source: `galoz.co.il/Hermes GPT 5.5/2026-04-27/Improved_HTML_Template.html`
