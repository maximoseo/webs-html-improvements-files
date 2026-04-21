# HTML REDESIGN MEGA SKILL UPGRADE

**Name:** HTML Template Redesign Mega Skill
**Version:** 2.0.0
**Context:** This skill is MANDATORY when an agent is tasked with fixing, redesigning, or restructuring HTML templates, particularly for content-heavy, conversion-oriented, or WordPress-safe assets.

## CORE DIRECTIVES
1. **Never delete existing capabilities.** Always expand and refine.
2. **Preserve exact content.** Never use placeholders or `lorem ipsum`. Use actual `src` URLs and actual text.
3. **No external dependencies.** Keep CSS inline or in scoped `<style>` tags. Do not rely on external JS libraries unless instructed. Keep scripts wrapped in IIFE.

## SUB-SKILLS & SYSTEMS

### 1. Responsive Layout Fixer
- **Rule:** Layouts must natively scale across 320px (mobile), 768px (tablet), and 1024px+ (desktop) viewports.
- **Action:** Utilize `minmax`, `clamp()`, and flexbox `gap` properties. Avoid hardcoded `width` or `height` unless strictly necessary (e.g., floating tap targets).

### 2. Dashboard UI Cleaner & Prompt Studio UX Improver
- **Rule:** Administrative and dashboard interfaces require high contrast, clear data hierarchies, and reduced visual noise.
- **Action:** Apply soft background tones (`#f8fafc`, `#f1f5f9`), distinct borders (`#e2e8f0`), and use whitespace for grouping.

### 3. Keyword Research UI Optimizer
- **Rule:** Data-heavy UI components must prioritize readability.
- **Action:** Ensure tables use `min-width`, `white-space: nowrap` for headers, and alternating row colors for massive datasets.

### 4. Modal / Popup UX System
- **Rule:** Modals must have a visible backdrop (`rgba(0,0,0,0.5)`), z-index > 9000, and a clear, accessible close mechanism (`[x]`).
- **Action:** Include ARIA attributes (`role="dialog"`, `aria-modal="true"`) and focus trapping logic if JS is permitted.

### 5. Button & CTA Hierarchy Fixer + Conversion CTA Engine
- **Rule:** Only ONE primary CTA style per view. Secondary and tertiary buttons must be visually distinct.
- **Action:** Primary buttons should use high-contrast brand colors with `transform: translateY(-2px)` and `box-shadow` on hover. Insert mid-article and end-of-article conversion blocks naturally.

### 6. Box / Row / Alignment System
- **Rule:** Adhere to strict 4px or 8px baseline grids.
- **Action:** Margins and padding should be multiples of 4 (e.g., 8px, 16px, 24px, 32px, 64px).

### 7. WordPress-Safe HTML Generator + HTML & N8N Sync Engine
- **Rule:** Output must be compatible with Gutenberg custom HTML blocks or N8N injection.
- **Action:** Avoid `<html>`, `<head>`, or `<body>` tags if generating a partial. Do not inject conflicting generic CSS resets.

### 8. RTL / Hebrew Layout Engine
- **Rule:** Right-to-Left languages require specific directional handling.
- **Action:** Inject `dir="rtl"` on the root container. Ensure padding/margins are logically mapped (e.g., icons placed with `margin-left` instead of `margin-right` relative to text). 

### 9. TOC / FAQ Interaction System
- **Rule:** TOC and FAQ must be natively collapsible without complex JS.
- **Action:** Use `<details>` and `<summary>` tags. Remove numeric prefixes from TOC items. Place the TOC immediately after the first introductory paragraph or image.

### 10. Content Spacing Optimizer
- **Rule:** Vertical rhythm dictates reading flow.
- **Action:** `h2` elements need `margin-top: 4rem` and `margin-bottom: 1.5rem`. Paragraphs need `line-height: 1.8` and `margin-bottom: 1.2rem`.

### 11. Author / Trust Section Builder
- **Rule:** Articles must include a professional, branded author block.
- **Action:** Include the company logo linked to the homepage, real social media links with brand-specific hover colors, and trust signals (years of experience, customer counts).

### 12. Floating Buttons System
- **Rule:** Floating interactive elements must not overlap readable content or each other.
- **Action:** 
  - *Contact Us:* Fixed bottom (e.g., `bottom: 16px`), 44x44px tap target.
  - *Scroll to Top:* Hidden by default, appears after 300px scroll (`bottom: 76px`), smooth transitions.

### 13. Accessibility & Contrast Fixer
- **Rule:** Ensure WCAG AA compliance.
- **Action:** No text over low-contrast backgrounds. Hover states must not drop contrast below minimum ratios. All interactive elements need `aria-label` or visible text. Enforce EXACTLY ONE `<h1>` tag in the document.

---
**Usage:** Load this skill whenever a user requests an HTML redesign, CSS fix, or WP/N8N template upgrade. Evaluate the output strictly against the 13 sub-skills above before finalizing.
