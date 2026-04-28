# SKILL: MakhalReader — AI-Scored RSS Reader
**Source:** https://github.com/Tutanka01/makhalReader
**Domain:** content-curation
**Trigger:** Use when setting up an intelligent RSS reader that auto-scores articles by relevance using LLMs, surfaces daily digests, and learns from user feedback.

## Summary
MakhalReader is a self-hosted RSS reader (FastAPI + React) that scores every article 0–10 via Gemini/Ollama before you see it. Features 3-layer deduplication, daily digest view, virtualized UI, keyboard navigation, PWA offline support, and feedback-driven preference learning.

## Key Patterns
- LLM scoring 0-10 before articles appear (noise filtered out)
- Daily Digest tab: 🔥 score≥9, ⭐ score≥7, 👍 score≥5
- 3-layer dedup: canonical URL + title fingerprint + `<link rel="canonical">`
- 👍/👎 feedback updates a preference profile (~220 tokens, contrastive)
- `docker compose up -d` — no migrations, no manual setup
- Works with OpenRouter API key or fully local Ollama

## Usage
When user wants to triage 30+ RSS feeds efficiently without reading noise. One-command deploy, configure OpenRouter or Ollama for scoring.

## Code/Template
```bash
cp .env.example .env
# Set OPENROUTER_API_KEY (or leave blank for Ollama)
docker compose up -d
# App at http://localhost

# Keyboard shortcuts
j/k → next/previous article
r   → toggle read
b   → bookmark
/   → search
```
