# SKILL: Awesome AutoResearch — Curated AutoResearch Use Cases
**Source:** https://github.com/WecoAI/awesome-autoresearch
**Domain:** code
**Trigger:** When you want to apply the AutoResearch optimization loop to a new domain or find inspiration for autonomous improvement tasks

## Summary
Curated list of AutoResearch use cases with optimization traces. AutoResearch = program.md that instructs a coding agent to iteratively edit one file, evaluate with fixed metric, keep/revert, loop forever. Portable pattern applied to LLM training, GPU kernels, SQL, voice agents, and more.

## Key Patterns
- Core loop: edit train.py → run 5-min eval → check metric → keep or revert → repeat
- program.md is the "research org code" — comprehensive enough for 10+ hour autonomous runs
- Applied to: GPT training, GPU kernels (18→187 TFLOPS), Shopify Liquid (53% faster), voice agent prompts, tabular ML
- Same loop works for any task with a single measurable metric

## Usage
Adapt program.md for your optimization target. Give agent one file to edit, one metric to maximize.

## Code/Template
```markdown
# program.md structure
- Clear task description and objective metric
- Single file to edit (e.g., kernel.py, train.py)
- Fixed evaluation command (e.g., python bench.py)
- Decision rule: if metric improved → commit, else → revert
- Loop instruction: repeat forever
- Crash handling and recovery procedures
- 6-tier optimization playbook (problem-specific)
```
