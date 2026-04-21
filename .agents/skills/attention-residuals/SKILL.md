# SKILL: Attention Residuals (AttnRes) — Drop-in Transformer Residual Replacement
**Source:** https://github.com/MoonshotAI/Attention-Residuals
**Domain:** code
**Trigger:** When implementing or improving Transformer architectures with better depth utilization

## Summary
Drop-in replacement for standard residual connections. Each layer selectively aggregates earlier representations via learned softmax attention over depth. Block AttnRes matches 1.25x compute baseline with marginal overhead.

## Key Patterns
- Full AttnRes: each layer attends over all previous outputs (O(Ld) memory)
- Block AttnRes: N blocks with intra-block standard residuals + inter-block attention (O(Nd) memory)
- Per-layer pseudo-query w_l learned; softmax over preceding layer outputs
- Improves GPQA-Diamond +7.5, HumanEval +3.1 on Kimi 48B MoE model

## Usage
Apply to any Transformer training run as a drop-in for standard residuals.

## Code/Template
```python
def block_attn_res(blocks, partial_block, proj, norm):
    V = torch.stack(blocks + [partial_block])          # [N+1, B, T, D]
    K = norm(V)
    logits = torch.einsum('d, n b t d -> n b t', proj.weight.squeeze(), K)
    return torch.einsum('n b t, n b t d -> b t d', logits.softmax(0), V)
# Apply before attention and MLP in each transformer layer
```
