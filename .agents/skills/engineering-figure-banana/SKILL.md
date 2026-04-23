---
name: Engineering Figure Banana
source: https://github.com/heyu-233/engineering-figure-banana
category: Research
purpose: Agent-native skill for engineering and CS paper figures — two separate pipelines for conceptual diagrams (image mode) and exact publication plots (plot mode)
when_to_use: When generating figures for engineering or CS papers, system architecture diagrams, algorithm workflows, or publication-quality quantitative plots
tags: [figures, research, cs-papers, diagrams, plots, visualization, engineering]
---

# Engineering Figure Banana

## Purpose
Not a general-purpose academic figure platform. Specifically splits conceptual diagrams from exact quantitative plots into different workflows — optimized for CS, systems, algorithms, electronics, and embedded paper visuals.

## When To Use
- **image mode**: System architecture diagrams, algorithm workflows, graphical abstracts, electronics schematics, reference-inspired redraws
- **plot mode**: Benchmark bar charts, ablation plots, trend curves, heatmaps, scatter plots, multi-panel quantitative figures
- Rule: if numeric truth matters → plot mode; if conceptual → image mode; if mixed → quantitative panels locally + image for explanatory panels

## How To Apply
**Install (Windows):**
```powershell
& "$HOME/.codex/skills/engineering-figure-banana/scripts/install_and_test.ps1" -RunSetupCheck
```

**Quick wizard:**
```powershell
& "$HOME/.codex/skills/engineering-figure-banana/scripts/wizard.ps1"
```

**Direct test:**
```powershell
python .../scripts/generate_image.py `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search"
```

**Recommended upstream:** use `ai-research-writing-guide` to decide what claim the figure should support, then use this skill to render it.

## Examples
- "Generate a system architecture diagram for our distributed caching system" → image mode
- "Create a bar chart comparing our model vs baselines on 5 benchmarks" → plot mode

## Integration Notes
- Windows tested (primary), macOS reported working, Linux expected to work
- Keep real API keys outside repository
- Prefer local plotting for exact quantitative figures
- Works as Codex skill (SKILL.md in .codex/skills/)
