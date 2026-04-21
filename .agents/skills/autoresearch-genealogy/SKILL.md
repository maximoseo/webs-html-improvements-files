# SKILL: autoresearch-genealogy
**Source:** https://github.com/mattprusak/autoresearch-genealogy
**Domain:** code
**Trigger:** When applying Karpathy-style autonomous research loops to genealogy — expanding family trees, auditing sources, resolving unknown ancestors, or analyzing DNA data

## Summary
Structured prompts, Obsidian vault templates, and autoresearch workflows for AI-assisted genealogy. Produced 105 files spanning 9 generations across 6 family lines. Includes 12 autoresearch prompts, 24 country-specific archive guides, and 7 step-by-step workflows.

## Key Patterns
- 12 prompts with Goal/Metric/Direction/Verify/Guard/Iterations/Protocol structure
- Key prompts: tree-expansion, cross-reference-audit, findagrave-sweep, source-citation-audit, immigration-search, dna-chromosome-analysis
- Normalized fact schema with confidence tiers: Strong Signal / Moderate Signal / Speculative
- Vault template: Family_Tree.md, per-person YAML frontmatter, research-log, open-questions
- Measurable metrics: count of sourced claims, resolved questions, remaining discrepancies
- Log negative results (what you didn't find is as important as what you found)

## Usage
```bash
git clone https://github.com/mattprusak/autoresearch-genealogy
# Copy vault-template/ into Obsidian vault
# Fill Family_Tree.md, then run prompts via Claude Code /autoresearch
```

## Code/Template
```markdown
# Prompt structure (01-tree-expansion.md)
Goal: Push every branch as far back as possible
Metric: Count of ancestors with birth year known
Direction: higher
Verify: Cross-reference against 2+ independent sources
Guard: No speculative claims without citation
```
