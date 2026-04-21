# SKILL: Zeroboot - Sub-Millisecond VM Sandboxes via Copy-on-Write Forking
**Source:** https://github.com/zerobootdev/zeroboot
**Domain:** code
**Trigger:** When spinning up isolated sandboxes for AI code execution, needing ultra-low-latency VM provisioning (<1ms), or building secure code execution infrastructure for agents

## Summary
Rust implementation of sub-millisecond KVM VM sandboxes using copy-on-write forking from Firecracker snapshots. p50 spawn latency 0.79ms, ~265KB memory per sandbox. Each sandbox is a real KVM VM with hardware-enforced memory isolation.

## Key Patterns
- CoW forking: mmap(MAP_PRIVATE) snapshot → new KVM VM + restored CPU state in ~0.8ms
- Template once, fork infinitely: boot VM → snapshot → fork per request
- MoE optimization: load only active experts per token (10x faster for MoE models)
- No networking inside forks (serial I/O only)
- Python + TypeScript SDKs for agent integration

## Usage
```python
from zeroboot import Sandbox
sb = Sandbox("zb_live_your_key")
result = sb.run("import numpy as np; print(np.random.rand(3))")
```

## Code/Template
```bash
# Try managed API
curl -X POST https://api.zeroboot.dev/v1/exec \
  -H 'Authorization: Bearer zb_demo_hn2026' \
  -d '{"code":"import numpy as np; print(np.random.rand(3))"}'
# Self-host: requires Linux with KVM support
# Architecture: Firecracker snapshot → mmap(MAP_PRIVATE) → KVM VM (~0.8ms)
```
