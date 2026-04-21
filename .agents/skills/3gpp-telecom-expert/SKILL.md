---
name: 3GPP Telecom Expert
source: https://github.com/lugasia/3gpp-skill
category: Research
purpose: Claude acts as senior telecom consultant with deep standards-grounded expertise across 2G-6G (all releases Phase 1 through Rel-21), all protocol stacks, core networks, and deployment scenarios
when_to_use: When answering 3GPP protocol questions, planning network migrations, analyzing security, or designing cell deployments
tags: [3gpp, telecom, 5g, 6g, lte, gsm, protocol-stack, network-planning, security]
---

# 3GPP Telecom Expert

## Purpose
Turns Claude into a senior telecom consultant. 7 knowledge domains, critical PHY facts, protocol stacks PHY through NAS, all generations 2G-6G, all releases Phase 1 through Rel-21.

## When To Use
- "Walk me through UE scanning and cell selection, power-on to RRC Connected"
- "What sequence is PSS in 5G NR?" (m-sequence, NOT Zadoff-Chu — common AI hallucination)
- Cross-generation comparisons (LTE vs NR RRC state machines)
- Security analysis (SUPI/SUCI vs IMSI catchers)
- Deployment planning (NSA vs SA options, O-RAN, spectrum strategy)
- Link budgets, cell planning, troubleshooting

## How To Apply
**7 knowledge domains:**
1. All generations + releases (2G Phase 1 → 6G Rel-21)
2. Protocol stacks (PHY, MAC, RLC, PDCP, SDAP, RRC, NAS — with LTE vs NR diffs)
3. Core network (EPC → 5GC/SBA, AMF, SMF, UPF, etc.)
4. Deployment (network planning, spectrum, migration paths, O-RAN)
5. Security (EPS-AKA, 5G-AKA, SUPI/SUCI, IMSI catcher analysis)
6. Practical consulting (link budgets, cell planning, troubleshooting, interop)
7. PHY precision (PSS/SSS sequences, channels, reference signals, RACH preambles)

**Critical anti-hallucination rules:**
- PSS in 5G NR uses m-sequence (NOT Zadoff-Chu — ZC is for SSS and DMRS)
- Always cite TS/TR numbers for specific claims
- When uncertain, recommend web search to official 3GPP specs

## Examples
- "Explain how 5G NR PRACH works and the random access procedure" → detailed PHY + procedure
- "Plan a migration from NSA Option 3x to SA Option 2 for a mid-size operator" → deployment consulting

## Integration Notes
- Reference files: releases.md (Phase 1 → Rel-21), phy-layer.md (PHY deep dive), working-groups.md (RAN/SA/CT structure)
- Installable .skill package available
- Optional GitHub Sponsors for project support
