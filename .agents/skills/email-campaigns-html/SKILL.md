---
name: HTML Email Campaigns Builder
source: https://github.com/irinabuht12-oss/email-campaigns-claude
category: Automation
purpose: Complete pattern for building and sending modern HTML marketing emails with Resend — frost-glass cards, video blocks, CTA buttons, GIF optimization, and Resend pipeline
when_to_use: When creating HTML email campaigns, marketing emails, or transactional emails with modern design patterns
tags: [email, html, marketing, resend, campaign, design, gif, cta]
---

# HTML Email Campaigns Builder

## Purpose
Claude Code skill encoding the complete pattern for modern marketing email production. Includes asset hosting, reusable design blocks, GIF optimization, and Resend send pipeline.

## When To Use
- Building launch emails, newsletters, drip sequences
- Creating hero image, frost-glass card, or video thumbnail email blocks
- Setting up Resend for single-send, batch, or drip with webhooks

## How To Apply
**Install:**
```bash
mkdir -p ~/.claude/skills/email-campaigns
cp SKILL.md ~/.claude/skills/email-campaigns/SKILL.md
```

**Design tokens:**
| Element | Value |
|---------|-------|
| Card corner radius | 3px |
| Card shadow | 0 2px 8px rgba(24,24,27,.06), 0 8px 24px rgba(24,24,27,.04) |
| Typography | 26px / 15px / 13px scale |
| Max card width | 560px |
| Primary CTA | Black pill, repeated 2x |
| Background | Soft sky-blue gradient + 6% SVG noise |

**Asset hosting:** Vercel/Netlify public/ folder as email CDN (free, no Cloudinary cost)

**GIF pipeline:** `ffmpeg` one-liners: MP4 → email-safe GIF (under 2MB, 15fps, sensibly trimmed)

**Pre-send checklist:** absolute URLs, preheader text, alt text, email client testing

## Examples
- "Build a product launch email with frost-glass logo cards and a video thumbnail block"
- "Set up a 3-email drip sequence with Resend webhooks"

## Integration Notes
- Invoke via `/email-campaigns` in Claude Code session
- Resend API key required for send functionality
- All URLs must be absolute for email clients
- Test across email clients before sending
