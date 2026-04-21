---
name: Paper Finder (Academic Search)
source: https://github.com/bchao1/paper-finder
category: Research
purpose: Academic paper discovery and search skill (repo not publicly accessible at time of ingestion)
when_to_use: When searching for academic papers by topic, keyword, or author
tags: [research, academic, papers, search, arxiv]
---
# Paper Finder

## Purpose
Academic paper discovery and search tool. Note: repository was not publicly accessible at time of skill ingestion (April 2026). Skill created as placeholder.

## Expected Capabilities (Common Pattern)
- Search arXiv, Semantic Scholar, PubMed by topic/keyword
- Filter by date, citations, venue
- Export BibTeX references
- Summarize abstracts

## Alternatives (Confirmed Working)
- `paper-orchestra-skill` — uses Semantic Scholar API for literature review (verified)
- `lich-skills/tavily-search` — general web search including papers
- Direct: `https://api.semanticscholar.org/graph/v1/paper/search`

## Integration Notes
- Original repo: https://github.com/bchao1/paper-finder
- Status: 404 at time of ingestion — check repo for public access
- For academic search, prefer `paper-orchestra-skill` (verified + documented)
