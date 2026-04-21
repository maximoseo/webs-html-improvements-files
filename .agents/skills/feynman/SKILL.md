# SKILL: Feynman
**Source:** https://github.com/getcompanion-ai/feynman
**Domain:** code
**Trigger:** When conducting AI-powered research on scientific papers, doing multi-agent literature reviews, or replicating ML experiments

## Summary
An open-source CLI AI research agent built on Pi runtime + AlphaXiv paper search. Supports deep research, literature reviews, paper audits, experiment replication, and autonomous research loops. Also installable as standalone skills for other agents.

## Key Patterns
- `feynman "query"` — search papers + web, produce cited brief
- `/deepresearch <topic>` — multi-agent parallel investigation with synthesis
- `/lit <topic>` — literature review with consensus/disagreements/open questions
- `/audit <paper-id>` — compare paper claims against public codebase
- `/replicate <paper>` — replicate experiments on local or cloud GPUs
- `/autoresearch <idea>` — autonomous experiment loop
- 4 agents: Researcher, Reviewer, Writer, Verifier
- AlphaXiv integration for paper Q&A and code reading
- Modal + RunPod for serverless/persistent GPU compute
- Skills-only install: `curl -fsSL https://feynman.is/install-skills | bash`
- Every output source-grounded with direct URLs

## Usage
Install: `curl -fsSL https://feynman.is/install | bash` (macOS/Linux) or PowerShell equivalent. Run `feynman "topic"` for quick research. Use slash commands for structured workflows.

## Code/Template
```bash
# Install
curl -fsSL https://feynman.is/install | bash

# Quick research
feynman "what do we know about scaling laws"

# Deep multi-agent investigation
feynman deepresearch "mechanistic interpretability"

# Literature review
feynman lit "RLHF alternatives"

# Install skills only (for other agents)
curl -fsSL https://feynman.is/install-skills | bash
# Skills install to: ~/.codex/skills/feynman
```
