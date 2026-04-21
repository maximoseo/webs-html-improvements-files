---
name: PaperOrchestra (Multi-Agent Paper Writing)
source: https://github.com/Ar9av/PaperOrchestra
category: Research
purpose: Multi-agent pipeline for turning unstructured research materials into submission-ready LaTeX papers — Outline → Plotting → Literature Review → Section Writing → Refinement
when_to_use: When converting experiment logs and research notes into a formal academic paper
tags: [research, academic, paper-writing, latex, multi-agent, literature-review]
---
# PaperOrchestra

## Purpose
7-skill multi-agent pipeline implementing the PaperOrchestra paper (arXiv:2604.05018) — 50-68% win margin on literature review quality vs single-agent baselines.

## Pipeline
```
agent-research-aggregator (optional)
  ↓ (when inputs missing)
paper-orchestra (orchestrator)
  ↓ parallelizes:
  ├── plotting-agent (Step 2, ~20-30 LLM calls)
  └── literature-review-agent (Step 3, ~20-30 LLM calls)
  ↓
section-writing-agent (Step 4, 1 multimodal call)
  ↓
content-refinement-agent (Step 5, ~5-7 LLM calls: simulated peer review)
```

## 7 Skills
| Skill | Role |
|---|---|
| `paper-orchestra` | Top-level orchestrator |
| `outline-agent` | Idea + log + template → structured outline JSON |
| `plotting-agent` | Execute plotting plan, VLM-critique refinement |
| `literature-review-agent` | Web search + Semantic Scholar verify + draft |
| `section-writing-agent` | One multimodal call: remaining sections + tables |
| `content-refinement-agent` | Simulated peer review with accept/revert |
| `paper-writing-bench` | Reverse-engineer benchmark cases from existing papers |

## Quick Start
```bash
# Option A: structured inputs ready
python skills/paper-orchestra/scripts/init_workspace.py --out workspace/
# Drop idea.md + experimental_log.md + template.tex into workspace/inputs/
# "Run the paper-orchestra pipeline on ./workspace"

# Option B: scattered research directory
"Write a paper from my work in ~/my-project"
```

## Optional Integrations
- `SEMANTIC_SCHOLAR_API_KEY` — higher rate limit for citation verification
- `PAPERBANANA_PATH` — figure generation backbone (Gemini or OpenRouter key)
- `EXA_API_KEY` — research-paper-focused search (~$0.007/query)

## Integration Notes
- No API keys required for core pipeline (uses host agent's native web search)
- All prompts verbatim from Appendix F of arXiv:2604.05018
- Agent-research-aggregator bridges scattered logs → structured inputs
- Pairs with `engineering-figure-banana` for figures
