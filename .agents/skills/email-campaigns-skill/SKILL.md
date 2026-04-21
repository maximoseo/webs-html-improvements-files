---
name: Email Campaigns (HTML Email + Resend)
source: https://github.com/irinabuht12-oss/email-campaigns-claude
category: Automation
purpose: Build and send beautiful HTML email campaigns using Resend — frost-glass cards, video blocks, CTA buttons, GIF pipeline, drip sequences
when_to_use: When creating marketing emails, launch announcements, or drip sequences that need polished HTML templates
tags: [email, html, resend, marketing, campaigns, automation, design]
---
# Email Campaigns Skill

## Purpose
Complete pattern for building and sending modern marketing emails with reusable design blocks and the Resend send pipeline.

## Design System
| Element | Value |
|---|---|
| Card corner radius | 3px |
| Card shadow | `0 2px 8px rgba(24,24,27,.06), 0 8px 24px rgba(24,24,27,.04)` |
| Typography | 26px / 15px / 13px |
| Max card width | 560px |
| Primary action | Black pill CTA, repeated 2x |
| Background | Soft sky-blue gradient + 6% SVG noise |

## Design Blocks Available
- Hero image with overlay text
- Frost-glass logo cards (translucent, backdrop-blur)
- Video thumbnail blocks with blurred color backgrounds
- Dark pill CTA buttons (repeated 2x)
- Sponsor/partner logo rows

## GIF Pipeline
```bash
ffmpeg -i input.mp4 -vf fps=15,scale=480:-1 -loop 0 output.gif
# → email-safe GIF: under 2MB, 15fps, trimmed
```

## Resend Integration
```bash
# Single send
resend emails send --to user@example.com --from you@yourdomain.com \
  --subject "Subject" --html "$(cat email.html)"

# Batch send or drip via webhooks — see SKILL.md
```

## Install
```bash
mkdir -p ~/.claude/skills/email-campaigns
cp email-campaigns-claude/SKILL.md ~/.claude/skills/email-campaigns/SKILL.md
```
Then: `/email-campaigns` in any session.

## Integration Notes
- Asset hosting: use Vercel/Netlify `public/` as free email CDN
- Pre-send checklist: absolute URLs, preheader, alt text, client testing
- Example real email in `examples/claude-connector.html`
