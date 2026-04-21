# SKILL: ClaudePrism
**Source:** https://github.com/delibae/claude-prism
**Domain:** code
**Trigger:** When writing scientific papers, theses, or research documents with LaTeX + Python analysis, offline, with Claude AI assistance

## Summary
A local-first scientific writing workspace (Tauri 2 + Rust) with Claude AI, offline LaTeX compilation via Tectonic, built-in Python/uv environment, and 100+ domain skills (bioinformatics, cheminformatics, ML, clinical research). Open-source alternative to OpenAI Prism.

## Key Patterns
- Offline LaTeX compilation via embedded Tectonic (no cloud upload)
- Built-in uv + venv: one-click Python environment setup
- 100+ scientific skills from K-Dense Scientific Skills catalog
- Skills installed globally (`~/.claude/skills/`) or per-project
- Template gallery + project wizard with AI-generated initial content
- Git-based version history with labels and diff
- Drag & drop PDF/BIB/image reference files
- Claude models: Opus, Sonnet, Haiku — selectable per task
- All files stored locally; Claude API calls sent to Anthropic for inference only

## Usage
Download for macOS/Windows/Linux. Install, open app, pick a template, name your project. Drop reference files. Chat with Claude in the editor. Install domain skills from the skills browser for specialized knowledge.

## Code/Template
```bash
# Install domain skill (bioinformatics example)
# From Skills browser: search "Scanpy" or "BioPython"
# Skills install to: ~/.claude/skills/

# Python environment setup (one-click in app):
uv venv .venv && uv pip install matplotlib seaborn pandas
# Claude auto-uses .venv for Python execution
```
