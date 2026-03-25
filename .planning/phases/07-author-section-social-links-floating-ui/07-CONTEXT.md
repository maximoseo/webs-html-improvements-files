# Phase 7: Author Section, Social Links & Floating UI - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Replace author stub with About the Author section (final section, logo, verified social links). Add floating Back to Top and Contact Us buttons. All data from hipsterstyle-discovery.json.

</domain>

<decisions>
## Implementation Decisions

### Author Section (locked by spec)
- MUST be the final section — nothing after it
- Logo image, visually centered and balanced
- Only verified real social profiles: Facebook (/HipsterBabyCollection) and Instagram (/hipster.style/)
- NO YouTube (confirmed absent), NO invented links
- Brand name: "היפסטר" (Hipster)
- Social area: elegant and non-spammy
- Brand-color hover on social icons

### Floating Buttons (locked by spec)
- Floating Back to Top: smooth scroll to #om-top anchor
- Floating Contact Us: link to real contact (phone: 052-9767667 or site contact page)
- Professional, minimal, do not overlap content
- No duplication of existing floating UI actions
- On tablet/mobile: resize/reposition to avoid obstructing content

### Hover States (locked by spec)
- CTA button: premium professional hover (HOVER-03)
- Social links: network brand-color hover — Facebook #1877F2, Instagram gradient or #E4405F (HOVER-04)

### Claude's Discretion
- Author section background color and border styling
- Floating button exact positioning (bottom-right corner typical)
- Social icon implementation (Unicode/SVG inline or text labels)
- Contact button destination (phone tel: link vs contact page)

</decisions>

<code_context>
## Existing Code Insights

### Discovery Data
- hipsterstyle-discovery.json has: brand name, logo URL, social profiles (FB + IG), contact info
- Facebook: https://facebook.com/HipsterBabyCollection
- Instagram: https://instagram.com/hipster.style/
- Phone: 052-9767667, Email: info@hipsterstyle.co.il

### Current Template
- Has author stub section ready for replacement
- Template uses inline-block + percentage layout
- Accent color: #c8a97e, bg: #f9f6f1, border: #e8e0d4

</code_context>

<specifics>
## Specific Ideas

Use brand logo from Supabase if available, otherwise use text-based author section.

</specifics>

<deferred>
## Deferred Ideas

None

</deferred>
