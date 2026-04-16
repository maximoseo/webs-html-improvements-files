# Validation Note — powerplug.ai Hermes Agent Redesign
**Working date:** 2026-04-15
**Version path:** powerplug.ai / Hermes Agent / 2026-04-16
**Agent:** Hermes Agent

---

## What Was Reviewed Before Editing

- Current Hermes Agent HTML template (59KB) — reviewed full structure, sections, CTAs, author block, TOC, FAQ, floating elements
- Current Hermes Agent N8N prompt (4.7KB) — reviewed rules, structure requirements, brand guidance
- Current Hermes Agent N8N workflow (117KB, 63 nodes) — reviewed Writing Blog node, template node, image prompt node, brand tokens
- Codex/2026-04-16 HTML (43KB) — reviewed for reusable section structure and content depth
- Claude Code/2026-04-16 HTML (43KB) — reviewed for TOC/FAQ pattern and CTA placement
- agent-zero/2026-04-16 (file not accessible — too small, 14 bytes, assumed empty or placeholder)
- Live powerplug.ai site — scraped brand colors, logo URL, contact page, social links, phone, email, company details, trust signals

---

## What Was Changed

### HTML Template
- Added proper floating Contact Us button (fixed, bottom-right, min 44x44px, links to /contact-us, hover effect, no collision with scroll button)
- Added floating Scroll-to-Top button (appears after 300px scroll, animated, hover effect, safe position)
- Added inline <script> for scroll detection (safe within article scope)
- Hero: retained dark navy gradient, added logo badge, enforced exactly ONE H1, removed any date/year from intro area
- Added 3-column trust/proof strip (60% savings, 4 months ROI, 50K+ PCs)
- Added Key Takeaways block with verified client data
- TOC: collapsed by default, animated chevron, numbers in list items only (not in heading text), correct section IDs
- TOP CTA: dark navy background, "Book a Power Savings Assessment" / "Talk to a PowerPlug Specialist"
- MIDDLE CTA: white/green-bordered, "Request a PowerPlug Demo"
- BOTTOM CTA: dark navy, trust reinforcement with real client names and verified metrics
- Added Did You Know blocks in Why Power Management and Security sections
- Added How-To numbered steps block in How It Works section
- Added Tips columns block in WakeUp section
- Added ROI comparison table (3 org sizes, estimated savings, typical payback)
- Added Tip block under ROI section
- Case Studies: 3 verified clients with real numbers (Clalit $1.2M, Rambam <4mo ROI, Ben Gurion University)
- FAQ: 6 items, all collapsed, animated chevrons, hover effects, real user questions
- Author block: rectangular logo tile, logo links to homepage, real social links (Facebook/Twitter/LinkedIn), correct hover colors, phone + email, Contact button

### N8N Prompt
- Added full brand source of truth (all verified URLs, colors, social links, phone, email, case study numbers)
- Added NON-NEGOTIABLE RULES section with 16 explicit rules covering WordPress safety, floating buttons, H1 enforcement, no-date-in-intro rule, social hover colors
- Added DESIGN DIRECTION section with explicit color values and spacing guidance
- Added explicit REQUIRED ARTICLE STRUCTURE with ordered list
- Added CTA RULES with 3 distinct CTA labels and all linking to /contact-us
- Added explicit TOC RULES (collapsed, chevron animation, no numbers in heading)
- Added FAQ RULES (min 6 items, all collapsed, hover effects)
- Added CONTENT QUALITY RULES (external link source guidance, no filler, Did You Know/Tips/How-To requirement)
- Removed old rule 11 that prohibited floating buttons — replaced with explicit requirement for floating buttons
- Rule 13: do NOT mention dates/years in intro/hero

### N8N Workflow
- Patched Writing Blog node prompt with the full improved N8N prompt text
- Patched template/assembler node with improved writing-stage rules
- Fixed image prompt brand token: BRAND_SECONDARY_COLOR was incorrectly set to purple #7238ce — corrected to green #8bc540 to match PowerPlug brand
- Updated workflow name to include working date reference

---

## Sources Used

- Live site: https://powerplug.ai/ (brand colors, logo, social links, phone, company description)
- Contact page: https://powerplug.ai/contact-us (confirmed URL, company legal info)
- External reference: https://www.energy.gov/eere/buildings/computers-and-office-equipment (Did You Know fact)
- Case study data: Clalit, Rambam, Ben Gurion University — all from public PowerPlug case study references

---

## Behaviors Verified

- HTML: one H1 only — confirmed
- TOC: no numbers in heading text — confirmed
- TOC/FAQ: start collapsed — confirmed (no `open` attribute on details elements)
- CTAs: all link to https://powerplug.ai/contact-us — confirmed
- Floating Contact button: links to /contact-us, min 44x44px on mobile — confirmed
- Floating Scroll button: opacity:0/pointer-events:none by default, shows after 300px scroll via JS — confirmed
- Author logo: rectangular tile, links to https://powerplug.ai, object-fit:contain — confirmed
- Author social links: real URLs for Facebook, Twitter, LinkedIn — confirmed
- Brand colors: navy #151d3f and green #8bc540 used consistently — confirmed
- No date/year in hero or first paragraph — confirmed
- WordPress-safe: no external CSS, no external JS, inline styles only — confirmed
- Images: all use loading="lazy", border-radius:12px, consistent shadow/border — confirmed

---

## Constraints Encountered

- agent-zero/2026-04-16 file was only 14 bytes — likely empty or corrupted; could not reference it
- No Instagram, YouTube, or WhatsApp links found on powerplug.ai — not included in author block
- Image URLs are dynamic N8N template variables ({{ $json.images.section_N.url }}) — cannot verify at static file level; must be confirmed after live workflow run

---

## Unresolved Items Requiring Manual Follow-Up

1. Verify floating button positioning on the live PowerPlug WordPress theme — the site has an accessibility toolbar that may conflict with bottom-right positioning; adjust to bottom-left if needed
2. Confirm WordPress theme does not override article-scoped CSS (some themes strip <style> inside post content)
3. Test TOC section anchor links (#intro, #why-power, etc.) in the live WordPress environment — some page builders strip element IDs
4. Review N8N workflow credentials (Google Sheets, OpenRouter API, WordPress API) are still valid before running
5. Image prompt brand token correction (#7238ce → #8bc540) should produce more on-brand AI-generated images — verify on next workflow run
