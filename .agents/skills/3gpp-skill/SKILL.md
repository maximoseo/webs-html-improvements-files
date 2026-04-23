---
name: 3GPP Telecom Expert
source: https://github.com/lugasia/3gpp-skill
category: Research
purpose: Deep 3GPP expertise — 2G through 6G, all releases, protocol stacks, core network, deployment, security, consulting
when_to_use: When asking about telecom standards, 5G NR architecture, LTE vs 5G differences, PHY layer, cell planning, or 3GPP spec series
tags: [telecom, 3gpp, 5g, lte, 4g, protocol, wireless, networking]
---
# 3GPP Expert Skill

## Purpose
Turns Claude into a senior telecom consultant covering the full 3GPP ecosystem — 2G through 6G, all releases, protocol stacks, and deployment.

## Coverage
| Era | Releases | Key Technologies |
|---|---|---|
| 2G | Phase 1 – Rel-98 | GSM, GPRS, EDGE |
| 3G | Rel-99 – Rel-7 | UMTS, WCDMA, HSPA, HSPA+ |
| 4G | Rel-8 – Rel-14 | LTE, LTE-A, NB-IoT, C-V2X |
| 5G | Rel-15 – Rel-17 | NR, 5GC/SBA, NTN, RedCap |
| 5G-Adv | Rel-18 – Rel-19 | AI/ML, XR, Ambient IoT, MIMO |
| 6G | Rel-20 – Rel-21 | Sub-THz, ISAC, AI-native, digital twins |

## Example Questions Handled
- "Walk me through UE cell selection from power-on to RRC Connected"
- "What sequence is used for PSS in 5G NR?" (m-sequence, not Zadoff-Chu — common AI hallucination corrected)
- "Explain LTE vs 5G NR RRC state machines, including RRC_INACTIVE"
- "How does 5G's SUPI/SUCI protect against IMSI catchers?"
- "NSA vs SA options for LTE→5G migration"

## Install
```bash
# Claude Desktop
# Download 3gpp-expert.skill from Releases and open it

# Manual
cp -r 3gpp-expert ~/.claude/skills/3gpp-expert
```

## Integration Notes
- References: releases.md, phy-layer.md, working-groups.md
- PHY layer: correct PSS/SSS sequences per RAT (critical for avoiding hallucinations)
- Security: EPS-AKA vs 5G-AKA, SUPI/SUCI, IMSI catcher analysis
