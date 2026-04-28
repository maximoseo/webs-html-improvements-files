# SKILL: Ladder — Autonomous Creation & Optimization System
**Source:** https://github.com/danielmiessler/Ladder
**Domain:** agent-tools
**Trigger:** Use when building autonomous AI research loops, continuous optimization pipelines, hypothesis-driven experimentation systems, or structured ideation workflows for agents.

## Summary
Ladder is an open system for autonomous creation and optimization modeled on Renaissance/Bell Labs innovation patterns. Organizes work into 6 stages: Sources → Ideas → Hypotheses → Experiments → Algorithms → Results, with markdown frontmatter files that loop results back as new sources.

## Key Patterns
- 6 pipeline stages: SR- (Sources), ID- (Ideas), HY- (Hypotheses), EX- (Experiments), AL- (Algorithms), RE- (Results)
- Results feed back as sources → continuous autonomous improvement loop
- Cognitive phases: CONSUME → FORM → THINK → LEARN → TALK → STEAL → SLEEP → ABSORB → INSPIRE → TEST
- Each entry is a markdown file with structured frontmatter
- Executable by humans, AI agents, or both

## Usage
When building autonomous AI research/optimization loops, structuring continuous improvement pipelines, or designing experiment-driven agent workflows.

## Code/Template
```markdown
---
type: hypothesis
id: HY-001
source: ID-003
status: pending
---
# Hypothesis: [Testable prediction]

## Prediction
[What we expect to happen]

## Test Method
[How to verify this]

## Success Criteria
[Measurable outcome]
```
