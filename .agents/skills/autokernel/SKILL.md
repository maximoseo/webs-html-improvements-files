# SKILL: AutoKernel — Autonomous GPU Kernel Optimization
**Source:** https://github.com/RightNow-AI/autokernel
**Domain:** code
**Trigger:** When you need to autonomously optimize GPU kernels for a PyTorch model using AI agents

## Summary
Autoresearch loop for GPU kernel optimization. Give it a PyTorch model, agent profiles bottlenecks, extracts Triton/CUDA kernels, optimizes autonomously (edit → benchmark → keep/revert → repeat), ~40 experiments/hour.

## Key Patterns
- Pipeline: profile.py → extract.py → bench.py (loop) → verify.py
- 9 kernel types: matmul, softmax, layernorm, rmsnorm, flash_attention, fused_mlp, cross_entropy, rotary_embedding, reduce
- 5-stage correctness: smoke, shape sweep, numerical stability, determinism, edge cases
- program.md = "research org code" read by agent for autonomous 10+ hour operation

## Usage
Start agent in project dir, tell it to read program.md and kick off optimization.

## Code/Template
```bash
git clone https://github.com/RightNow-AI/autokernel.git && cd autokernel
uv sync && uv run prepare.py
uv run profile.py --model models/llama_7b.py --class-name LlamaModel \
  --input-shape 1,512 --dtype float16
uv run extract.py --top 5
uv run bench.py    # verify benchmark works

# Then in Claude Code / any agent:
# "Read program.md and let's kick off a new experiment. Start with setup."
```
