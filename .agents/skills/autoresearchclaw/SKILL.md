# SKILL: AutoResearchClaw — Autonomous AI Research Pipeline
**Source:** https://github.com/aiming-lab/AutoResearchClaw
**Domain:** code
**Trigger:** When you want to autonomously generate research papers from a single idea or topic using AI agents

## Summary
End-to-end autonomous research pipeline: idea → literature review → experiments → paper. Human-in-the-Loop modes (full-auto to step-by-step). 2699 tests. OpenClaw integration for chat-triggered research. Skills library with 19+ pre-loaded skills.

## Key Patterns
- 6 HITL modes: full-auto, gate-only, checkpoint, step-by-step, co-pilot, custom
- CLI: researchclaw research "X" → runs full pipeline
- Cross-platform: Claude Code, Codex CLI, Copilot CLI, Gemini CLI, Kimi CLI
- Anti-fabrication: VerifiedRegistry + experiment diagnosis & repair loop
- --resume flag for continuing interrupted runs

## Usage
Use for autonomous academic research generation. Always apply human review before any submission (see ethics guidelines).

## Code/Template
```bash
pip install autoresearchclaw   # Python 3.11+
researchclaw research "Effect of X on Y"   # full-auto mode
researchclaw research "X" --mode checkpoint  # human checkpoints
researchclaw attach <run-id>   # attach to running pipeline
researchclaw status <run-id>
researchclaw skills install    # install additional skills
# Via OpenClaw: tell agent "Research X" after clawhub install autoresearchclaw
```
