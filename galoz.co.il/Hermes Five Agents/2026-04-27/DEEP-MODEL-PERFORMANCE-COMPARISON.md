# Galoz Deep Model Performance Comparison

Date: 2026-04-27

Purpose: Compare five model-specific sub-agents without deleting or merging any agent.

## Executive Summary

- Winner by rubric: **Hermes GLM 5.1**
- OpenAI-first operational default: **Hermes GPT 5.5**
- Backup recommendation: **Hermes Opus 4.7**
- Key finding: All five outputs pass the WordPress-ready gate and are intentionally similar; differences are mainly prompt/review depth and model-specific metadata, so the dashboard should preserve all five for future side-by-side tests.

## Rubric

- **wordpress_readiness** (20 pts): RTL/lang semantics, inline CSS density, no script tags, real images, no placeholders, WordPress 1:1 prompt contract
- **content_completeness** (18 pts): word count, Hebrew density, H1/H2/H3 structure, FAQ/details, CTA/contact coverage
- **visual_ux** (14 pts): image count/alt, links and CTAs, responsive-friendly structures, tables/details/sections balance
- **seo_structure** (12 pts): heading hierarchy, internal links, FAQ, schema/prompt notes, source traceability
- **n8n_workflow_quality** (14 pts): valid JSON, node count, wordpressReady metadata, workflow covers HTML/prompt/schema/QA
- **prompt_quality** (12 pts): prompt length, explicit WordPress rules, QA acceptance, image/source instructions, model review incorporated
- **model_distinctiveness** (10 pts): OpenRouter review quality, agent-specific notes, model identity preserved, differences useful for comparison

## Scoreboard

### 1. Hermes GLM 5.1 — 99.32/100
- Model: `z-ai/glm-5.1`
- Metrics: words 1118, Hebrew chars 5211, images 4, links 22, H2 13, FAQ/details 6, scripts 0, placeholders 0
- Category scores: wordpress_readiness 100.0, content_completeness 100.0, visual_ux 100.0, seo_structure 100.0, n8n_workflow_quality 97.7, prompt_quality 97.0, model_distinctiveness 100.0

### 2. Hermes Opus 4.7 — 95.02/100
- Model: `anthropic/claude-opus-4.7`
- Metrics: words 1120, Hebrew chars 5211, images 4, links 22, H2 13, FAQ/details 6, scripts 0, placeholders 0
- Category scores: wordpress_readiness 100.0, content_completeness 100.0, visual_ux 100.0, seo_structure 100.0, n8n_workflow_quality 97.7, prompt_quality 84.1, model_distinctiveness 72.5

### 3. Hermes GPT 5.5 — 95.02/100
- Model: `openai/gpt-5.5`
- Metrics: words 1119, Hebrew chars 5211, images 4, links 22, H2 13, FAQ/details 6, scripts 0, placeholders 0
- Category scores: wordpress_readiness 100.0, content_completeness 100.0, visual_ux 100.0, seo_structure 100.0, n8n_workflow_quality 97.7, prompt_quality 84.1, model_distinctiveness 72.5

### 4. Hermes Gemini 3.1 — 92.85/100
- Model: `google/gemini-3.1-pro-preview`
- Metrics: words 1120, Hebrew chars 5211, images 4, links 22, H2 13, FAQ/details 6, scripts 0, placeholders 0
- Category scores: wordpress_readiness 100.0, content_completeness 100.0, visual_ux 100.0, seo_structure 100.0, n8n_workflow_quality 97.8, prompt_quality 65.9, model_distinctiveness 72.5

### 5. Hermes Kimi K2.6 — 92.73/100
- Model: `moonshotai/kimi-k2.6`
- Metrics: words 1119, Hebrew chars 5211, images 4, links 22, H2 13, FAQ/details 6, scripts 0, placeholders 0
- Category scores: wordpress_readiness 100.0, content_completeness 100.0, visual_ux 100.0, seo_structure 100.0, n8n_workflow_quality 97.7, prompt_quality 65.0, model_distinctiveness 72.5

## Recommendations

- Keep all five agents visible in the dashboard for true model comparison.
- Use the winner_by_rubric for first manual WordPress paste test.
- Use Hermes GPT 5.5 as operational default if maintaining an OpenAI-first workflow matters more than tiny rubric differences.
- For the next experiment, force each model to produce genuinely different creative/layout strategies to better expose model performance differences.

## Important Note

This report does not delete, merge, or replace any sub-agent. It is a comparison layer only.
