# RISK REPORT
Date: 2026-04-20

## Security Review

No API keys, secrets, or credentials were found in any of the 35 repos processed.
No secrets were committed or stored in any skill files created.
All API key references in skill files use env var patterns (e.g. GEMINI_API_KEY, FAL_KEY).

## Skills with API Key Requirements
| Skill | Required Credential | Risk |
|-------|---------------------|------|
| shopify-admin-skills | SHOPIFY_ACCESS_TOKEN | Low - standard OAuth token |
| logo-generator-svg | GEMINI_API_KEY | Low - Google AI API |
| seedance-video-gen | FAL_KEY | Low - Fal AI API |
| email-campaigns-html | RESEND_API_KEY | Low - email service |
| friday-autonomous-ai | Multiple (Telegram, ElevenLabs, etc.) | Medium - complex setup |
| lich-skills-personal | TAVILY_API_KEY, GEMINI_API_KEY | Low |

## Skills with Known Limitations
| Skill | Limitation |
|-------|-----------|
| jetpack-compose-audit | May drift as Compose Compiler updates - verify Kotlin 2.0.20+ |
| material-3-md | M3 Expressive only on Compose, NOT available on Web |
| paper-finder-ml | Training knowledge misses 2024-2025 papers - requires web search access |
| 3gpp-telecom-expert | PSS in 5G NR uses m-sequence, NOT Zadoff-Chu - known AI hallucination trap |
| android-skills-mcp | Bundled snapshot may lag behind upstream android/skills |
| friday-autonomous-ai | Cron jobs have 7-day TTL - requires watchdog to prevent expiration |
| seedance-video-gen | Max 5 reference images - quality degrades above limit |

## Dependencies That May Not Be Available
| Skill | Dependency | Risk |
|-------|-----------|------|
| ai-life-obsidian | yt-dlp, ffmpeg, pandoc, pdftotext | Must be installed manually |
| ai-life-obsidian (local transcription) | mlx_whisper, pyannote.audio (Mac MPS) | Mac only for local path |
| logo-generator-svg | cairosvg, Pillow, google-genai | Python deps via pip |
| engineering-figure-banana | Windows PowerShell scripts tested | macOS expected to work |
| marp-slides-builder | MARP for VS Code extension | VS Code dependency |
| html-ppt-studio | npx install | Node.js required |
| android-skills-mcp | Node.js 20+ | Runtime requirement |

## Repos with Security-Relevant Patterns (No Actual Secrets Found)
| Repo | Pattern | Status |
|------|---------|--------|
| missingus3r/friday-showcase | .env file pattern for Telegram bot token | No actual token found |
| LichAmnesia/lich-skills | gitleaks integration mentioned | Indicates security awareness |
| op7418/logo-generator-skill | .env.example template provided | No actual API key exposed |

## Repos That Could Not Be Fully Fetched
All 35 repos were successfully fetched. No access errors.
spencerpauly/awesome-cursor-skills README was truncated at 25KB - partial read.
Content sufficient for classification; no SKILL.md created (aggregator only).

## Risk Level Summary
- Overall risk: LOW
- No secrets found or created
- Skills reference env vars, not inline credentials
- Biggest risk: dependency availability on target machines
