# SOURCE MAP — powerplug.ai Hermes Agent rebuild

Date: 2026-04-17
Commit target: `powerplug.ai/Hermes Agent/2026-04-16/` on `maximoseo/webs-html-improvements-files`

## Live site sources (source of truth)

| Asset | Live URL | Use |
|---|---|---|
| Homepage | https://powerplug.ai/ | Logo, brand palette, meta description, hero language |
| Contact page | https://powerplug.ai/contact-us | Every CTA button href |
| Logo PNG | https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png | About the Author logo + floating Contact implicit brand link |
| LinkedIn | https://www.linkedin.com/company/powerplug-ltd | About the Author social |
| Facebook | https://www.facebook.com/PowerPlugLtd/ | About the Author social |
| X / Twitter | https://twitter.com/PowerPlugLtd | About the Author social |
| Email | info@powerplugltd.com | mailto in trust block |
| Phone | +1-646-751-7797 | tel: in trust block |
| Real customer reference | Clalit Health Services (mentioned on live site) | Trust-block attribution |

## Brand palette (pulled from live HTML, frequency-sorted)

| Hex | Usage |
|---|---|
| `#7238ce` | Primary purple (buttons, links, accents) |
| `#bc55ff` | Accent purple (gradients, hover) |
| `#131b3b` | Navy (headings, h1/h2/h3) |
| `#414042` | Body ink |
| `#6c6c6d` | Muted ink |
| `#f5f4f5` | Mist / surface |
| `#d8d8d9` | Border |

## Third-party sources (external links in body)

| URL | Why |
|---|---|
| https://www.energystar.gov/products/computers | Authoritative reference for endpoint energy efficiency guidance |
| https://www.iea.org/reports/energy-efficiency-2023 | Global energy-efficiency report cited in Did-You-Know block |

## Image sources (Unsplash, free-use with hotlink OK)

| Image | URL | alt |
|---|---|---|
| Hero | https://images.unsplash.com/photo-1558494949-ef010cbdcc31 | Rows of powered-on office workstations in a modern workspace |
| Pitfalls section | https://images.unsplash.com/photo-1518770660439-4636190af475 | Close-up of a PC motherboard showing CPU and cooling components |
| Rollout section | https://images.unsplash.com/photo-1573164713714-d95e436ab8d6 | IT operations team collaborating on rollout planning with laptops and whiteboard |

## Parallel agent versions reviewed

Current run did not deep-review sibling agent folders (Claude Code, Copilot, Gemini, agent-zero, CLAUDE CODE (Tim Claw Max)) because the rebuild prioritized speed and rule compliance over cross-agent synthesis. The Hermes Agent base files were used as the sole improvement foundation per user direction: "rebuild 3 files, improve last 3 upload files".

## Files rebuilt in place

| File | Old size | New size | Change |
|---|---|---|---|
| Improved_HTML_Template.html | 37,764 B | ~33,608 B | Full rebuild per 34 rules |
| Improved_N8N_Prompt.txt | 12,619 B | ~11,769 B | Full rebuild — 33-rule encoded |
| Improved_N8N_Workflow.json | 126,169 B | ~123,942 B | Surgical update of `Writing Blog` agent prompt; 63 node IDs preserved |
| SOURCE-MAP-2026-04-15.md | 3,819 B | THIS FILE | Full rewrite |
| SUMMARY-2026-04-15.md | 4,478 B | see file | Full rewrite |
| VALIDATION-NOTE-2026-04-15.md | 6,451 B | see file | Full rewrite with 34-row checklist |
