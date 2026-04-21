# SKILL: Autoresearch MLX - Apple Silicon Port of Karpathy Autoresearch
**Source:** https://github.com/trevin-creator/autoresearch-mlx
**Domain:** code
**Trigger:** When running autonomous ML research loops on Apple Silicon, optimizing neural network training with fixed time budgets, or using Claude Code for iterative ML experimentation

## Summary
Apple Silicon (MLX) port of Karpathy's autoresearch: autonomous research loop controlled via program.md with one mutable train.py, one metric (val_bpb), 5-minute training budget, keep-or-revert via git. Native MLX replaces PyTorch/CUDA.

## Key Patterns
- Fixed files: prepare.py (data/eval, read-only), train.py (model/optimizer, editable by agent)
- program.md: the autonomous experiment protocol Claude reads
- results.tsv: experiment history log
- ~6-7 min per experiment on Apple Silicon (5min train + compile + eval)
- Key Apple Silicon insight: smaller faster-training models beat larger ones within fixed time budget
- Point Claude Code or any coding agent at program.md to run the loop

## Usage
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv run prepare.py    # one-time: data + tokenizer prep
uv run train.py      # run one 5-minute experiment
# Then point Claude Code at program.md
```

## Code/Template
```
Loop: read train.py → pick change → edit → git commit → run val_bpb → 
      if improved: keep | if worse: git revert → log to results.tsv → repeat
```
