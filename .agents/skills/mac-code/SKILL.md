# SKILL: Mac Code - Run Large Models Beyond RAM on Apple Silicon
**Source:** https://github.com/walter-grace/mac-code
**Domain:** code
**Trigger:** When running 27B-235B parameter models on 16GB Apple Silicon Macs, implementing flash streaming for models that exceed RAM, or building local AI agents with large models

## Summary
Techniques for running models that genuinely exceed RAM on Apple Silicon using Flash Streaming (stream FFN weights from SSD per-token) and Expert Sniper (MoE routing optimization). Achieves 30 tok/s for 35B MoE at 1.42 GB RAM on a 16 GB Mac mini M4.

## Key Patterns
- Flash Streaming: pin attention/embeddings/KV cache in RAM; stream FFN weights from SSD per token (never grows beyond ~5.5GB)
- Expert Sniper: for MoE models, load only 8 active experts (~14 MB) not all 256 per token (10x faster)
- Batched Union-of-Experts: verify 8 tokens in one forward pass for speculative decoding
- Quick Start: 35B MoE via llama.cpp IQ2_M (30 tok/s, fits in RAM entirely)

## Usage
```bash
brew install llama.cpp && pip3 install rich ddgs --break-system-packages
# Download model (10.6 GB IQ2_M): python3 script via huggingface_hub
llama-server --model ~/models/Qwen3.5-35B-A3B-UD-IQ2_M.gguf --port 8000 --n-gpu-layers 99
python3 agent.py  # Interactive agent with web search + shell
```

## Code/Template
```
Flash Streaming per token:
1. Run attention (from RAM - instant)
2. Load FFN weights from SSD (~165-221 MB)
3. Run FFN matmul on GPU
4. Discard FFN weights (memory stays flat)
MoE: load only 8 active experts (~14 MB) vs 256 total
```
