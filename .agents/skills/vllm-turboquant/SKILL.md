# SKILL: vllm-turboquant
**Source:** https://github.com/mitkox/vllm-turboquant
**Domain:** code
**Trigger:** When serving LLMs on RTX A6000 or GB10 GPUs with TurboQuant KV-cache quantization for long-context inference

## Summary
A fork of vLLM extending its experimental TurboQuant KV-cache path for SM86 (RTX A6000) and SM121 (GB10) GPUs. Adds turboquant25/turboquant35 KV-cache recipes, Triton attention backend, per-layer metadata loading, and tensor-parallel metadata slicing.

## Key Patterns
- TurboQuant KV recipes: `turboquant25`, `turboquant35`
- `--attention-backend TRITON_ATTN` — Triton prefill fast path for common head sizes
- `--turboquant-metadata-path <json>` — per-layer metadata or local model-side `turboquant_kv.json`
- Tensor-parallel metadata slicing for replicated/partitioned KV-head layouts
- Source build required (not precompiled wheels)
- CUDA 12.8, Python 3.12, uv package manager

## Usage
```bash
uv venv --python 3.12 && source .venv/bin/activate
export CUDA_HOME=/usr/local/cuda-12.8 VLLM_USE_PRECOMPILED=0
uv pip install -e .
.venv/bin/vllm serve /models/target \
  --tensor-parallel-size 4 \
  --attention-backend TRITON_ATTN \
  --kv-cache-dtype turboquant35 \
  --enable-turboquant \
  --turboquant-metadata-path /models/target/turboquant_kv.json
```

## Code/Template
```bash
# Benchmark TurboQuant vs baseline
bash benchmarks/run_turboquant_gb10_compare.sh
```
