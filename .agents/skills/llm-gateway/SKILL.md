# SKILL: LLM Gateway (OpenZiti)
**Source:** https://github.com/openziti/llm-gateway
**Domain:** code
**Trigger:** When routing LLM requests across OpenAI, Anthropic, and local backends (Ollama, vLLM) with zero-trust networking, semantic routing, and multi-endpoint load balancing

## Summary
An OpenAI-compatible API proxy that routes by model name prefix, translates Anthropic format, and exposes backends via zrok (OpenZiti) for zero-trust access across NAT/air-gaps. Single Go binary, one YAML config, no database.

## Key Patterns
- Route by prefix: `gpt-*/o1-*/o3-*` → OpenAI, `claude-*` → Anthropic, else → local
- Semantic routing (3-layer cascade): keyword heuristics → embedding similarity → LLM classifier
- Multi-endpoint load balancing: weighted round-robin + passive failover + health checks
- VM sleep detection; mix Ollama/vLLM/llama-server in same pool
- zrok shares: expose gateway or backends across NAT without port forwarding
- OpenTelemetry/Prometheus metrics; virtual API keys with model-glob restrictions

## Usage
```bash
go install github.com/openziti/llm-gateway/cmd/llm-gateway@latest
llm-gateway run config.yaml
```

## Code/Template
```yaml
listen: ":8080"
providers:
  open_ai:
    api_key: "${OPENAI_API_KEY}"
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
  local:
    endpoints:
      - name: gpu-box-1
        base_url: "http://10.0.0.1:11434"
        weight: 3
      - name: gpu-box-2
        base_url: "http://10.0.0.2:11434"
    health_check:
      interval_seconds: 30
```
