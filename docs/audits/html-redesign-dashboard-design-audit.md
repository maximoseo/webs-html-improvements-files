# HTML Redesign Dashboard Design Audit

**Audited URL:** https://html-redesign-dashboard.maximo-seo.ai/  
**Captured at:** 2026-04-25T19:03:09Z  
**Viewports reviewed:** Desktop 1440×1100, Tablet 768×1050, Mobile 375×950  
**Evidence directory:** `output/playwright/dashboard-design-audit/`  
**State inventory:** `output/playwright/dashboard-design-audit/audit-state.json`  
**Evaluation dimensions:** layout, spacing, typography, color/contrast, alignment, responsiveness, hierarchy, affordance, consistency, accessibility.

## Priority definitions

- **P0:** Critical usability/accessibility/blocking issues.
- **P1:** Important design/usability problems that materially reduce polish, speed, or accessibility.
- **P2:** Non-blocking improvements and refinements.

## Executive summary

The production dashboard is stable enough for authenticated navigation and screenshot capture across the main product areas. The recent main-menu override is present in production on desktop: the desktop tab navigation measures `820×44`, shows the `Main menu` label, and active tabs use the new blue/purple/green gradient styling. No horizontal page overflow was detected in the automated viewport inventory.

The main design debt is not a single broken page; it is accumulated UI density and inconsistent responsive behavior:

1. **Mobile/tablet navigation hides the upgraded main menu entirely.** At 768px and 375px, the main tab nav is `display:none` and the user sees the drawer/hamburger pattern instead. This explains why visual main-menu work can look unchanged on smaller devices.
2. **Several tap targets are under the 44px accessibility guideline.** The recurring drawer items are about `35–37px` tall; the Search control is about `32–34px`; notification/action controls are also below target size.
3. **Settings is extremely long.** It reaches `4371px` desktop, `6931px` tablet, and `7612px` mobile — around `8×` the mobile viewport. This creates fatigue and makes settings hard to scan or operate.
4. **Global visual hierarchy is still mixed.** The header/navigation layer is now polished, but many content modules retain older dense cards/forms, mixed light/dark surfaces, small text, and inconsistent control treatments.
5. **High control density is systemic.** The DOM inventory reports 334–365 buttons per tab because many controls/drawer items are globally present. Even when not all are visible at once, the interaction model needs pruning and clearer grouping.

**P0 issues found:** 0  
**P1 issues found:** 6  
**P2 issues found:** 7

## Audit coverage

### Screenshots captured

| Area | Desktop | Tablet | Mobile |
|---|---|---|---|
| Projects | `tab-projects-desktop.png` | `tab-projects-tablet.png` | `tab-projects-mobile.png` |
| N8N Fixer | `tab-n8n-fixer-desktop.png` | `tab-n8n-fixer-tablet.png` | `tab-n8n-fixer-mobile.png` |
| Skills Radar | `tab-skills-radar-desktop.png` | `tab-skills-radar-tablet.png` | `tab-skills-radar-mobile.png` |
| KW Research | `tab-kw-research-desktop.png` | `tab-kw-research-tablet.png` | `tab-kw-research-mobile.png` |
| Tasks | `tab-tasks-desktop.png` | `tab-tasks-tablet.png` | `tab-tasks-mobile.png` |
| Analytics | `tab-analytics-desktop.png` | `tab-analytics-tablet.png` | `tab-analytics-mobile.png` |
| Settings | `tab-settings-desktop.png` | `tab-settings-tablet.png` | `tab-settings-mobile.png` |
| Global search | `modal-global-search-desktop.png` | — | — |
| Mobile drawer | — | — | `mobile-drawer-open.png` |
| Login | `login-desktop.png` | — | — |

### Automated layout inventory

| Device | Tab | Screenshot | Body height | Horizontal overflow | Nav state | Small tap targets | Cards / Tables / Buttons |
|---|---|---|---:|---|---|---:|---|
| desktop | Projects | `tab-projects-desktop.png` | 1563 | false | `flex 820×44` | 20 | 11 / 0 / 335 |
| desktop | N8N Fixer | `tab-n8n-fixer-desktop.png` | 2097 | false | `flex 820×44` | 20 | 0 / 0 / 334 |
| desktop | Skills Radar | `tab-skills-radar-desktop.png` | 1571 | false | `flex 820×44` | 20 | 0 / 0 / 343 |
| desktop | KW Research | `tab-kw-research-desktop.png` | 1871 | false | `flex 820×44` | 20 | 5 / 0 / 342 |
| desktop | Tasks | `tab-tasks-desktop.png` | 1100 | false | `flex 820×44` | 20 | 0 / 0 / 342 |
| desktop | Analytics | `tab-analytics-desktop.png` | 1786 | false | `flex 820×44` | 20 | 7 / 0 / 342 |
| desktop | Settings | `tab-settings-desktop.png` | 4371 | false | `flex 820×44` | 20 | 7 / 1 / 365 |
| tablet | Projects | `tab-projects-tablet.png` | 2866 | false | `none 0×0` | 20 | 11 / 0 / 365 |
| tablet | N8N Fixer | `tab-n8n-fixer-tablet.png` | 2493 | false | `none 0×0` | 20 | 0 / 0 / 365 |
| tablet | Skills Radar | `tab-skills-radar-tablet.png` | 1993 | false | `none 0×0` | 20 | 0 / 0 / 365 |
| tablet | KW Research | `tab-kw-research-tablet.png` | 2154 | false | `none 0×0` | 20 | 5 / 0 / 365 |
| tablet | Tasks | `tab-tasks-tablet.png` | 1135 | false | `none 0×0` | 20 | 0 / 0 / 365 |
| tablet | Analytics | `tab-analytics-tablet.png` | 2037 | false | `none 0×0` | 18 | 7 / 0 / 365 |
| tablet | Settings | `tab-settings-tablet.png` | 6931 | false | `none 0×0` | 20 | 7 / 1 / 365 |
| mobile | Projects | `tab-projects-mobile.png` | 3229 | false | `none 0×0` | 20 | 11 / 0 / 365 |
| mobile | N8N Fixer | `tab-n8n-fixer-mobile.png` | 2627 | false | `none 0×0` | 20 | 0 / 0 / 365 |
| mobile | Skills Radar | `tab-skills-radar-mobile.png` | 2476 | false | `none 0×0` | 20 | 0 / 0 / 365 |
| mobile | KW Research | `tab-kw-research-mobile.png` | 2536 | false | `none 0×0` | 20 | 5 / 0 / 365 |
| mobile | Tasks | `tab-tasks-mobile.png` | 1175 | false | `none 0×0` | 20 | 0 / 0 / 365 |
| mobile | Analytics | `tab-analytics-mobile.png` | 2689 | false | `none 0×0` | 18 | 7 / 0 / 365 |
| mobile | Settings | `tab-settings-mobile.png` | 7612 | false | `none 0×0` | 20 | 7 / 1 / 365 |

## Global issues

### P1-01 — Main menu upgrade is desktop-only at current breakpoints

**Evidence:** `audit-state.json`, all tablet/mobile screenshots.  
**Observed:** Desktop has the final upgraded nav (`flex`, `820×44`, `"Main menu"`). Tablet and mobile switch the nav to `display:none` and rely on the mobile drawer.  
**Impact:** On a tablet or narrow laptop, the user will not see the redesigned main menu, which can make production appear unchanged even after a correct deploy/cache clear.  
**Recommendation:** Add an intermediate navigation mode for 821–1024px, or apply the same visual language to the mobile drawer trigger/drawer header so the redesign is visible across devices.

### P1-02 — Tap targets are consistently below 44px

**Evidence:** `smallTapTargets` in `audit-state.json`.  
**Observed examples:**

- Mobile/tablet drawer items: about `287×37`.
- Desktop tab buttons: about `79–121×34`.
- Search control: about `32×32` or `32×34`.
- Notification control: about `36×34` or `36×40`.
- Brand link/icon: `36×36` on mobile.

**Impact:** Lower touch accuracy and weaker accessibility, especially on phones and tablets.  
**Recommendation:** Set minimum interactive height to `44px` for drawer items, compact icon buttons, and tab buttons. Preserve visual compactness with internal alignment rather than reducing hit area.

### P1-03 — Mobile/tablet pages are too long and require excessive scrolling

**Evidence:** body-height inventory.  
**Most severe pages:**

- Settings mobile: `7612px`, about `8×` the mobile viewport.
- Settings tablet: `6931px`, about `6.6×` the tablet viewport.
- Projects mobile: `3229px`, about `3.4×` the mobile viewport.
- Analytics mobile: `2689px`, about `2.8×` the mobile viewport.
- N8N Fixer / KW Research / Skills Radar mobile: all about `2.6–2.8×` viewport height.

**Impact:** Hard to understand page structure, difficult to return to important controls, and poor operational speed for employees.  
**Recommendation:** Convert long pages into grouped sections with collapsible panels, sticky section index, and “most-used first” ordering. Settings should be split into categories or tabs.

### P1-04 — Mixed visual systems remain after the header/menu polish

**Evidence:** captured screenshots and text-style samples in `audit-state.json`.  
**Observed:** Header and desktop nav now use a modern dark/glass style, while many inner forms/cards retain older mixed light/dark surfaces, small labels, and inconsistent button styles.  
**Impact:** The dashboard feels partially redesigned rather than consistently productized.  
**Recommendation:** Define one reusable surface system for cards, forms, toolbar rows, status chips, and primary/secondary/destructive buttons; apply it by component class rather than page-specific overrides.

### P1-05 — High global control count increases complexity

**Evidence:** button counts: 334–365 per tab.  
**Observed:** Many buttons and drawer controls are present in the DOM on every tab. While some are hidden/global controls, the high count suggests repeated controls and dense interaction surfaces.  
**Impact:** More risk for inconsistent styling, keyboard/focus noise, and operational confusion.  
**Recommendation:** Separate global drawer/header controls from tab-specific controls in the audit instrumentation, then reduce visible actions per page using progressive disclosure: primary action, secondary menu, advanced collapsible section.

### P1-06 — Settings page lacks enough information architecture

**Evidence:** `tab-settings-desktop.png`, `tab-settings-tablet.png`, `tab-settings-mobile.png`; body heights.  
**Observed:** Settings is the longest page by a large margin and contains multiple cards/table/forms in one long vertical flow.  
**Impact:** Hard for employees to locate provider/auth/model/workflow settings quickly.  
**Recommendation:** Split Settings into clear categories: Providers, Authentication, GitHub/Render, N8N, Models, Maintenance. Add a sticky local section nav and collapsible advanced sections.

## Per-tab issues

### Projects

- **P1:** Long mobile/tablet scrolling: `3229px` mobile and `2866px` tablet.
- **P2:** Project cards and action rows should use stronger grouping: primary actions should be visible, advanced actions should move behind a menu.
- **P2:** The automated state returned an empty `visiblePage` for Projects. This may be instrumentation rather than UI, but the Projects page should expose a stable page id/state for testing.

### N8N Fixer

- **P1:** Dense form layout and long page height: `2627px` mobile, `2493px` tablet, `2097px` desktop.
- **P2:** Fields, status controls, and action buttons need clearer hierarchy: “Analyze & Fix Workflow” should remain dominant while secondary diagnostics/import actions should be grouped.

### Skills Radar

- **P2:** Medium-long mobile page (`2476px`) and multiple status/action elements; good candidate for compact summary cards and collapsible source details.
- **P2:** Ensure external/source badges have consistent contrast and spacing with the rest of the dashboard surface system.

### KW Research

- **P1:** Important controls and setup fields compete for attention; the page is long on all devices (`1871px` desktop, `2536px` mobile).
- **P2:** Keep “Test Connection”, model selection, required fields, and run actions in a single guided stepper/sequence to reduce cognitive load.

### Tasks

- **P2:** Lowest page-height risk (`1100px` desktop, `1175px` mobile), but still inherits the global tap-target and navigation issues.
- **P2:** Can serve as the baseline for simpler page structure when refactoring heavier tabs.

### Analytics

- **P1:** Mobile/tablet height is high (`2689px` mobile, `2037px` tablet) and multiple cards can create a dashboard-within-dashboard feeling.
- **P2:** Prioritize key metrics above the fold, collapse secondary diagnostic panels, and standardize chart/card spacing.

### Settings

- **P1:** The most urgent design cleanup target due to extreme page height and many controls.
- **P1:** Needs category navigation and advanced-section collapse.
- **P2:** The single table on the page should be checked for mobile readability and sticky/stacked behavior.

## Per-device issues

### Desktop 1440px

**Status:** Mostly stable. No horizontal overflow detected. The main-menu redesign is visible and active styles are applied.

**Issues:**

- **P1:** Desktop tab buttons are still below 44px high (`34px`).
- **P1:** Settings is too long (`4371px`).
- **P2:** Main-menu polish outpaces inner content polish, creating an inconsistent first impression after navigation.

### Tablet 768px

**Status:** No horizontal overflow detected. Layout stacks correctly but becomes very long.

**Issues:**

- **P1:** Desktop main menu is hidden (`display:none`), so the redesign is not visible at tablet width.
- **P1:** Drawer items are below 44px touch target height.
- **P1:** Settings is extremely long (`6931px`).
- **P2:** Consider a tablet-specific compact tab strip rather than full mobile drawer behavior.

### Mobile 375px

**Status:** No horizontal overflow detected. Mobile drawer capture exists.

**Issues:**

- **P1:** Drawer items and header icon buttons are below recommended tap-target sizes.
- **P1:** Settings reaches `7612px`, making it the highest-friction page.
- **P1:** Most functional tabs exceed `2.5×` viewport height.
- **P2:** Add sticky local action bars or “Back to top”/section jump controls for long workflows.

## Accessibility notes

- **No P0 accessibility blocker was detected from the automated inventory.**
- **Tap targets:** Several controls are below the 44px guideline. This is the strongest accessibility issue.
- **Keyboard/focus risk:** The high number of globally present buttons may create noisy keyboard navigation unless hidden controls are correctly removed from tab order with `display:none`, `inert`, or equivalent state.
- **Contrast risk:** Text samples show a mixture of dark labels, light surfaces, dark surfaces, and muted foreground colors. Run a color contrast audit after component standardization.
- **Skip link:** Present, but appears in overflow detection because it is positioned off-screen until focus. That is expected; verify focus state visually in a dedicated keyboard QA pass.
- **Mobile drawer:** Verify `aria-expanded`, `aria-controls`, focus trap, Escape-close, and return focus to trigger.

## Recommended remediation order

### Batch 1 — Make the navigation redesign visible and accessible everywhere

1. Raise desktop tab, mobile drawer, search, notification, and compact icon hit areas to minimum `44px`.
2. Apply the main-menu visual language to tablet/mobile drawer trigger and drawer header.
3. Consider a tablet-specific compact tab strip for 821–1024px and possibly 768px landscape.
4. Add/verify drawer accessibility attributes and focus behavior.

### Batch 2 — Split and simplify Settings

1. Add Settings category nav: Providers, Auth, GitHub/Render, N8N, Models, Maintenance.
2. Collapse advanced/rare settings by default.
3. Keep critical connection/status controls above the fold.
4. QA mobile height target: reduce from `7612px` to below ~`3500–4000px` if possible.

### Batch 3 — Reduce page density on Projects, N8N Fixer, KW Research, Analytics

1. Identify one primary action per page.
2. Move secondary/advanced actions into grouped menus or collapsible panels.
3. Standardize form/card spacing and titles.
4. Add local sticky action bars only where users need persistent run/save controls.

### Batch 4 — Component-system cleanup

1. Create shared classes/tokens for surfaces, cards, toolbars, chips, buttons, form fields, and section headers.
2. Replace page-specific one-off styles with shared component classes.
3. Run screenshots again across desktop/tablet/mobile.
4. Update regression tests to assert nav visibility/tap-target minimums and no horizontal overflow.

## Verification notes

- Production authenticated capture completed.
- Screenshot coverage: 25 files.
- Referenced screenshots exist in `output/playwright/dashboard-design-audit/`.
- No horizontal overflow detected in the captured desktop/tablet/mobile states.
- Desktop main-menu final override is present in computed state.
- Tablet/mobile intentionally hide the desktop nav and should be treated as a separate design path.

## Files produced

- `docs/audits/html-redesign-dashboard-design-audit.md`
- `output/playwright/dashboard-design-audit/audit-state.json`
- `output/playwright/dashboard-design-audit/*.png`
