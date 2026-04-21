---
name: Spider King Reverse Engineering
source: https://github.com/aoyunyang/spider-king-skill
category: Tools
purpose: Web protocol reverse engineering skill — converts browser-dependent hostile web clients into stable, reproducible pure-protocol collectors
when_to_use: When web scraping fails due to dynamic parameters, signatures, encryption, WebSocket sessions, or browser-only requests
tags: [reverse-engineering, web-scraping, protocol-recovery, anti-bot, python-collector]
---

# Spider King Reverse Engineering

## Purpose
Reverse engineering methodology for web protocol recovery. Not browser automation — converts browser-dependent targets into stable Python protocol collectors without Playwright/Selenium as final delivery.

## When To Use
- Page code shows one API, network traffic uses another
- Requests have sign/token that gets rewritten before sending
- Responses need decoding, decryption, character mapping, or binary parsing
- Getting 403/412/429 on protocol replay
- Signatures, cookies, challenge scripts, WASM, WebSocket sessions are tangled together
- Final delivery must run WITHOUT a browser

## How To Apply
**5-step methodology:**
1. **Startup Gate**: Environment check, target family classification (signer-gated/verifier-gated/decode-gated/session-gated), delivery intent declaration
2. **Dual-Tool Reconnaissance**: chrome-devtools (page state, network) + js-reverse (initiator, source search, wrapper tracking) — lightweight first pass
3. **Identify True Dynamic State**: May be rotating cookies, page-specific headers, request wrapper fields, server-returned bootstrap JS, WASM exports, response decode chains
4. **Offline Reconstruction**: Python-first → Python + tiny JS helper → Python + tiny WASM helper → Python + local bootstrap executor
5. **Repeatability Verification**: Same logic succeeds 2-3 times, pagination advances, dynamic state regenerates

**4 helper scripts:**
- `check_reverse_env.py`: Environment check (Python, Node, npm, curl, git)
- `crypto_fingerprint.py`: Classify suspicious output (digest, Base64, custom encoding)
- `protocol_diff.py`: Compare request/response samples, find true dynamic fields
- `scaffold_reverse_project.py`: Generate Python-first project skeleton

## Examples
- 403 on page 2 but not page 1 → protocol_diff.py to find differing field → reconstruct signature
- Response is garbled → crypto_fingerprint.py identifies XOR cipher → Python decryption added

## Integration Notes
- Uses chrome-devtools and js-reverse MCP tools
- Final delivery: Python collector only, no browser dependency
- Repeatability is the completion criterion — not "it worked once"
