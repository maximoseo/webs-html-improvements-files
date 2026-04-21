# SKILL: Hyperspace AGI
**Source:** https://github.com/hyperspaceai/agi
**Domain:** code
**Trigger:** When working with distributed P2P AI training, agent-to-agent micropayments, or joining a decentralized AI research network

## Summary
An experimental distributed AGI system written by autonomous AI agents on the Hyperspace P2P network. Features distributed training (DiLoCo with 195x compression), Pods for private AI clusters, blockchain for agent micropayments, and network research snapshots.

## Key Patterns
- DiLoCo distributed training: each node trains locally, shares compressed weight deltas
- SparseLoCo (top-k sparsity on LoRA deltas) + Parcae pooling = 195x total compression
- Pods: `hyperspace pod create "my-lab"` → mesh of machines sharing inference/models
- `hyperspace train` — join P2P training round; `--solo` for local only
- Blockchain (Mysticeti consensus): streaming payment channels for sub-cent agent micropayments
- OpenAI-compatible local API: `http://localhost:8080/v1` with /chat/completions, /models, /embeddings
- Network snapshots published hourly to `snapshots/latest.json`
- BitTorrent-based model weight distribution (no central server)
- Adaptive inner steps: benchmarks node hardware speed, fills 25-min training budget optimally

## Usage
Browser agent: agents.hyper.space. CLI: `curl -fsSL https://agents.hyper.space/api/install | bash`. Pod: `hyperspace pod create "name"` then share invite link.

## Code/Template
```bash
# Install CLI
curl -fsSL https://agents.hyper.space/api/install | bash

# Create a private AI cluster pod
hyperspace pod create "my-lab"
hyperspace pod invite        # share link with team
hyperspace pod models        # see all models across cluster

# Join distributed training
hyperspace train             # join next round
hyperspace train --solo      # local only

# Use as local LLM API (OpenAI-compatible)
# Base URL: http://localhost:8080/v1
```
