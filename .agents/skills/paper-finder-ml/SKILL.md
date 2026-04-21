---
name: Paper Finder ML
source: https://github.com/bchao1/paper-finder
category: Research
purpose: Find, organize, and maintain a persistent knowledge base of ML/AI/CV/NLP research papers with mind-graph connections, BibTeX, and per-paper summaries
when_to_use: When searching for related work, building literature reviews, discovering papers on a topic, or organizing research references
tags: [research, papers, ml, arxiv, semantic-scholar, bibtex, literature-review]
---

# Paper Finder ML

## Purpose
Research paper discovery and organization agent. Searches arxiv, Google Scholar, Semantic Scholar, and top venues (CVPR, NeurIPS, ICML, ACL, SIGGRAPH, etc.). Maintains a persistent knowledge base with memory bank, mind-graph, and BibTeX.

## When To Use
- "Find papers on mixed-resolution diffusion"
- "What exists about video generation efficiency?"
- "Related work for my paper on transformers"
- Building a literature review
- Organizing references for a conference submission

## How To Apply
**Search strategy (mandatory):**
1. Semantic Scholar API: `https://api.semanticscholar.org/graph/v1/paper/search?query=<q>&limit=20`
2. WebSearch with venue-specific queries
3. Multi-angle search: cross-domain synonyms + enabling mechanisms + motivating applications
4. Follow citation graph of top-relevance papers

**Directory structure per topic:**
```
<topic-name>/
  memory-bank.md     # All discovered papers
  mind-graph.md      # Topic-paper connections
  summaries/         # Per-paper .md files
  references.bib     # Combined BibTeX
  pdfs/              # Only when user asks
  discussions/       # Comparison logs
```

**Do NOT download PDFs unless explicitly requested**

## Examples
- "Find papers on efficient attention mechanisms for long sequences" → 3 parallel searches + multi-angle pass
- "Build a BibTeX file for my literature review on diffusion models" → search + memory-bank + references.bib

## Integration Notes
- Training knowledge alone misses 2024-2025+ papers — web search is mandatory
- Venues: CV (CVPR, ECCV, ICCV), ML (NeurIPS, ICML, ICLR), NLP (ACL, EMNLP), Graphics (SIGGRAPH), Robotics (CoRL, RSS)
- Invoke research-paper-analyst skill for detailed per-paper summaries
- Prioritize algorithmic contributions over systems/engineering papers
