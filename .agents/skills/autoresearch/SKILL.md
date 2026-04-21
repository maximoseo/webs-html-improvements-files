# SKILL: autoresearch (Karpathy)
**Source:** https://github.com/karpathy/autoresearch
**Domain:** code
**Trigger:** When running autonomous AI-driven research loops overnight — letting an agent iterate on code (train, measure, keep/discard) without human supervision

## Summary
Karpathy's autoresearch gives an AI agent a minimal LLM training setup and lets it experiment autonomously: modify train.py, run for 5 minutes, check val_bpb metric, keep or discard, repeat. Wake up to 100 experiments and a better model. The core pattern: fixed time budget + single measurable metric + agent edits single file.

## Key Patterns
- **Single file to modify**: agent only edits `train.py` (model, optimizer, hyperparams, architecture)
- **Fixed 5-minute time budget** per experiment — makes experiments directly comparable
- **Metric**: `val_bpb` (validation bits per byte) — lower is better, vocab-size-independent
- **`program.md`**: the "OS" — human edits this to configure the research org
- **`prepare.py`**: fixed constants + data prep — agent does NOT modify this
- Loop: modify → commit → evaluate → keep/discard → log → repeat (~12 experiments/hour)
- Self-contained: single GPU, one file, one metric, no distributed training

## Usage
```bash
uv sync
uv run prepare.py          # one-time data download + tokenizer (~2 min)
uv run train.py            # manual single run (~5 min)
# Then spin up Claude/Codex in this repo and prompt:
# "Look at program.md and kick off a new experiment"
```

## Code/Template
```markdown
# program.md (the human-editable research org instructions)
## Goal
Minimize val_bpb on the FineWeb validation set.
## Current best
val_bpb = X.XXX (commit: abc123)
## Hypotheses to try next
- Try reducing DEPTH from 8 to 6 with wider hidden dim
- Experiment with WINDOW_PATTERN = "SSSSL"
```
