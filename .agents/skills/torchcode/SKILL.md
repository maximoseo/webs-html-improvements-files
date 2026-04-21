# SKILL: TorchCode
**Source:** https://github.com/duoan/TorchCode
**Domain:** code
**Trigger:** When practicing PyTorch interview questions or implementing ML operations from scratch (ReLU, softmax, attention, transformers)

## Summary
A self-hosted Jupyter-based platform (like LeetCode for PyTorch) with 40 curated ML interview problems, automated judge with gradient verification, hints, reference solutions, and progress tracking. No GPU required.

## Key Patterns
- 40 problems covering: ReLU, Softmax, LayerNorm, MultiHeadAttention, Transformers, etc.
- `check("relu")` — run tests with colored pass/fail, gradient verification, timing
- `hint("relu")` — nudge without spoilers
- `status()` — progress dashboard across all 40 problems
- `reset_progress()` — clean slate for re-practice
- One-click "Open in Colab" per problem (no local setup)
- Available on Hugging Face Spaces (zero install)
- Judge installable via `pip install torch-judge` for Colab use
- Problems frequency-tagged: 🔥 very likely, ⭐ commonly asked, 💡 emerging

## Usage
Zero-install: launch at huggingface.co/spaces/duoan/TorchCode. Local: `docker run -p 8888:8888 ghcr.io/duoan/torchcode:latest` or `make run`. Install judge for Colab: `pip install torch-judge`.

## Code/Template
```python
# In any notebook or Colab:
from torch_judge import check, status, hint, reset_progress

status()              # see all 40 problems and progress
check("softmax")      # run tests for softmax implementation
hint("attention")     # get a hint for attention implementation

# Your implementation skeleton:
import torch
def my_softmax(x: torch.Tensor, dim: int = -1) -> torch.Tensor:
    # implement here
    pass
check("softmax", my_softmax)
```
